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

classes = list(classifier.classes_)

negative_index = classes.index("negative")
positive_index = classes.index("positive")

negative_log_probabilities = classifier.feature_log_prob_[negative_index]
positive_log_probabilities = classifier.feature_log_prob_[positive_index]

# Positive value means the word favors the negative class.
negative_strength = (
    negative_log_probabilities
    - positive_log_probabilities
)

ranked_indices = np.argsort(negative_strength)[::-1]

negative_words = []

for index in ranked_indices:
    word = str(feature_names[index])

    # Keep simple letter-only words to avoid tokenization surprises.
    if word.isalpha() and len(word) > 1:
        negative_words.append(
            {
                "word": word,
                "strength": float(negative_strength[index]),
            }
        )

print("\nStrongest negative-associated words:")

for item in negative_words[:30]:
    print(
        f"{item['word']:20s} "
        f"strength={item['strength']:.4f}"
    )

def local_predict(text: str) -> tuple[str, np.ndarray]:
    vector = vectorizer.transform([text])
    label = str(classifier.predict(vector)[0])
    probabilities = classifier.predict_proba(vector)[0]

    return label, probabilities


for review in reviews:
    label, probabilities = local_predict(review["text"])

    print(
        review["id"],
        label,
        probabilities,
    )

def negative_probability(text: str) -> float:
    vector = vectorizer.transform([text])
    probabilities = classifier.predict_proba(vector)[0]
    return float(probabilities[negative_index])


candidate_words = [
    item["word"]
    for item in negative_words[:100]
]


def solve_whitebox_review(
    original_text: str,
    max_words: int,
) -> tuple[str, list[str], dict]:
    added_words: list[str] = []
    current_text = original_text

    for position in range(max_words):
        best_word = None
        best_probability = -1.0
        best_label = None

        for word in candidate_words:
            test_text = current_text + " " + word
            label, _ = local_predict(test_text)
            probability = negative_probability(test_text)

            if probability > best_probability:
                best_probability = probability
                best_word = word
                best_label = label

        if best_word is None:
            break

        added_words.append(best_word)
        current_text = original_text + " " + " ".join(added_words)

        print(
            f"  {position + 1:02d} "
            f"word={best_word:18s} "
            f"negative_probability={best_probability:.6f} "
            f"label={best_label}"
        )

        label, probabilities = local_predict(current_text)

        if label == "negative":
            return current_text, added_words, {
                "label": label,
                "probabilities": probabilities.tolist(),
            }

    label, probabilities = local_predict(current_text)

    return current_text, added_words, {
        "label": label,
        "probabilities": probabilities.tolist(),
    }

solutions = []

for review in reviews:
    print("\nSolving:", review["id"])

    augmented_text, added_words, result = solve_whitebox_review(
        review["text"],
        budget,
    )

    print("Final label:", result["label"])
    print("Words added:", len(added_words))
    print("Added sequence:", " ".join(added_words))

    solutions.append(
        {
            "id": review["id"],
            "augmented_text": augmented_text,
        }
    )

submission = post_json(
    "/submit/whitebox",
    {"solutions": solutions},
)

print("\nSubmission response:")
print(submission)
