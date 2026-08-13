#!/usr/bin/env python3

import argparse
import requests
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
import io
import base64
import numpy as np
import os


def base64_to_tensor(base64_str: str) -> torch.Tensor:
    """
    Convert base64-encoded PNG to tensor.

    Args:
        base64_str: Base64-encoded PNG string

    Returns:
        torch.Tensor: Image tensor in [0,1] range with shape (C, H, W)
    """
    img_bytes = base64.b64decode(base64_str)
    img = Image.open(io.BytesIO(img_bytes))
    tensor = transforms.ToTensor()(img)
    return tensor


def tensor_to_base64(tensor: torch.Tensor) -> str:
    """
    Convert tensor to base64-encoded PNG.

    Args:
        tensor: Image tensor in [0,1] range with shape (C, H, W)

    Returns:
        str: Base64-encoded PNG string
    """
    img_array = (tensor.permute(1, 2, 0).numpy() * 255).astype(np.uint8)
    img = Image.fromarray(img_array)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


class CIFAR10CNN(nn.Module):
    """
    Simple CNN for CIFAR-10 classification.

    Architecture:
        - Conv block 1: 3→32 channels, BatchNorm, ReLU, MaxPool
        - Conv block 2: 32→64 channels, BatchNorm, ReLU, MaxPool
        - FC1: 64*8*8 → 128, ReLU, Dropout(0.5)
        - FC2: 128 → 10 (logits)
    """

    def __init__(self, num_classes: int = 10):
        """
        Initialize the CNN.

        Args:
            num_classes: Number of output classes
        """
        super().__init__()

        # First convolutional block
        self.conv1 = nn.Conv2d(
            3,
            32,
            kernel_size=3,
            padding=1,
        )
        self.bn1 = nn.BatchNorm2d(32)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(
            2,
            2,
        )

        # Second convolutional block
        self.conv2 = nn.Conv2d(
            32,
            64,
            kernel_size=3,
            padding=1,
        )
        self.bn2 = nn.BatchNorm2d(64)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(
            2,
            2,
        )

        # Fully connected layers
        self.fc1 = nn.Linear(
            64 * 8 * 8,
            128,
        )
        self.relu3 = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(
            128,
            num_classes,
        )

    def forward(
        self,
        x: torch.Tensor,
    ) -> torch.Tensor:
        """
        Forward pass.
        """
        x = self.pool1(
            self.relu1(
                self.bn1(
                    self.conv1(x)
                )
            )
        )

        x = self.pool2(
            self.relu2(
                self.bn2(
                    self.conv2(x)
                )
            )
        )

        x = x.view(
            x.size(0),
            -1,
        )

        x = self.dropout(
            self.relu3(
                self.fc1(x)
            )
        )

        x = self.fc2(x)

        return x


def load_model(
    model_path: str,
    device: str = "cuda",
) -> CIFAR10CNN:
    """
    Load trained CIFAR-10 model.
    """
    model = CIFAR10CNN(
        num_classes=10
    )

    checkpoint = torch.load(
        model_path,
        map_location=device,
    )

    if (
        isinstance(checkpoint, dict)
        and "model_state_dict" in checkpoint
    ):
        model.load_state_dict(
            checkpoint["model_state_dict"]
        )
    else:
        model.load_state_dict(
            checkpoint
        )

    model = model.to(device)
    model.eval()

    return model


