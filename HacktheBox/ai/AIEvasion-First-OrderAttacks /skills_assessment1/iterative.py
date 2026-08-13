import io
import base64
import requests
import torch
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms

from model import load_model

def tensor_to_base64(tensor: torch.Tensor) -> str:
    tensor = tensor.detach().cpu()
    img_array = (
        tensor.permute(1, 2, 0).numpy() * 255
    ).round().clip(0, 255).astype("uint8")

    img = Image.fromarray(img_array)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    return base64.b64encode(
        buffer.getvalue()
    ).decode("ascii")

BASE_URL = "http://154.57.164.82:31284"

device = "cuda" if torch.cuda.is_available() else "cpu"

challenge = requests.get(f"{BASE_URL}/challenge").json()

raw = base64.b64decode(challenge["image"])
img = Image.open(io.BytesIO(raw)).convert("RGB")

x = transforms.ToTensor()(img).to(device)

mean = torch.tensor(
    challenge["normalization"]["mean"],
    device=device,
).view(3, 1, 1)

std = torch.tensor(
    challenge["normalization"]["std"],
    device=device,
).view(3, 1, 1)

model = load_model(
    "cifar10_model_best.pth",
    device=device,
)

target_class = int(challenge["target_class"])
epsilon = float(challenge["epsilon"])

target = torch.tensor(
    [target_class],
    device=device,
)

x_orig = x.clone().detach()
x_adv = x.clone().detach()

num_iterations = 20
alpha = epsilon / num_iterations

print("Starting targeted I-FGSM")
print("Original class:", challenge["original_class"])
print("Target class:", target_class)
print("Epsilon:", epsilon)
print("Alpha:", alpha)
print()

for i in range(num_iterations):
    x_adv.requires_grad = True

    x_norm = (x_adv - mean) / std

    output = model(
        x_norm.unsqueeze(0)
    )

    loss = F.cross_entropy(
        output,
        target,
    )

    model.zero_grad()
    loss.backward()

    grad = x_adv.grad

    # Targeted attack: move opposite the gradient
    x_adv = (
        x_adv
        - alpha * grad.sign()
    )

    # Keep total change within epsilon
    delta = x_adv - x_orig

    delta = torch.clamp(
        delta,
        -epsilon,
        epsilon,
    )

    x_adv = x_orig + delta

    # Keep valid pixel range
    x_adv = torch.clamp(
        x_adv,
        0.0,
        1.0,
    ).detach()

    with torch.no_grad():
        check_norm = (
            x_adv - mean
        ) / std

        output_check = model(
            check_norm.unsqueeze(0)
        )

        pred = output_check.argmax(
            dim=1
        ).item()

        target_loss = F.cross_entropy(
            output_check,
            target,
        ).item()

        max_change = torch.abs(
            x_adv - x_orig
        ).max().item()

    print(
        f"Iteration {i + 1:2d} | "
        f"pred={pred} | "
        f"target_loss={target_loss:.4f} | "
        f"Linf={max_change:.6f}"
    )

    if pred == target_class:
        print()
        print("SUCCESS: target class reached")
        break
