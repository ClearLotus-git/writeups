<img width="950" height="219" alt="image" src="https://github.com/user-attachments/assets/e02eaf3a-4abe-43ef-b50c-5bcd856c3e46" />




nmap scan

nmap -A 10.129.1.97 -sC -sV -p-

Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-11 20:11 EST
Nmap scan report for panel.pterodactyl.htb (10.129.1.97)
Host is up (0.040s latency).
Not shown: 65210 filtered tcp ports (no-response), 321 filtered tcp ports (admin-prohibited)
PORT     STATE  SERVICE    VERSION
22/tcp   open   ssh        OpenSSH 9.6 (protocol 2.0)
| ssh-hostkey: 
|   256 a3:74:1e:a3:ad:02:14:01:00:e6:ab:b4:18:84:16:e0 (ECDSA)
|_  256 65:c8:33:17:7a:d6:52:3d:63:c3:e4:a9:60:64:2d:cc (ED25519)
80/tcp   open   http       nginx 1.21.5
|_http-title: Pterodactyl
|_http-trane-info: Problem with XML parsing of /evox/about
|_http-server-header: nginx/1.21.5
443/tcp  closed https
8080/tcp closed http-proxy
Aggressive OS guesses: Linux 5.0 - 5.14 (98%), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3) (98%), Linux 4.15 - 5.19 (94%), Linux 2.6.32 - 3.13 (93%), OpenWrt 22.03 (Linux 5.10) (92%), Linux 3.10 - 4.11 (91%), Linux 5.0 (91%), Linux 3.2 - 4.14 (90%), Linux 4.15 (90%), Linux 2.6.32 - 3.10 (90%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops

TRACEROUTE (using port 443/tcp)
HOP RTT      ADDRESS
1   48.43 ms 10.10.14.1
2   48.49 ms panel.pterodactyl.htb (10.129.1.97)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 327.23 seconds



add to /etc/hosts

pterodactyl.htb


ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/big.txt \
-u http://pterodactyl.htb/ \
-H "Host: FUZZ.pterodactyl.htb" -fw

panel.pterodactyl.htb

Exploit = 
https://www.exploit-db.com/exploits/52341


```
curl -I http://panel.pterodactyl.htb

HTTP/1.1 200 OK
Server: nginx/1.21.5
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
X-Powered-By: PHP/8.4.8
Cache-Control: no-cache, private
Date: Thu, 12 Feb 2026 01:00:12 GMT
Set-Cookie: XSRF-TOKEN=eyJpdiI6ImtsQXFUTjFxNDU0Y0tWL3lFcThpbWc9PSIsInZhbHVlIjoiVXlTWk02UWNQVnJpVmphQS9jMU9rcllOUEtnUkhxTXAyZ05NSXFPTlAzbkVPWDhNd253Q2dKU0dCbklYbjZsbzIwdGdjVW9EVzZYSXd3NnF6RjJmR0puNkRNczlsa25YdExtb0hFc1Z6andhdS9qNTBkSUowSkZKZkhKZklZeEwiLCJtYWMiOiJkODg4M2E4MjYzZTYzNTJjYTA1YTM5YmY2ZDIzZTI0MTQ2MTA3ZTUwOGQ0ZjZlNjk1M2RiY2MxODlkZTU1OTRkIiwidGFnIjoiIn0%3D; expires=Thu, 12 Feb 2026 13:00:12 GMT; Max-Age=43200; path=/; samesite=lax
Set-Cookie: pterodactyl_session=eyJpdiI6Im9mYmtoY25SMVdMb0JmaXYycWpXenc9PSIsInZhbHVlIjoiWjBtZXI5MzRDcG5mWUkxN0k1ZUtLRGhiVlNYdjNiM0FBN0ZXckFvbjMwK1VxRTBlb25mNWJGekNXdG5ac0ZQSEEwc1MvSSsrb3ZKb1JJTUlLc2Y5MlRpVXliWGkzczYxQ3JsRCtFcHdnR01YZkk1ekdLZU4vSkZoQllkZnprMFQiLCJtYWMiOiJiNmM1MzgyMGJkMTgyZjM5YTg3YzRiYmVhNWY5YWVmZjZhM2UyMjgzMjQ4ZDAwYjIxYmQ5NTU1NWI4ZDBjYzg3IiwidGFnIjoiIn0%3D; expires=Thu, 12 Feb 2026 13:00:12 GMT; Max-Age=43200; path=/; httponly; samesite=lax
```

curl -i http://panel.pterodactyl.htb/.env.backup
curl -i http://panel.pterodactyl.htb/.env.save



CVE-2025-49132 - PHP PEAR Remote Code Execution

Database credential extraction from Laravel configuration

CVE-2025-6018 - PAM environment variable injection

CVE-2025-6019 - UDisks2 XFS filesystem privilege escalation




nano /etc/hosts 

<TARGET_IP> pterodactyl.htb panel.pterodactyl.htb


curl -i http://pterodactyl.htb/

HTTP/1.1 200 OK
Server: nginx/1.21.5
Date: Thu, 12 Feb 2026 01:15:03 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
X-Powered-By: PHP/8.4.8


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Minecraft Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="global.css">
</head>

<body class="body">
    <header style="position: relative; text-align: center;">
        <img alt="Header Image" src="Public/Header.png" style="width: 100%; height: auto; max-height: 25rem; object-fit: cover; display: block;" />
        <h1 class="title">MonitorLand</h1>
        <hr class="separator">
    </header>
    
    <main>
        <p>
            Join our awesome Minecraft community!
        </p>
        <div class="ip-box" id="server-ip">play.pterodactyl.htb</div>
        <button onclick="copyIP()">Copy Server IP</button>
        <p style="margin-top:2rem;">
            Version: 1.20.x <br>SMP and Vanilla Servers.<br> <a href="/changelog.txt">Changelogs</a>
        </p>
    </main>

    <footer>
        &copy; 2025 MonitorLand. Not affiliated with Mojang.
    </footer>

    <script>
        function copyIP() {
            const ip = document.getElementById('server-ip').innerText;
            const textArea = document.createElement("textarea");
            textArea.value = ip;
            textArea.style.position = "fixed";
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();

            try {
                document.execCommand("copy");
                alert("Server IP copied to clipboard");
            } catch (err) {
                alert("Failed to copy");
            }

            document.body.removeChild(textArea);
        }
    </script>
</body>
</html>


subdomain = play.pterodactyl.htb
add to /etc/hosts 

┌──(kali㉿kali)-[~/pterodactyl]
└─$ curl -i http://play.pterodactyl.htb/

HTTP/1.1 302 Moved Temporarily
Server: nginx/1.21.5
Date: Thu, 12 Feb 2026 01:17:04 GMT
Content-Type: text/html
Content-Length: 145
Connection: keep-alive
Location: http://pterodactyl.htb/

<html>
<head><title>302 Found</title></head>
<body>
<center><h1>302 Found</h1></center>
<hr><center>nginx/1.21.5</center>
</body>
</html>
                                                                                                                    
┌──(kali㉿kali)-[~/pterodactyl]
└─$ 


nmap -sC -sV -p 25565 10.129.1.97            

Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-11 20:18 EST
Nmap scan report for panel.pterodactyl.htb (10.129.1.97)
Host is up (0.035s latency).

PORT      STATE    SERVICE   VERSION
25565/tcp filtered minecraft

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.43 seconds

setup? 

nginx → Laravel (Pterodactyl panel)
Minecraft running internally (Docker)
SSH available for system users

BURP -> capture login get request and see ->> GET /sanctum/csrf-cookie
HTTP/1.1 204 No Content
Set-Cookie: XSRF-TOKEN=...
Set-Cookie: pterodactyl_session=...

BURP -> capture post request and see -> {"user":"test ","password":"test","g-recaptcha-response":""}

Content-Type: application/json
Accept: application/json
X-Requested-With: XMLHttpRequest
This is an AJAX login.

---------------

test post requests 


---------------------

Forgot Password?


Brup capture -> admin@admin.com

curl http://pterodactyl.htb/changelog.txt

MonitorLand - CHANGELOG.txt
======================================

Version 1.20.X

[Added] Main Website Deployment
--------------------------------
- Deployed the primary landing site for MonitorLand.
- Implemented homepage, and link for Minecraft server.
- Integrated site styling and dark-mode as primary.

[Linked] Subdomain Configuration
--------------------------------
- Added DNS and reverse proxy routing for play.pterodactyl.htb.
- Configured NGINX virtual host for subdomain forwarding.

[Installed] Pterodactyl Panel v1.11.10
--------------------------------------
- Installed Pterodactyl Panel.
- Configured environment:
  - PHP with required extensions.
  - MariaDB 11.8.3 backend.

[Enhanced] PHP Capabilities
-------------------------------------
- Enabled PHP-FPM for smoother website handling on all domains.
- Enabled PHP-PEAR for PHP package management.
- Added temporary PHP debugging via phpinfo()


 curl http://pterodactyl.htb/phpinfo.php

 ffuf -u http://pterodactyl.htb/FUZZ -w /usr/share/wordlists/dirb/common.txt



        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://pterodactyl.htb/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.htaccess               [Status: 403, Size: 153, Words: 3, Lines: 8, Duration: 41ms]
.hta                    [Status: 403, Size: 153, Words: 3, Lines: 8, Duration: 42ms]
.htpasswd               [Status: 403, Size: 153, Words: 3, Lines: 8, Duration: 47ms]
                        [Status: 200, Size: 1686, Words: 429, Lines: 55, Duration: 47ms]
index.php               [Status: 200, Size: 1686, Words: 429, Lines: 55, Duration: 36ms]
phpinfo.php             [Status: 200, Size: 73021, Words: 3592, Lines: 828, Duration: 43ms]
:: Progress: [4614/4614] :: Job [1/1] :: 980 req/sec :: Duration: [0:00:04] :: Errors: 0 ::




curl -H "Host: evil.com" http://10.129.1.97

<html>
<head><title>302 Found</title></head>
<body>
<center><h1>302 Found</h1></center>
<hr><center>nginx/1.21.5</center>
</body>
</html>
                                                                                                                    
┌──(kali㉿kali)-[~/pterodactyl]
└─$ curl -v -H "Host: evil.com" http://10.129.1.97

*   Trying 10.129.1.97:80...
* Connected to 10.129.1.97 (10.129.1.97) port 80
* using HTTP/1.x
> GET / HTTP/1.1
> Host: evil.com
> User-Agent: curl/8.15.0
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 302 Moved Temporarily
< Server: nginx/1.21.5
< Date: Thu, 12 Feb 2026 03:56:09 GMT
< Content-Type: text/html
< Content-Length: 145
< Connection: keep-alive
< Location: http://pterodactyl.htb/
< 
<html>
<head><title>302 Found</title></head>
<body>
<center><h1>302 Found</h1></center>
<hr><center>nginx/1.21.5</center>
</body>
</html>
* Connection #0 to host 10.129.1.97 left intact


Searchbar - pterodactyl panel vv1.11.10 exploits

and 
```
curl -i http://panel.pterodactyl.htb/locales/
```

----------------------------------


Exploit : https://github.com/advisories/GHSA-24wv-6c99-f843







