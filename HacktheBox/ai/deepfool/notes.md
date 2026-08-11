Attack snip

```
cand = deepfool_targeted(
    model,
    chall.x01,
    target=chall.target,
    overshoot=ov,
    max_iter=100,
)
```


1. Is this a valid 28×28 image?
2. How far is it from the original?
3. Is distance <= threshold?
4. What does the server model predict?
5. Is prediction == target?

pass => print("Flag:", r.json().get("flag"))

<img width="615" height="40" alt="image" src="https://github.com/user-attachments/assets/80316229-0dfe-4710-8001-88edc7f7b02f" />
