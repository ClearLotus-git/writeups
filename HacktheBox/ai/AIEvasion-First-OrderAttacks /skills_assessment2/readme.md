<img width="865" height="247" alt="image" src="https://github.com/user-attachments/assets/cb70cd9d-858e-4fad-b45e-9014ed932bf2" />


```
export BASE_URL="http://154.57.164.82:32220"
```

```
curl -s "$BASE_URL/challenge" | jq
```
Output:

<img width="1003" height="611" alt="image" src="https://github.com/user-attachments/assets/2fb37cee-d9e4-40a3-8ee9-cf960d78fc7b" />


```
curl -s "$BASE_URL/model/weights" -o cifar10_model_best.pth
```

```
python3 deepfool_step.py
```

Output:

```
Current prediction: 7

Approximate boundary distances:
0: airplane   distance ≈ 1.267534
1: automobile distance ≈ 1.083013
2: bird       distance ≈ 1.201886
3: cat        distance ≈ 0.829084
4: deer       distance ≈ 1.079623
5: dog        distance ≈ 0.832938
6: frog       distance ≈ 1.065910
8: ship       distance ≈ 1.107970
9: truck      distance ≈ 0.672357

```

```
python3 deepfool_one_step.py
```




