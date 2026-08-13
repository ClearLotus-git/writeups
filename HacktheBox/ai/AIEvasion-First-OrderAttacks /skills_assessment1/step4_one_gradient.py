import io
import base64
import requests
import torch
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms

from model import load_model


BASE_URL = "http://154.57.164.82:31284"

device = "cuda" if torch.cuda.is_available() else "cpu"

# 1. Get challenge
challenge = requests.get(f"{BASE_URL}/challenge").json()

# 2. Decode image
raw = base64.b64decode(challenge["image"])
img = Image.open(io.BytesIO(raw)).convert("RGB")
x = transforms.ToTensor()(img).to(device)

# 3. Load normalization values
mean = torch.tensor(
    challenge["normalization"]["mean"],
    device=device,
).view(3, 1, 1)

std = torch.tensor(
    challenge["normalization"]["std"],
    device=device,
).view(3, 1, 1)

# 4. Load model
model = load_model(
    "cifar10_model_best.pth",
    device=device,
)

target_class = int(challenge["target_class"])

# 5. Make image require gradients
x_adv = x.clone().detach()
x_adv.requires_grad = True

# 6. Normalize before model input
x_norm = (x_adv - mean) / std

# 7. Forward pass
output = model(x_norm.unsqueeze(0))

pred_before = output.argmax(dim=1).item()

print("Prediction before step:", pred_before)
print("Target class:", target_class)

# 8. Build target tensor
target = torch.tensor(
    [target_class],
    device=device,
)

# 9. Compute loss toward target class
loss = F.cross_entropy(output, target)

print("Target loss before step:", loss.item())

# 10. Backpropagate to image pixels
model.zero_grad()
loss.backward()

grad = x_adv.grad

print("Gradient shape:", grad.shape)
print("Gradient min:", grad.min().item())
print("Gradient max:", grad.max().item())
print("Gradient mean abs:", grad.abs().mean().item())

# 11. Take ONE small targeted step
epsilon = float(challenge["epsilon"])
alpha = epsilon / 10

x_new = x_adv - alpha * grad.sign()

# 12. Keep pixels valid
x_new = torch.clamp(x_new, 0.0, 1.0).detach()

# 13. Check prediction after one step
with torch.no_grad():
    x_new_norm = (x_new - mean) / std
    output_new = model(x_new_norm.unsqueeze(0))
    pred_after = output_new.argmax(dim=1).item()
    new_loss = F.cross_entropy(output_new, target)

print("Prediction after one step:", pred_after)
print("Target loss after step:", new_loss.item())
print(
    "Max pixel change:",
    torch.abs(x_new - x).max().item()
)
