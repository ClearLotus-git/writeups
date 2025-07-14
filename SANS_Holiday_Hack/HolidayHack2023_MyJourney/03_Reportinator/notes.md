## Objective 4 – Reportinator


---

###  Objective

Noel Boetie used ChatGPT (well… “ChatNPT”) to draft a penetration test report, but the output was full of errors. My goal was to help him review and clean it up while also exploring different ways to validate the findings.

---

###  Hints

- AI-generated reports are only as good as the prompts used.
- Review everything carefully — not just for technical accuracy, but also for logic, formatting, and compliance.

---

##  Solution

###  The Unintended Way – Brute-Force Combo Discovery

Instead of only reviewing the report findings manually, I tried a different approach: brute-forcing the `/check` endpoint via Burp Suite.

####  Method:

- Used **ClusterBomb** in **Burp Intruder** with **9 payload positions** — each had values `0` and `1`.
- Targeted the `/check` endpoint with a POST request.
- Compared response lengths to identify valid versus invalid combinations.

####  Invalid Response

If the combination was wrong, the response body would look like this (length ~274 or 278):

```json
{"error":"FAILURE"}
```

####  Correct Payload

Eventually, I found the right combo that passed the validation:

```http
POST /check HTTP/2
Host: hhc23-reportinator-dot-holidayhack2023.ue.r.appspot.com
Content-Type: application/x-www-form-urlencoded

input-1=0&input-2=0&input-3=1&input-4=0&input-5=0&input-6=1&input-7=0&input-8=0&input-9=1
```

Response:

```json
{"hash":"7fe1681630ab878a61b03421b14a0e34fe726cb726e860672bc6e3a6e4d51e0f","resourceId":"81e70c44-aed9-48d2-a48a-40d69be977f3"}
```

This shortcut allowed me to bypass the manual report validation — but I still reviewed the findings afterward to understand why certain answers were incorrect.

---

###  The Intended Way – Spot the Errors in the Report

ChatNPT made several mistakes in the pentest findings:

---

####  Finding 3: Java Deserialization RCE

- It references **TCP port 88555**, which is invalid — max port number is 65535.
- Cites **NIST SP 800-53 SC-28**, which applies to **data at rest** — irrelevant here.

---

####  Finding 6: Stored Cross-Site Scripting (XSS)

- Mentions an HTTP **“SEND” method**, which doesn't exist.
- Calls XSS a **“language”**, which makes no sense — XSS is a vulnerability type.
- A better XSS payload would be something like:

```html
<script>alert(1)</script>
```

---

####  Finding 9: Internal IP Address Disclosure

- Refers to an **“HTTP 7.4.33 request”**, which isn’t a real HTTP version (looks more like a PHP version).
- Recommends modifying the `Location` header to show the **Windows registration key** — that's not only wrong but also a terrible idea.  
  A secure implementation would use a **relative redirect path**.

---

###  Result

Whether using the brute-force trick or reviewing the report directly, the end result was the same — the invalid findings were rejected, and the correct ones were confirmed. Noel’s report was cleaned up and finalized.

---

###  Lesson Learned

It’s easy to let AI tools do the writing — but if you don’t check the output, you could be submitting something full of nonsense. Also, sometimes there’s more than one way to solve a challenge, and knowing how to script or automate testing can help speed up the process.

Brute-force isn’t elegant… but it works.

