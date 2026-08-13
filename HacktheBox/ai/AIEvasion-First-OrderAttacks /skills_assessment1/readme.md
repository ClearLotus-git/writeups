# Skills Assessment 1

Your task is to craft a targeted adversarial example using FGSM. Unlike the simple MNIST challenges, this assessment uses CIFAR-10 with color images and a more sophisticated classifier. You must transform a dog image into one the classifier predicts as a cat, while staying within a strict 
L ∞ perturbation budget.

All three conditions must hold: the predicted class equals the target (cat, class 3), the maximum absolute pixel difference is at most ϵ, and all pixel values remain in 
[0,1] 32×32×3.


```
$ curl -s "$BASE_URL/challenge" | jq
{
  "challenge": "Skills Assessment 1",
  "epsilon": 0.03137254901960784,
  "epsilon_description": "0.031373 (8/255)",
  "image": "iVBORw0KGgoAAAA
<snip> =", <BASE64 Continuation>

"instructions": "Implement an attack to change this dog image to a cat. Constraint: L∞ ≤ 0.031373 in [0,1] pixel space. Submit the adversarial image to /submit endpoint.",
  "max_iterations_hint": 100,
  "normalization": {
    "mean": [
      0.4914,
      0.4822,
      0.4465
    ],
    "std": [
      0.247,
      0.2435,
      0.2616
    ]
  },
  "original_class": 5,
  "original_class_name": "dog",
  "sample_index": 42,
  "target_class": 3,
  "target_class_name": "cat"
}

```

```
curl -s -X POST "$BASE_URL/predict" \
  -H 'content-type: application/json' \
  -d '{"image": "<base64 PNG of 32x32 RGB>"}' | jq
```

Output:

```
"all_probabilities": {
    "airplane": 0.0018776189535856247,
    "automobile": 0.00008390734728891402,
    "bird": 0.032560426741838455,
    "cat": 0.3050636649131775,
    "deer": 0.03268500417470932,
    "dog": 0.5486953258514404,
    "frog": 0.0017310439143329859,
    "horse": 0.07610547542572021,
    "ship": 0.0003322885022498667,
    "truck": 0.0008651679963804781
  },
  "confidence": 0.5486953258514404,
  "predicted_class": 5,
  "predicted_class_name": "dog"
}
```

```
curl -s -X POST "$BASE_URL/submit" \
  -H 'content-type: application/json' \
  -d '{"image": "<base64 PNG of 32x32 RGB>"}' | jq
```

Output:

```
"hint": "Target class not achieved. Got dog, need cat. Try more iterations or different step size.",
  "message": "Validation failed. Check constraints.",
  "success": false,
  "validation": {
    "adversarial_class": "dog",
    "adversarial_prediction": 5,
    "changed_pixel_ratio": 0.0,
    "direction_check": false,
    "gradient_alignment": 0.0,
    "linf_constraint": "≤ 0.031373",
    "linf_norm": 0.0,
    "linf_satisfied": true,
    "sufficient_coverage": false,
    "target_achieved": false,
    "target_class": "cat",
    "valid_range": true
  }
}
```

```
pip3 install numpy requests torch torchvision
```


Run script:

```
$ python3 challenge.py --host http://IP:PORT
```

<img width="1021" height="591" alt="image" src="https://github.com/user-attachments/assets/6a71589e-8c1d-47da-9a8e-50140f4a6cce" />









