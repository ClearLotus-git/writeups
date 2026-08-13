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
x_adv = x_norm.clone().detach().requires_grad_(True)

output = model(x_adv.unsqueeze(0))
pred = output.argmax(dim=1).item()

print("Prediction before:", pred)

# Gradient of current class
model.zero_grad()
output[0, pred].backward(retain_graph=True)
grad_current = x_adv.grad.detach().clone()

best_distance = float("inf")
best_w = None
best_class = None
best_f = None

for k in range(10):
    if k == pred:
        continue

    x_adv.grad.zero_()
    model.zero_grad()

    output[0, k].backward(retain_graph=True)
    grad_k = x_adv.grad.detach().clone()

    w = grad_k - grad_current
    f = output[0, k] - output[0, pred]

    distance = torch.abs(f) / (
        torch.norm(w.flatten()) + 1e-12
    )

    if distance.item() < best_distance:
        best_distance = distance.item()
        best_w = w.clone()
        best_class = k
        best_f = f.detach().clone()

print("Closest class:", best_class)
print("Estimated boundary distance:", best_distance)

# Minimal L2 step toward closest boundary
w_norm_sq = torch.norm(best_w.flatten()) ** 2 + 1e-12

r = (
    torch.abs(best_f)
    / w_norm_sq
) * best_w

# Small overshoot so we go slightly past the boundary
overshoot = 0.02

x_new = x_adv + (1 + overshoot) * r
x_new = x_new.detach()

# Check new prediction
with torch.no_grad():
    output_new = model(x_new.unsqueeze(0))
    pred_new = output_new.argmax(dim=1).item()

print("Prediction after one DeepFool step:", pred_new)

# L2 distance in normalized space
l2 = torch.norm(x_new - x_norm.to(device)).item()

print("Normalized-space L2:", l2)
print("Threshold:", challenge["l2_threshold"])