def ifgsm_targeted_attack(
    model: nn.Module,
    image: torch.Tensor,
    target_class: int,
    epsilon: float,
    mean: list,
    std: list,
    num_iterations: int = 50,
    alpha: float = None,
    device: str = "cuda",
) -> torch.Tensor:
    """
    Implement Iterative FGSM targeted attack.
    """
    if alpha is None:
        alpha = epsilon / num_iterations

    mean_t = torch.tensor(
        mean,
        device=device,
    ).view(
        3,
        1,
        1,
    )

    std_t = torch.tensor(
        std,
        device=device,
    ).view(
        3,
        1,
        1,
    )

    x_adv = image.clone().to(device)
    x_orig = image.clone().to(device)

    target = torch.tensor(
        [target_class],
        device=device,
    )

    print(
        f"\n{'=' * 60}"
    )
    print(
        "I-FGSM Targeted Attack"
    )
    print(
        f"{'=' * 60}"
    )
    print(
        f"Target class: {target_class}"
    )
    print(
        f"Epsilon: {epsilon:.6f} "
        f"({epsilon * 255:.1f}/255)"
    )
    print(
        f"Iterations: {num_iterations}"
    )
    print(
        f"Step size (alpha): "
        f"{alpha:.6f}"
    )
    print(
        f"{'=' * 60}\n"
    )

    for iteration in range(
        num_iterations
    ):
        x_norm = (
            x_adv - mean_t
        ) / std_t

        x_norm.requires_grad = True

        outputs = model(
            x_norm.unsqueeze(0)
        )

        loss = F.cross_entropy(
            outputs,
            target,
        )

        model.zero_grad()
        loss.backward()

        grad_norm = x_norm.grad

        grad_pixel = (
            grad_norm / std_t
        )

        x_adv = (
            x_adv
            - alpha
            * grad_pixel.sign()
        )

        delta = (
            x_adv - x_orig
        )

        delta = torch.clamp(
            delta,
            -epsilon,
            epsilon,
        )

        x_adv = (
            x_orig + delta
        )

        x_adv = torch.clamp(
            x_adv,
            0.0,
            1.0,
        )

        x_adv = x_adv.detach()

        if (
            iteration + 1
        ) % 10 == 0:
            with torch.no_grad():
                x_norm_check = (
                    x_adv - mean_t
                ) / std_t

                pred = model(
                    x_norm_check.unsqueeze(0)
                ).argmax(
                    dim=1
                ).item()

            print(
                f"  Iteration "
                f"{iteration + 1}/"
                f"{num_iterations} "
                f"- Current prediction: "
                f"{pred}"
            )

    print(
        f"\n{'=' * 60}"
    )
    print(
        "Attack complete!"
    )
    print(
        f"{'=' * 60}\n"
    )

    return (
        x_adv
        .detach()
        .cpu()
    )


def test_api_robustness(
    host: str,
    image: torch.Tensor,
) -> bool:
    """
    Test API robustness against invalid inputs.
    """
    print(
        f"\n{'=' * 60}"
    )
    print(
        "API Robustness Tests"
    )
    print(
        f"{'=' * 60}\n"
    )

    all_passed = True

    print(
        "[Test 1] Invalid JSON format..."
    )

    try:
        response = requests.post(
            f"{host}/submit",
            data="invalid json",
            headers={
                "content-type":
                "application/json"
            },
        )

        if response.status_code == 400:
            print(
                "  [+] Correctly rejected "
                "invalid JSON"
            )
        else:
            print(
                f"  [-] Expected 400, "
                f"got "
                f"{response.status_code}"
            )
            all_passed = False

    except Exception as e:
        print(
            f"  [-] Exception: {e}"
        )
        all_passed = False

    print(
        "\n[Test 2] Missing "
        "'image' field..."
    )

    try:
        response = requests.post(
            f"{host}/submit",
            json={
                "wrong_field": "data"
            },
        )

        if response.status_code == 400:
            result = response.json()

            if (
                "error" in result
                and "image"
                in result["error"].lower()
            ):
                print(
                    "  [+] Correctly rejected "
                    "missing image field"
                )
            else:
                print(
                    "  [-] Expected error "
                    "message about missing "
                    "image field"
                )
                all_passed = False
        else:
            print(
                f"  [-] Expected 400, "
                f"got "
                f"{response.status_code}"
            )
            all_passed = False

    except Exception as e:
        print(
            f"  [-] Exception: {e}"
        )
        all_passed = False

    print(
        "\n[Test 3] Invalid "
        "base64 encoding..."
    )

    try:
        response = requests.post(
            f"{host}/submit",
            json={
                "image":
                "not_valid_base64!!!"
            },
        )

        if response.status_code == 400:
            print(
                "  [+] Correctly rejected "
                "invalid base64"
            )
        else:
            print(
                f"  [-] Expected 400, "
                f"got "
                f"{response.status_code}"
            )
            all_passed = False

    except Exception as e:
        print(
            f"  [-] Exception: {e}"
        )
        all_passed = False

    print(
        "\n[Test 4] Corrupted "
        "image data..."
    )

    try:
        corrupted_base64 = (
            base64.b64encode(
                b"not a valid png image"
            )
            .decode("utf-8")
        )

        response = requests.post(
            f"{host}/submit",
            json={
                "image":
                corrupted_base64
            },
        )

        if response.status_code == 400:
            print(
                "  [+] Correctly rejected "
                "corrupted image data"
            )
        else:
            print(
                f"  [-] Expected 400, "
                f"got "
                f"{response.status_code}"
            )
            all_passed = False

    except Exception as e:
        print(
            f"  [-] Exception: {e}"
        )
        all_passed = False

    print(
        f"\n{'=' * 60}"
    )
    print(
        f"API Robustness: "
        f"{'PASSED' if all_passed else 'FAILED'}"
    )
    print(
        f"{'=' * 60}\n"
    )

    return all_passed


