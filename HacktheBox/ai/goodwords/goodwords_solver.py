import math
import requests

BASE_URL = "http://IP:PORT"

# Candidate legitimate-looking words to test
CANDIDATES = [
    "later",
    "home",
    "meeting",
    "work",
    "family",
    "good",
    "safe",
    "great",
    "coffee",
    "hello",
    "tomorrow",
    "thanks",
    "friend",
    "support",
    "please",
    "doing",
    "really",
    "ask",
    "report",
    "schedule",
    "project",
    "office",
    "today",
    "message",
    "call",
    "love",
    "happy",
    "week",
    "morning",
    "evening",
]


def predict(text: str) -> dict:
    """Send text to the black-box prediction endpoint."""
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"text": text},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def log_odds(probability: float) -> float:
    """
    Convert probability into log-odds.

    This is more useful than raw probability when values are
    extremely close to 1.0.
    """
    epsilon = 1e-15
    probability = min(max(probability, epsilon), 1 - epsilon)

    return math.log(probability / (1 - probability))


def submit(augmented_text: str) -> dict:
    """Submit the final append-only message."""
    response = requests.post(
        f"{BASE_URL}/submit",
        json={"augmented_text": augmented_text},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------
# 1. Retrieve the challenge
# ---------------------------------------------------------

challenge_response = requests.get(
    f"{BASE_URL}/challenge",
    timeout=10,
)
challenge_response.raise_for_status()

challenge = challenge_response.json()

base = challenge["base_message"]
budget = int(challenge["max_added_words"])
target_label = challenge["target_label"]

print("=" * 70)
print("BASE MESSAGE")
print("=" * 70)
print(base)

print("\nWord budget:", budget)
print("Target label:", target_label)


# ---------------------------------------------------------
# 2. Measure the baseline
# ---------------------------------------------------------

baseline = predict(base)
baseline_probability = float(baseline["spam_probability"])
baseline_log_odds = log_odds(baseline_probability)

print("\n" + "=" * 70)
print("BASELINE")
print("=" * 70)
print("Label:", baseline["label"])
print("Spam probability:", baseline_probability)


# ---------------------------------------------------------
# 3. Test every candidate word individually
# ---------------------------------------------------------

ranked_words = []

print("\n" + "=" * 70)
print("TESTING INDIVIDUAL WORDS")
print("=" * 70)

for word in CANDIDATES:
    test_text = f"{base} {word}"
    result = predict(test_text)

    probability = float(result["spam_probability"])

    raw_impact = baseline_probability - probability
    log_odds_impact = baseline_log_odds - log_odds(probability)

    ranked_words.append(
        {
            "word": word,
            "probability": probability,
            "raw_impact": raw_impact,
            "log_odds_impact": log_odds_impact,
        }
    )

ranked_words.sort(
    key=lambda item: item["log_odds_impact"],
    reverse=True,
)

for position, item in enumerate(ranked_words, start=1):
    print(
        f"{position:02d}. "
        f"{item['word']:12s} "
        f"log-impact={item['log_odds_impact']:.6f} "
        f"spam={item['probability']:.12f}"
    )


# Keep only words that actually reduced spam odds
useful_words = [
    item["word"]
    for item in ranked_words
    if item["log_odds_impact"] > 0
]

if not useful_words:
    raise RuntimeError("No useful candidate words were found.")

print("\nBest words:", useful_words[:10])


# ---------------------------------------------------------
# 4. Strategy A: Repeat the strongest single word
# ---------------------------------------------------------

best_word = useful_words[0]

print("\n" + "=" * 70)
print(f"STRATEGY A: REPEATING '{best_word}'")
print("=" * 70)

successful_text = None
successful_result = None

for count in range(1, budget + 1):
    added_words = [best_word] * count
    augmented = base + " " + " ".join(added_words)

    result = predict(augmented)

    print(
        f"{count:02d} added | "
        f"label={result['label']:4s} | "
        f"spam={result['spam_probability']:.12f}"
    )

    if result["label"] == target_label:
        successful_text = augmented
        successful_result = result
        break


# ---------------------------------------------------------
# 5. Strategy B: Use ranked words in a cycle
# ---------------------------------------------------------

if successful_text is None:
    print("\n" + "=" * 70)
    print("STRATEGY B: MIXING TOP-RANKED WORDS")
    print("=" * 70)

    added_words = []

    for count in range(1, budget + 1):
        word = useful_words[(count - 1) % len(useful_words)]
        added_words.append(word)

        augmented = base + " " + " ".join(added_words)
        result = predict(augmented)

        print(
            f"{count:02d} added | "
            f"word={word:12s} | "
            f"label={result['label']:4s} | "
            f"spam={result['spam_probability']:.12f}"
        )

        if result["label"] == target_label:
            successful_text = augmented
            successful_result = result
            break


# ---------------------------------------------------------
# 6. Strategy C: Greedy adaptive selection
# ---------------------------------------------------------

if successful_text is None:
    print("\n" + "=" * 70)
    print("STRATEGY C: GREEDY ADAPTIVE SEARCH")
    print("=" * 70)

    added_words = []
    current_text = base
    current_probability = baseline_probability

    for position in range(1, budget + 1):
        best_candidate = None
        best_result = None
        best_reduction = float("-inf")

        for word in useful_words:
            test_text = current_text + " " + word
            result = predict(test_text)

            probability = float(result["spam_probability"])
            reduction = current_probability - probability

            if reduction > best_reduction:
                best_reduction = reduction
                best_candidate = word
                best_result = result

        added_words.append(best_candidate)
        current_text = base + " " + " ".join(added_words)
        current_probability = float(best_result["spam_probability"])

        print(
            f"{position:02d} added | "
            f"word={best_candidate:12s} | "
            f"label={best_result['label']:4s} | "
            f"spam={current_probability:.12f}"
        )

        if best_result["label"] == target_label:
            successful_text = current_text
            successful_result = best_result
            break


# ---------------------------------------------------------
# 7. Submit if successful
# ---------------------------------------------------------

print("\n" + "=" * 70)

if successful_text is None:
    print("No ham classification found within the word budget.")
    print("Expand the candidate vocabulary and run the script again.")

else:
    added_section = successful_text[len(base):].strip()
    words_added = added_section.split()

    print("SUCCESSFUL PREDICTION")
    print("=" * 70)
    print("Label:", successful_result["label"])
    print("Spam probability:", successful_result["spam_probability"])
    print("Words added:", len(words_added))
    print("Added text:")
    print(" ".join(words_added))

    print("\nSubmitting...")

    submission = submit(successful_text)

    print("\nSubmission response:")
    print(submission)
