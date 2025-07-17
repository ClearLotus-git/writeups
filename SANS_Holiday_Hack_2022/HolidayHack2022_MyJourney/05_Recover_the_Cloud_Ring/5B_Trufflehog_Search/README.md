# SANS Holiday Hack Challenge 2022 - KringleCon V: Golden Rings
## Recover the Cloud Ring
### Trufflehog Search
**Difficulty:** 🎄🎄

The goal of this challenge was to uncover AWS credentials hidden in a Git repository using the Trufflehog tool.

---

###  Strategy

After speaking with Jill Underpole, it became clear that the objective involved scanning a remote Git repo for sensitive credentials like AWS keys. The suggested tool, [Trufflehog](https://github.com/trufflesecurity/trufflehog), is great at digging through Git history for high-entropy secrets.

---

###  Investigation

First, I cloned the repo using the URL provided in the Cloud Ring conversation:
```bash
git clone https://haugfactory.com/orcadmin/aws_scripts
```

Rather than manually inspecting each commit, I took a shortcut by running `trufflehog` on the repo:
```bash
trufflehog https://haugfactory.com/orcadmin/aws_scripts
```

The tool automatically identified AWS credentials within a file named `put_policy.py`. This file had multiple commits that exposed both the `aws_access_key_id` and the `aws_secret_access_key`.

---

###  Solution

The answer to the challenge prompt — "What file contains the AWS credentials?" — is:

**`put_policy.py`**

---

###  Lessons Learned

- Trufflehog is a fast and effective way to scan repos for sensitive data leaks.
- Even deleted or modified credentials in past commits can still be recovered.
- This exercise emphasizes why developers should never hard-code secrets and should rotate keys often.