def test_anti_cheat(
    host: str,
    model: nn.Module,
    image: torch.Tensor,
    target_class: int,
    epsilon: float,
    mean: list,
    std: list,
    device: str,
) -> bool:
    """
    Test anti-cheat mechanisms.
    """
    print(
        f"\n{'=' * 60}"
    )
    print(
        "Anti-Cheat Mechanism Tests"
    )
    print(
        f"{'=' * 60}\n"
    )

    all_passed = True

    mean_t = torch.tensor(
        mean
    ).view(
        3,
        1,
        1,
    )

    std_t = torch.tensor(
        std
    ).view(
        3,
        1,
        1,
    )

    print(
        "[Test 1] Submitting clean "
        "image (should fail)..."
    )

    try:
        clean_base64 = (
            tensor_to_base64(image)
        )

        response = requests.post(
            f"{host}/submit",
            json={
                "image":
                clean_base64
            },
        )

        result = response.json()

        if (
            not result["success"]
            and not result[
                "validation"
            ]["target_achieved"]
        ):
            print(
                "  [+] Correctly rejected "
                "clean image"
            )
        else:
            print(
                "  [-] Should reject clean "
                "image "
                "(no target achieved)"
            )
            all_passed = False

    except Exception as e:
        print(
            f"  [-] Exception: {e}"
        )
        all_passed = False

    print(
        "\n[Test 2] Perturbation "
        "exceeding epsilon "
        "(should fail)..."
    )

    try:
        large_pert = image.clone()

        large_pert = torch.clamp(
            large_pert + epsilon * 2,
            0,
            1,
        )

        large_base64 = (
            tensor_to_base64(
                large_pert
            )
        )

        response = requests.post(
            f"{host}/submit",
            json={
                "image":
                large_base64
            },
        )

        result = response.json()

        if (
            not result["success"]
            and not result[
                "validation"
            ]["linf_satisfied"]
        ):
            print(
                "  [+] Correctly rejected "
                "oversized perturbation"
            )
        else:
            print(
                "  [-] Should reject "
                "perturbation > epsilon"
            )
            all_passed = False

    except Exception as e:
        print(
            f"  [-] Exception: {e}"
        )
        all_passed = False

    print(
        "\n[Test 3] Localized patch "
        "attack (should fail)..."
    )

    try:
        patch_image = image.clone()

        patch_image[
            :,
            :8,
            :8,
        ] = torch.clamp(
            patch_image[
                :,
                :8,
                :8,
            ] + epsilon * 0.9,
            0,
            1,
        )

        patch_base64 = (
            tensor_to_base64(
                patch_image
            )
        )

        response = requests.post(
            f"{host}/submit",
            json={
                "image":
                patch_base64
            },
        )

        result = response.json()

        if (
            not result["success"]
            and not result[
                "validation"
            ].get(
                "sufficient_coverage",
                True,
            )
        ):
            print(
                "  [+] Correctly rejected "
                "localized patch"
            )
        else:
            print(
                "  [-] Should reject "
                "patch-only attacks"
            )
            all_passed = False

    except Exception as e:
        print(
            f"  [-] Exception: {e}"
        )
        all_passed = False

    print(
        "\n[Test 4] Reversed gradient "
        "direction (should fail)..."
    )

    try:
        x_wrong = (
            image
            .clone()
            .to(device)
        )

        for _ in range(30):
            x_norm = (
                x_wrong
                - mean_t.to(device)
            ) / std_t.to(device)

            x_norm.requires_grad = True

            outputs = model(
                x_norm.unsqueeze(0)
            )

            loss = F.cross_entropy(
                outputs,
                torch.tensor(
                    [target_class],
                    device=device,
                ),
            )

            model.zero_grad()
            loss.backward()

            grad_norm = x_norm.grad

            grad_pixel = (
                grad_norm
                / std_t.to(device)
            )

            x_wrong = (
                x_wrong
                + (epsilon / 30)
                * grad_pixel.sign()
            )

            x_wrong = torch.clamp(
                x_wrong,
                0,
                1,
            )

        x_wrong = x_wrong.cpu()

        wrong_base64 = (
            tensor_to_base64(
                x_wrong
            )
        )

        response = requests.post(
            f"{host}/submit",
            json={
                "image":
                wrong_base64
            },
        )

        result = response.json()

        if not result["success"]:
            if (
                result["validation"].get(
                    "target_achieved"
                )
                and not result[
                    "validation"
                ].get(
                    "direction_check",
                    True,
                )
            ):
                print(
                    "  [+] Correctly rejected "
                    "wrong gradient direction"
                )

            elif not result[
                "validation"
            ].get(
                "target_achieved"
            ):
                print(
                    "  [+] Wrong direction "
                    "prevented target "
                    "achievement"
                )

            else:
                print(
                    "  [-] Should reject "
                    "reversed gradients"
                )
                all_passed = False
        else:
            print(
                "  [-] Should reject attacks "
                "with wrong gradient direction"
            )
            all_passed = False

    except Exception as e:
        print(
            f"  [-] Exception: {e}"
        )
        all_passed = False

    print(
        f"\n{'=' * 60}"
    )
    print(
        f"Anti-Cheat Tests: "
        f"{'PASSED' if all_passed else 'FAILED'}"
    )
    print(
        f"{'=' * 60}\n"
    )

    return all_passed


