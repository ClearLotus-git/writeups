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
