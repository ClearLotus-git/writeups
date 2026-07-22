#!/usr/bin/env python3

import os
import sys
from typing import Any

import requests


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8080").rstrip("/")
TIMEOUT = 30

POSITIVE_WORDS = [
    "excellent",
    "amazing",
    "wonderful",
    "brilliant",
    "fantastic",
    "great",
    "superb",
    "outstanding",
    "perfect",
    "favorite",
    "best",
    "masterpiece",
    "beautiful",
    "enjoyable",
    "entertaining",
    "delightful",
    "charming",
    "moving",
    "powerful",
    "memorable",
    "impressive",
    "engaging",
    "exciting",
    "fun",
    "funny",
    "interesting",
    "original",
    "creative",
    "strong",
    "talented",
    "recommended",
    "recommend",
    "loved",
    "love",
    "enjoyed",
    "pleased",
    "quality",
    "success",
    "effective",
    "remarkable",
    "magnificent",
    "incredible",
    "heartwarming",
    "compelling",
    "absorbing",
    "satisfying",
    "likable",
    "pleasant",
    "rewarding",
    "exceptional",
    "fascinating",
    "spectacular",
    "terrific",
    "awesome",
    "clever",
    "smart",
    "touching",
    "gorgeous",
    "stunning",
    "classic",
    "gem",
    "performance",
    "performances",
    "acting",
    "actor",
    "actors",
    "actress",
    "director",
    "direction",
    "story",
    "characters",
    "cinema",
    "cinematic",
    "screenplay",
    "visuals",
    "music",
    "experience",
]


session = requests.Session()
prediction_cache: dict[str, dict[str, Any]] = {}