def solve_challenge(
    host: str,
    device: str = "cuda",
    run_tests: bool = False,
):
    """
    Main solver function.
    """
    print(
        f"\n{'=' * 60}"
    )
    print(
        "Skills Assessment 1"
    )
    print(
        f"{'=' * 60}\n"
    )

    # Store the assets folder beside challenge.py.
    # Example:
    # /home/htb-ac-943240/assets/
    solver_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    assets_dir = os.path.join(
        solver_dir,
        "assets",
    )

    model_path = os.path.join(
        assets_dir,
        "cifar10_model_best.pth",
    )

    os.makedirs(
        assets_dir,
        exist_ok=True,
    )

    # Fetch model if missing
    if not os.path.exists(
        model_path
    ):
        print(
            f"[1/5] Model not found at "
            f"{model_path}"
        )

        weights_url = (
            f"{host}/model/weights"
        )

        print(
            "Attempting to download "
            f"weights from: "
            f"{weights_url}"
        )

        try:
            resp = requests.get(
                weights_url,
                timeout=30,
            )

            resp.raise_for_status()

            with open(
                model_path,
                "wb",
            ) as f:
                f.write(
                    resp.content
                )

            print(
                "  Weights downloaded "
                "and saved to "
                f"{model_path}"
            )

        except (
            requests.exceptions
            .RequestException
        ) as e:
            print(
                "[-] Error: Failed to "
                "download model weights "
                f"from {weights_url}"
            )
            print(
                f"Details: {e}"
            )
            print(
                "Hint: Ensure the challenge "
                "server exposes "
                "/model/weights and is "
                "reachable."
            )
            raise

    print(
        "[1/5] Loading CIFAR-10 "
        "model..."
    )

    model = load_model(
        model_path,
        device=device,
    )

    print(
        f"  Model loaded on {device}"
    )

    print(
        "\n[2/5] Fetching "
        "challenge..."
    )

    response = requests.get(
        f"{host}/challenge"
    )

    response.raise_for_status()

    challenge = response.json()

    print(
        f"  Original class: "
        f"{challenge['original_class']} "
        f"("
        f"{challenge['original_class_name']}"
        f")"
    )

    print(
        f"  Target class: "
        f"{challenge['target_class']} "
        f"("
        f"{challenge['target_class_name']}"
        f")"
    )

    print(
        f"  Epsilon (L∞): "
        f"{challenge['epsilon']:.6f}"
    )

    print(
        f"  Max iterations hint: "
        f"{challenge['max_iterations_hint']}"
    )

    print(
        "\n[3/5] Decoding "
        "challenge image..."
    )

    image = base64_to_tensor(
        challenge["image"]
    )

    mean = challenge[
        "normalization"
    ]["mean"]

    std = challenge[
        "normalization"
    ]["std"]

    print(
        f"  Image shape: "
        f"{image.shape}"
    )

    print(
        f"  Normalization: "
        f"mean={mean}, std={std}"
    )

    with torch.no_grad():
        mean_t = torch.tensor(
            mean
        ).view(
            3,
            1,
            1,
        )

        std_t = torch.tensor(
            std
        ).view(
            3,
            1,
            1,
        )

        img_norm = (
            image - mean_t
        ) / std_t

        orig_pred = (
            model(
                img_norm
                .unsqueeze(0)
                .to(device)
            )
            .argmax(dim=1)
            .item()
        )

    print(
        "  Verified original "
        f"prediction: {orig_pred}"
    )

    if run_tests:
        print(
            "\n" + "=" * 60
        )
        print(
            "RUNNING SECURITY TESTS"
        )
        print(
            "=" * 60
        )

        robustness_passed = (
            test_api_robustness(
                host,
                image,
            )
        )

        anticheat_passed = (
            test_anti_cheat(
                host,
                model,
                image,
                challenge[
                    "target_class"
                ],
                challenge[
                    "epsilon"
                ],
                mean,
                std,
                device,
            )
        )

        if (
            robustness_passed
            and anticheat_passed
        ):
            print(
                f"\n{'=' * 60}"
            )
            print(
                "[+] ALL SECURITY "
                "TESTS PASSED"
            )
            print(
                f"{'=' * 60}\n"
            )
        else:
            print(
                f"\n{'=' * 60}"
            )
            print(
                "[-] SOME SECURITY "
                "TESTS FAILED"
            )
            print(
                f"{'=' * 60}\n"
            )

        print(
            "Proceeding with "
            "legitimate attack...\n"
        )

    print(
        "\n[4/5] Running I-FGSM "
        "targeted attack..."
    )

    adv_image = (
        ifgsm_targeted_attack(
            model=model,
            image=image,
            target_class=challenge[
                "target_class"
            ],
            epsilon=challenge[
                "epsilon"
            ],
            mean=mean,
            std=std,
            num_iterations=50,
            device=device,
        )
    )

    with torch.no_grad():
        adv_norm = (
            adv_image - mean_t
        ) / std_t

        adv_pred = (
            model(
                adv_norm
                .unsqueeze(0)
                .to(device)
            )
            .argmax(dim=1)
            .item()
        )

    print(
        "  Final adversarial "
        f"prediction: {adv_pred}"
    )

    print(
        "\n[5/5] Submitting "
        "adversarial example..."
    )

    adv_base64 = (
        tensor_to_base64(
            adv_image
        )
    )

    response = requests.post(
        f"{host}/submit",
        json={
            "image":
            adv_base64
        },
    )

    response.raise_for_status()

    result = response.json()

    print(
        f"\n{'=' * 60}"
    )
    print(
        "Validation Results"
    )
    print(
        f"{'=' * 60}"
    )

    validation = result[
        "validation"
    ]

    print(
        f"L∞ norm: "
        f"{validation['linf_norm']:.6f} "
        f"/ "
        f"{challenge['epsilon']:.6f}"
    )

    print(
        "L∞ constraint satisfied: "
        f"{validation['linf_satisfied']}"
    )

    print(
        "Valid range [0,1]: "
        f"{validation['valid_range']}"
    )

    print(
        "Adversarial prediction: "
        f"{validation['adversarial_class']}"
    )

    print(
        "Target class: "
        f"{validation['target_class']}"
    )

    print(
        "Target achieved: "
        f"{validation['target_achieved']}"
    )

    print(
        f"\nSuccess: "
        f"{result['success']}"
    )

    if result["success"]:
        print(
            f"\n{'=' * 60}"
        )
        print(
            f"[+] FLAG: "
            f"{result['flag']}"
        )
        print(
            f"{'=' * 60}\n"
        )

    else:
        print(
            f"\n[-] "
            f"{result['message']}"
        )

        if "hint" in result:
            print(
                f"[!] "
                f"{result['hint']}\n"
            )


def main():
    """
    Main entry point.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Working solver for "
            "Skills Assessment 1"
        )
    )

    parser.add_argument(
        "--host",
        type=str,
        default=(
            "http://localhost:8000"
        ),
        help=(
            "Challenge server host URL "
            "(default: "
            "http://localhost:8000)"
        ),
    )

    parser.add_argument(
        "--device",
        type=str,
        default=(
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        ),
        help=(
            "Device to run attack on "
            "(default: cuda if "
            "available, else cpu)"
        ),
    )

    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help=(
            "Skip API robustness and "
            "anti-cheat tests "
            "(tests run by default)"
        ),
    )

    args = parser.parse_args()

    try:
        solve_challenge(
            args.host,
            args.device,
            not args.skip_tests,
        )

    except (
        requests.exceptions
        .ConnectionError
    ):
        print(
            "\n[-] Error: Could not "
            f"connect to {args.host}"
        )

    except Exception as e:
        print(
            f"\n[-] Error: "
            f"{str(e)}\n"
        )
        raise


if __name__ == "__main__":
    main()
