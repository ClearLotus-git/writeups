import os
import pickle
from pathlib import Path

import numpy as np
import requests


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8080")
MODEL_PATH = Path("model.pkl")


def get_json(path: str) -> dict:
    response = requests.get(
        f"{BASE_URL}{path}",
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def post_json(path: str, payload: dict) -> dict:
    response = requests.post(
        f"{BASE_URL}{path}",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def download_model() -> None:
    response = requests.get(
        f"{BASE_URL}/model/download",
        timeout=30,
    )
    response.raise_for_status()
    MODEL_PATH.write_bytes(response.content)


def load_bundle() -> dict:
    download_model()

    with MODEL_PATH.open("rb") as file:
        return pickle.load(file)


challenge = get_json("/challenge/whitebox")
reviews = challenge["reviews"]
budget = int(challenge["max_added_words"])

bundle = load_bundle()

print("Bundle keys:", bundle.keys())

classifier = bundle["classifier"]
vectorizer = bundle["vectorizer"]
feature_names = np.asarray(bundle["feature_names"])

print("Classifier:", type(classifier))
print("Classes:", classifier.classes_)
print("Features:", len(feature_names))
print("Reviews:", len(reviews))
print("Word budget:", budget)
