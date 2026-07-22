These are scripts used in goodwords challenge. This script should give the FLAG in one run.

You will take a strong spam message and append a compact sequence of legitimate looking words so that a Multinomial Naive Bayes model predicts ham. The service is black box: you see only labels and spam probabilities from the /predict endpoint. When your augmented message satisfies the append only constraint and the word budget, /submit returns a static flag.

```
python3 goodwords_solver.py
```

