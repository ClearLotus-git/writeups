# HTB Academy – Skills Assessment: Feature Obfuscation Attack

## Overview

This repository contains my solution and notes for the **Feature Obfuscation Attack** Skills Assessment from HTB Academy.

The assessment demonstrates two common adversarial machine learning scenarios using **Multinomial Naive Bayes** text classifiers.

- **Phase 1 – White-Box Attack**
  - Full access to the trained model.
  - Convert positive movie reviews into negative predictions.

- **Phase 2 – Black-Box Attack**
  - No model access.
  - Convert negative movie reviews into positive predictions using only prediction queries.

The objective of both phases is to understand how feature manipulation can influence a machine learning classifier without modifying the model itself.

---

# Learning Objectives

This assessment covers several important AI security concepts:

- White-box machine learning attacks
- Black-box machine learning attacks
- Feature obfuscation
- Feature engineering
- Multinomial Naive Bayes
- Adversarial Machine Learning
- Query-based model exploration
- Decision boundaries
- Greedy optimization

---

# Challenge Overview

The assessment is divided into two independent phases.

## Phase 1 – White-Box

### Goal

Flip **10 positive movie reviews** into **negative** predictions.

### Resources

- Complete model download
- Vectorizer
- Vocabulary
- Class labels
- Feature probabilities

### Constraints

- Append only
- Maximum 30 additional words

---

## Phase 2 – Black-Box

### Goal

Flip **10 negative movie reviews** into **positive** predictions.

### Resources

- Prediction API only

### Constraints

- No access to model internals
- Maximum 40 additional words

---

# Methodology

Although both phases have the same objective, the attack methodology differs depending on the amount of information available.

---

# Phase 1 Methodology (White-Box)

The complete trained model was downloaded from the assessment server.

The model bundle contained:

- Classifier
- CountVectorizer
- Feature names
- Class labels

Because the model was fully accessible, it was possible to inspect the learned feature probabilities directly.

For each vocabulary word:

```
log P(word | negative)

vs

log P(word | positive)
```

The difference between these values indicates how strongly a word contributes toward either sentiment.

Negative-associated words were ranked and appended to each positive review until the classifier predicted the negative class.

Workflow:

```
Download model
        │
        ▼
Inspect feature probabilities
        │
        ▼
Rank negative words
        │
        ▼
Append strongest features
        │
        ▼
Predict locally
        │
        ▼
Negative prediction
        │
        ▼
Submit
```

---

# Phase 2 Methodology (Black-Box)

Unlike the white-box phase, no model information was available.

The classifier could only be queried using the prediction endpoint.

Instead of inspecting weights, the attack relied entirely on observing model behaviour.

The workflow was:

```
Original review
        │
        ▼
Measure baseline prediction
        │
        ▼
Append candidate word
        │
        ▼
Query prediction API
        │
        ▼
Record response
        │
        ▼
Repeat
```

Candidate words producing stronger positive responses were retained and used to construct the final augmented review.

This approach gradually approximates the classifier's decision boundary using repeated observations rather than direct model inspection.

---

# Why Feature Obfuscation Works

Multinomial Naive Bayes estimates the probability of a document belonging to each class based on the frequency of observed words.

Appending statistically significant words changes the evidence presented to the classifier.

For example:

```
Original Review

↓

Negative Evidence
High

↓

Append Positive Words

↓

Positive Evidence Increases

↓

Decision Boundary Crossed

↓

Positive Prediction
```

The original review remains unchanged.

Only additional words are introduced.

---

# White-Box vs Black-Box

| White-Box | Black-Box |
|------------|-----------|
| Model available | Model hidden |
| Inspect feature probabilities | Infer behaviour through queries |
| Direct feature ranking | Experimental feature ranking |
| Local prediction | Remote prediction API |
| Faster optimization | Iterative exploration |

---

# Repository Structure

```
.
├── README.md
├── phase1_whitebox.py
├── blackbox_solver.py
└── notes/
```

---

# Requirements

```
Python 3
requests
numpy
scikit-learn
```

Install dependencies:

```bash
pip install requests numpy scikit-learn
```

---

# Running

White-box

```bash
python3 phase1_whitebox.py
```

Black-box

```bash
python3 blackbox_solverV2.py
```

---
