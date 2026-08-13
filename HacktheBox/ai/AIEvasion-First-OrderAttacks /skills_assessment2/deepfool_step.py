import io
import base64
import requests
import torch
from PIL import Image
import torchvision.transforms as transforms

from model import load_model


BASE_URL = "http://YOUR_INSTANCE_IP:PORT"

device = "cuda" if torch.cuda.is_available() else "cpu"

challenge = requests.get(f"{BASE_URL}/challenge").json()

raw = base64.b64decode(challenge["image"])
img = Image.open(io.BytesIO(raw)).convert("RGB")
x = transforms.ToTensor()(img)

mean = torch.tensor(
    challenge["normalization"]["mean"]
).view(3, 1, 1)

std = torch.tensor(
    challenge["normalization"]["std"]
).view(3, 1, 1)

model = load_model(
    "cifar10_model_best.pth",
    device=device,
)

# Work in normalized space
x_norm = ((x - mean) / std).to(device)
x_norm = x_norm.clone().detach().requires_grad_(True)

output = model(x_norm.unsqueeze(0))
pred = output.argmax(dim=1).item()

print("Current prediction:", pred)

# Gradient of current class
model.zero_grad()
output[0, pred].backward(retain_graph=True)
grad_current = x_norm.grad.detach().clone()

class_names = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]

print()
print("Approximate boundary distances:")

for k in range(10):
    if k == pred:
        continue

    x_norm.grad.zero_()
    model.zero_grad()

    output[0, k].backward(retain_graph=True)
    grad_k = x_norm.grad.detach().clone()

    w = grad_k - grad_current
    f = output[0, k] - output[0, pred]

    distance = torch.abs(f) / (
        torch.norm(w.flatten()) + 1e-12
    )

    print(
        f"{k}: {class_names[k]:10s} "
        f"distance ≈ {distance.item():.6f}"
    )