def get_json(path: str) -> dict[str, Any]:
    response = session.get(
        f"{BASE_URL}{path}",
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def post_json(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    response = session.post(
        f"{BASE_URL}{path}",
        json=payload,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def predict(text: str) -> dict[str, Any]:
    if text not in prediction_cache:
        prediction_cache[text] = post_json(
            "/predict",
            {"text": text},
        )

    return prediction_cache[text]


def positive_probability(result: dict[str, Any]) -> float:
    direct = float(result.get("positive_probability", 0.0))

    if direct > 0.0:
        return direct

    negative = float(result.get("negative_probability", 1.0))
    return max(0.0, 1.0 - negative)


def build_text(original: str, words: list[str]) -> str:
    if not words:
        return original

    return original + " " + " ".join(words)


def repeated_text(original: str, word: str, count: int) -> str:
    return build_text(original, [word] * count)


def find_minimum_flip_count(
    original: str,
    word: str,
    max_words: int,
) -> tuple[int, dict[str, Any]] | None:
    """
    First test the word repeated to the full budget.

    If that flips the label, use binary search to find the
    smallest repetition count that still produces positive.
    """

    full_text = repeated_text(original, word, max_words)
    full_result = predict(full_text)

    if full_result["label"] != "positive":
        return None

    low = 1
    high = max_words
    best_count = max_words
    best_result = full_result

    while low <= high:
        middle = (low + high) // 2

        test_text = repeated_text(original, word, middle)
        result = predict(test_text)

        if result["label"] == "positive":
            best_count = middle
            best_result = result
            high = middle - 1
        else:
            low = middle + 1

    return best_count, best_result


def find_best_single_word_solution(
    original: str,
    max_words: int,
) -> tuple[list[str], dict[str, Any]] | None:
    successful: list[tuple[int, float, str, dict[str, Any]]] = []

    print("\nTesting repeated positive words...")

    for number, word in enumerate(POSITIVE_WORDS, start=1):
        result = find_minimum_flip_count(
            original,
            word,
            max_words,
        )

        full_budget_result = predict(
            repeated_text(original, word, max_words)
        )

        probability = positive_probability(full_budget_result)

        print(
            f"[{number:02d}/{len(POSITIVE_WORDS):02d}] "
            f"{word:18s} "
            f"full-budget-label={full_budget_result['label']:8s} "
            f"positive={probability:.16e}"
        )

        if result is not None:
            count, flip_result = result

            successful.append(
                (
                    count,
                    -positive_probability(flip_result),
                    word,
                    flip_result,
                )
            )

    if not successful:
        return None

    successful.sort(
        key=lambda item: (
            item[0],
            item[1],
        )
    )

    count, _, word, result = successful[0]

    return [word] * count, result


def find_pair_solution(
    original: str,
    max_words: int,
) -> tuple[list[str], dict[str, Any]] | None:
    """
    Fallback strategy.

    Rank words by their full-budget positive probability,
    then test alternating combinations of the strongest words.
    """

    scored_words: list[tuple[float, str]] = []

    for word in POSITIVE_WORDS:
        result = predict(
            repeated_text(original, word, max_words)
        )

        scored_words.append(
            (
                positive_probability(result),
                word,
            )
        )

    scored_words.sort(reverse=True)

    top_words = [
        word
        for _, word in scored_words[:20]
    ]

    print("\nNo single repeated word flipped the review.")
    print("Testing alternating pairs from the top candidates...")

    best_solution = None

    for first_index, first_word in enumerate(top_words):
        for second_word in top_words[first_index + 1:]:
            additions = []

            for position in range(max_words):
                if position % 2 == 0:
                    additions.append(first_word)
                else:
                    additions.append(second_word)

            text = build_text(original, additions)
            result = predict(text)
            probability = positive_probability(result)

            print(
                f"{first_word:16s} + {second_word:16s} "
                f"label={result['label']:8s} "
                f"positive={probability:.16e}"
            )

            if result["label"] == "positive":
                best_solution = (
                    additions,
                    result,
                )
                return best_solution

    return None


def solve_review(
    review_id: str,
    original: str,
    max_words: int,
) -> dict[str, Any]:
    baseline = predict(original)

    print("\n" + "=" * 78)
    print(f"Review ID: {review_id}")
    print(f"Baseline label: {baseline['label']}")
    print(
        "Baseline positive probability:",
        f"{positive_probability(baseline):.16e}",
    )

    solution = find_best_single_word_solution(
        original,
        max_words,
    )

    if solution is None:
        solution = find_pair_solution(
            original,
            max_words,
        )

    if solution is None:
        raise RuntimeError(
            f"Could not flip {review_id}. "
            "Expand the positive candidate vocabulary."
        )

    added_words, result = solution
    augmented_text = build_text(
        original,
        added_words,
    )

    verification = predict(augmented_text)

    print("\nSolved:")
    print("Final label:", verification["label"])
    print(
        "Positive probability:",
        f"{positive_probability(verification):.16e}",
    )
    print("Words added:", len(added_words))
    print("Added words:", " ".join(added_words))

    if len(added_words) > max_words:
        raise RuntimeError(
            f"{review_id} exceeded the word budget."
        )

    if not augmented_text.startswith(original):
        raise RuntimeError(
            f"{review_id} modified the original text."
        )

    if verification["label"] != "positive":
        raise RuntimeError(
            f"{review_id} failed final local verification."
        )

    return {
        "id": review_id,
        "augmented_text": augmented_text,
    }


def main() -> None:
    try:
        health = get_json("/health")
        print("Health:", health)

        challenge = get_json("/challenge/blackbox")

        reviews = challenge["reviews"]
        max_words = int(challenge["max_added_words"])

        print("\nPhase:", challenge.get("phase", "blackbox"))
        print("Review count:", len(reviews))
        print("Maximum added words:", max_words)

        solutions = []

        for review in reviews:
            solution = solve_review(
                review_id=review["id"],
                original=review["text"],
                max_words=max_words,
            )

            solutions.append(solution)

        print("\n" + "=" * 78)
        print("All reviews flipped locally.")
        print("Submitting black-box solutions...")

        response = post_json(
            "/submit/blackbox",
            {"solutions": solutions},
        )

        print("\nSubmission response:")
        print(response)

        try:
            status = get_json("/status")
            print("\nAssessment status:")
            print(status)
        except requests.RequestException:
            pass

    except requests.RequestException as error:
        print(f"\nHTTP error: {error}", file=sys.stderr)
        sys.exit(1)

    except (KeyError, ValueError, RuntimeError) as error:
        print(f"\nSolver error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
