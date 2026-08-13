import io
import base64
import requests
import torch
from PIL import Image
import torchvision.transforms as transforms

from model import load_model


BASE_URL = "http://154.57.164.82:31284"

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

x_norm = (x - mean) / std

with torch.no_grad():
    output = model(
        x_norm.unsqueeze(0).to(device)
    )
    pred = output.argmax(dim=1).item()

print("Expected original class:", challenge["original_class"])
print("Expected name:", challenge["original_class_name"])
print("Local prediction:", pred)
