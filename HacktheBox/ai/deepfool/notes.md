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


Original class vs. target class

chall.label   # original label
chall.target  # desired adversarial label

L2 distance

Original:  [0.2, 0.5, 0.8]
Modified:  [0.3, 0.5, 0.7]

l2 = np.linalg.norm(modified - original)

Gradient

```
              Pixel 1   Pixel 2   Pixel 3

gradient =    +0.8      -0.1      +0.02
```
logits[0, target].backward()
grad_target = x.grad

Decision boundary

```
              Model predicts 3

                   ↑
                   |
              x x x|x x x
            x      |      x
-------------------+----------------
                   |
                   |     ●
                   |     7
                   |
              Model predicts 7
```

Perturbation

adversarial image = original image + tiny changes

```
Original:
[0.20, 0.50, 0.80]

Perturbation:
[+0.03, -0.01, +0.02]

               +

Adversarial:
[0.23, 0.49, 0.82]
```

final calc

np.linalg.norm(adversarial - original)
