# HTB Academy – GoodWords Challenge (Black-Box AI Evasion)

## Overview

This project contains my solution and notes for the **GoodWords Challenge** from HTB Academy.

The objective is to manipulate a **Multinomial Naive Bayes spam classifier** by appending legitimate-looking words to a spam SMS until the classifier predicts **ham**, while treating the model as a **black box**.

The challenge demonstrates how attackers (or AI security testers) can learn about a machine learning model **without ever seeing its internal parameters**.

---

# Learning Objectives

This challenge teaches several important AI security concepts:

- Black-box machine learning attacks
- Query-based model exploration
- Adaptive testing
- Decision boundaries
- Naive Bayes spam classification
- Feature influence
- Adversarial Machine Learning

---

# Challenge Workflow

The challenge exposes three API endpoints.

## 1. `/challenge`

Returns:

- Base spam message
- Maximum number of words that may be appended
- Desired target label (`ham`)

Example:

```json
{
    "base_message": "...",
    "max_added_words": 25,
    "target_label": "ham"
}
```

---

## 2. `/predict`

Receives arbitrary text and returns

```json
{
    "label": "spam",
    "spam_probability": 0.9999
}
```

This endpoint acts as the black-box model.

---

## 3. `/submit`

Validates that:

- the original message was not modified
- only appended words were added
- the word budget was respected
- the final prediction is `ham`

If successful, the challenge returns the flag.

---

# Attack Strategy

The model is treated as a complete black box.

Instead of inspecting model weights, the script repeatedly queries the API and observes how the prediction changes.

The overall process is:

```
Get base message
        │
        ▼
Measure baseline probability
        │
        ▼
Test candidate words
        │
        ▼
Measure probability changes
        │
        ▼
Rank words by effectiveness
        │
        ▼
Construct augmented message
        │
        ▼
Repeat until prediction = ham
```

---

# Script Workflow

## Step 1

Retrieve the challenge.

```text
GET /challenge
```

Receive:

- base message
- word budget
- target label

---

## Step 2

Measure the original spam probability.

Example:

```
spam_probability = 0.999999998
```

This becomes the baseline.

---

## Step 3

Test candidate words individually.

Example:

```
base + meeting
base + later
base + thanks
```

Each word is evaluated independently.

---

## Step 4

Rank candidate words.

Words producing the largest reduction in spam probability are ranked highest.

Example:

```
later
meeting
home
family
```

---

## Step 5

Construct an augmented message.

The script gradually appends effective words while respecting the challenge's word budget.

```
Base

↓

Base later

↓

Base later meeting

↓

Base later meeting family
```

After each addition the script queries the model again.

---

## Step 6

Once the classifier predicts

```
ham
```

the augmented message is submitted to the challenge endpoint.

---

# Why This Works

Multinomial Naive Bayes bases its prediction on word frequencies.

Certain words are statistically associated with legitimate messages.

Appending these words increases the evidence for the **ham** class until the decision boundary is crossed.

The model itself is never modified.

Only the input changes.

---

# What This Demonstrates

This challenge illustrates a core concept in adversarial machine learning:

> A model's behaviour can often be approximated simply by observing how its outputs change in response to carefully chosen inputs.

The script effectively learns which words influence the classifier most strongly without needing access to:

- model weights
- feature probabilities
- training data
- source code

This is the essence of a **black-box attack**.

---

# Repository Structure

```
.
├── README.md
├── goodwords_solver.py
└── notes/
```

---

# Requirements

```
Python 3.10+
requests
```

Install dependencies:

```bash
pip install requests
```

---

# Running

```bash
python3 goodwords_solver.py
```

---

# Key Takeaways

- Black-box models can be studied through repeated observation.
- Small input changes can significantly affect ML predictions.
- Query-based testing is a fundamental technique in AI red teaming.
- Multinomial Naive Bayes is particularly sensitive to word frequency.
- Understanding model behaviour is often more valuable than understanding model internals.

---

# Disclaimer

This repository was created for educational purposes while completing the HTB Academy GoodWords challenge.

The techniques demonstrated here should only be used in authorized environments such as training labs, CTFs, or systems where explicit permission has been granted.

