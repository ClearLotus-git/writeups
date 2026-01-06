# Skills Assessment for Web Fuzzing

### Notes 
Apply the multitude of tools and techniques showcased throughout this module.

### Task:
Find the flag.

---

```
ffuf -u http://83.136.251.11:40851/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -recursion -e .php,.txt,.html -ac

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://83.136.251.59:33679/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Extensions       : .php .txt .html 
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

admin                   [Status: 301, Size: 323, Words: 20, Lines: 10, Duration: 16ms]   <-------- here
[INFO] Adding a new job to the queue: http://83.136.251.59:33679/admin/FUZZ

[INFO] Starting queued job on target: http://83.136.251.59:33679/admin/FUZZ

index.php               [Status: 200, Size: 13, Words: 2, Lines: 1, Duration: 16ms]
index.php               [Status: 200, Size: 13, Words: 2, Lines: 1, Duration: 17ms]
panel.php               [Status: 200, Size: 58, Words: 8, Lines: 1, Duration: 18ms]  <------- here 
:: Prgress: [18892/18892] :: Job [2/2] :: 2469 req/sec :: Duration: [0:00:07] :: Errors: 0 ::
```



```
curl http://83.136.251.11:40851/admin/panel.php
Invalid parameter, please ensure accessID is set correctly
```

Fuzz the accessID parameter value using ffuf and the common.txt wordlist, and filter the words:

```
ffuf -u http://83.136.251.11:40851/admin/panel.php?accessID=FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -fw 8

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://83.136.251.11:40851/admin/panel.php?accessID=FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 8
________________________________________________

getaccess               [Status: 200, Size: 68, Words: 12, Lines: 1, Duration: 16ms]
:: Progress: [4723/4723] :: Job [1/1] :: 232 req/sec :: Duration: [0:00:05] :: Errors: 0 ::
```

```
curl http://83.136.251.11:40851/admin/panel.php?accessID=getaccess
Head on over to the fuzzing_fun.htb vhost for some more fuzzing fun!
```

Add to etc/hosts file: 
```
echo "STMIP fuzzing_fun.htb" | sudo tee -a /etc/hosts
```

```
curl http://fuzzing_fun.htb:40851
Welcome to fuzzing_fun.htb!
Your next starting point is in the godeep folder - but it might be on this vhost, it might not, who knows...
```

```
ffuf -u http://fuzzing_fun.htb:40851 -w /usr/share/seclists/Discovery/Web-Content/common.txt -H 'Host: FUZZ.fuzzing_fun.htb:33679' -ac

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://fuzzing_fun.htb:40851
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Header           : Host: FUZZ.fuzzing_fun.htb:33679
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

hidden                  [Status: 200, Size: 45, Words: 8, Lines: 1, Duration: 16ms]
:: Progress: [4723/4723] :: Job [1/1] :: 2040 req/sec :: Duration: [0:00:05] :: Errors: 0 ::
```


Add again to etc/hosts:

```
echo "STMIP hidden.fuzzing_fun.htb" | sudo tee -a /etc/hosts
```

```

ffuf -u http://hidden.fuzzing_fun.htb:40851/godeep/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -recursion

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev

________________________________________________

 :: Method           : GET
 :: URL              : http://hidden.fuzzing_fun.htb:33679/godeep/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

<SNIP>

[INFO] Adding a new job to the queue: http://hidden.fuzzing_fun.htb:33679/godeep/stoneedge/bbclone/typo3/FUZZ

[INFO] Starting queued job on target: http://hidden.fuzzing_fun.htb:33679/godeep/stoneedge/bbclone/typo3/FUZZ

.htpasswd               [Status: 403, Size: 290, Words: 20, Lines: 10, Duration: 16ms]
.hta                    [Status: 403, Size: 290, Words: 20, Lines: 10, Duration: 16ms]
.htaccess               [Status: 403, Size: 290, Words: 20, Lines: 10, Duration: 17ms]
index.php               [Status: 200, Size: 23, Words: 1, Lines: 1, Duration: 17ms]
:: Progress: [4723/4723] :: Job [4/4] :: 2469 req/sec :: Duration: [0:00:02] :: Errors: 0 ::
```

```
curl http://hidden.fuzzing_fun.htb:40851/godeep/stoneedge/bbclone/typo3/index.php
HTB{wXXXXXXXXXXXXs}
```
















