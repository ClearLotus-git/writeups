# DeepFool Challenge

Challenge Summary: 
Take the provided image whose label is 4, make the model predict 6, and keep the pixel modification within L2 ≤ 0.75.

Setup: 

```
$ export BASE_URL="http://154.57.164.82:32318"
curl -s "$BASE_URL/health"
{"status":"ok","l2_threshold":0.75,"index":95,"target":6}┌─[eu-academy-5]─[10.10.14.44]─[htb-ac-943240@htb-wggfjhe5e1]─[~]
└──╼ [★]$ curl -s "$BASE_URL/health" | jq
{
  "status": "ok",
  "l2_threshold": 0.75,
  "index": 95,
  "target": 6
}
```

```
$ curl -s "$BASE_URL/challenge" | jq
{
  "sample_index": 95,
  "l2_threshold": 0.75,
  "target": 6,
  "label": 4,
  "image_b64": "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABEklEQVR42s1SsUoDURCcF4xFLJLi0po0ES6NhZbKlZp/ENs0wTY/EBsLvTSCVgF7SzuNoHWKpEgTA2IhKNcEtJq5tQhI7o4rBbdZdodZZmcX+P/RkOkQAFBI9IMACEKLzbKcu8UUlTkZ3XppqBpqfOSGJMMM7XjCkYdQZCeD1d9ID/VInJVT0Hpjwu8eNi4pPgHVpHySPaBFigfoj/zVVfrOuWcAzhWmW8OT7RoAYG25354Bu+61aYj9C8QfnytTWyRJzhekSEZXyDpUKy3zTXu12xxIkkySKUp7UOyO798pkvOzzayvtdLOtUgOijnHEkl1c8BHSabT3zqh9vzLLDY/h9p+oWb7eS9SeeiU//wPfwBUpIYiGQCYgQAAAABJRU5ErkJggg=="
}
```

```
$ curl -s -X POST "$BASE_URL/predict" \
  -H 'content-type: application/json' \
  -d '{"image_b64": "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABEklEQVR42s1SsUoDURCcF4xFLJLi0po0ES6NhZbKlZp/ENs0wTY/EBsLvTSCVgF7SzuNoHWKpEgTA2IhKNcEtJq5tQhI7o4rBbdZdodZZmcX+P/RkOkQAFBI9IMACEKLzbKcu8UUlTkZ3XppqBpqfOSGJMMM7XjCkYdQZCeD1d9ID/VInJVT0Hpjwu8eNi4pPgHVpHySPaBFigfoj/zVVfrOuWcAzhWmW8OT7RoAYG25354Bu+61aYj9C8QfnytTWyRJzhekSEZXyDpUKy3zTXu12xxIkkySKUp7UOyO798pkvOzzayvtdLOtUgOijnHEkl1c8BHSabT3zqh9vzLLDY/h9p+oWb7eS9SeeiU//wPfwBUpIYiGQCYgQAAAABJRU5ErkJggg=="}' | jq
{
  "pred": 4,
  "confidence": 0.975742757320404
}

```

example output incorrect:

```
$ curl -s -X POST "$BASE_URL/submit" \
  -H 'content-type: application/json' \
  -d '{"image_b64": "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABEklEQVR42s1SsUoDURCcF4xFLJLi0po0ES6NhZbKlZp/ENs0wTY/EBsLvTSCVgF7SzuNoHWKpEgTA2IhKNcEtJq5tQhI7o4rBbdZdodZZmcX+P/RkOkQAFBI9IMACEKLzbKcu8UUlTkZ3XppqBpqfOSGJMMM7XjCkYdQZCeD1d9ID/VInJVT0Hpjwu8eNi4pPgHVpHySPaBFigfoj/zVVfrOuWcAzhWmW8OT7RoAYG25354Bu+61aYj9C8QfnytTWyRJzhekSEZXyDpUKy3zTXu12xxIkkySKUp7UOyO798pkvOzzayvtdLOtUgOijnHEkl1c8BHSabT3zqh9vzLLDY/h9p+oWb7eS9SeeiU//wPfwBUpIYiGQCYgQAAAABJRU5ErkJggg=="}' | jq
{
  "detail": "Wrong target: predicted 4, need 6"
}
```

Start:

1. Create script
2. Run script --- deepfool.py
3. obtain flag



<img width="746" height="695" alt="image" src="https://github.com/user-attachments/assets/22036bf0-2e57-4cb2-8346-c01afda51857" />










