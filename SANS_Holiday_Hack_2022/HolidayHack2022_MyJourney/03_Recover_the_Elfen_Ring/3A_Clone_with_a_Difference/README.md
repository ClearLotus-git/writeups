# Recover the Elfen Ring: Clone with a Difference  
**SANS Holiday Hack Challenge 2022 – KringleCon V: Golden Rings**  
**Difficulty:** 🎄

## Overview  
This objective tests your ability to work with Git in a slightly tricky scenario. You’re given a repository URL that doesn’t clone cleanly over SSH. A hint from Bow Ninecandle suggests switching to **HTTPS cloning**, which turns out to be the key. The goal: clone the repo and extract the last word from its `README.md`.

---

## Steps Performed

### 1. Initial SSH Clone Fails  
Attempting to clone with the provided SSH-style URL results in a permission error (no valid credentials / access).

### 2. Convert to HTTPS  
Using the hint “HTTPS Git Cloning,” I rewrote the URL and successfully cloned the repository:

```bash
git clone https://haugfactory.com/asnowball/aws_scripts.git
```

Successful output confirmed the repository downloaded locally into `aws_scripts/`.

---

### 3. Read the README  
To grab the last word in the `README.md`:

```bash
tail -n1 aws_scripts/README.md | rev | cut -d " " -f 1 | rev
```

**Result:** `maintainers.` (with punctuation)

Strip the period and submit **maintainers**.

---

## Answer Submission  
Verified using the in-environment tool:

```bash
runtoanswer
# Prompt: What's the last word in the README.md file for the aws_scripts repo?
> maintainers
# Response: Your answer is correct!
```

---

## Outcome  
Repository successfully cloned over HTTPS, README reviewed, and final answer (`maintainers`) confirmed. Challenge complete.
