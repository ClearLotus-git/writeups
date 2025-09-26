# Web Fuzzing - Skills Assessment

You are given an online academy's IP address but have no further information about their website. As the first step of conducting a Penetration Test, you are expected to locate all pages and domains linked to their IP to enumerate the IP and domains properly.

Finally, you should do some fuzzing on pages you identify to see if any of them has any parameters that can be interacted with. If you do find active parameters, see if you can retrieve any data from them.

## Objectives: 
- Run a sub-domain/vhost fuzzing scan on '*.academy.htb' for the IP shown above. What are all the sub-domains you can identify? (Only write the sub-domain name)
- Before you run your page fuzzing scan, you should first run an extension fuzzing scan. What are the different extensions accepted by the domains?
- One of the pages you will identify should say 'You don't have access!'. What is the full page URL?
- In the page from the previous question, you should be able to find multiple parameters that are accepted by the page. What are they?
- Try fuzzing the parameters you identified for working values. One of them should return a flag. What is the content of the flag?

---

```
sudo nano /etc/hosts

127.0.0.1	localhost
127.0.1.1	debian12-parrot
94.237.xx.xxx  admin.academy.htb    <------- add to host with ip
# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
127.0.0.1 localhost
127.0.1.1 htb-bpjxaiotgr htb-bpjxaiotgr.htb-cloud.com
```

```
$ ffuf -w /opt/useful/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://94.237.62.138:49630 -H 'Host: FUZZ.academy.htb' -ac 
        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://94.237.62.138:49630
 :: Wordlist         : FUZZ: /opt/useful/seclists/Discovery/DNS/subdomains-top1million-5000.txt
 :: Header           : Host: FUZZ.academy.htb
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

test                    [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 79ms]   <------ 1  ANSWER
archive                 [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 77ms]   <------ 2  ANSWER
faculty                 [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 77ms]   <------ 3  ANSWER 
:: Progress: [4989/4989] :: Job [1/1] :: 516 req/sec :: Duration: [0:00:10] :: Errors: 0 ::
```

---

```
$ sudo bash -c 'echo "94.237.xx.xxx test.academy.htb archive.academy.htb faculty.academy.htb" >> /etc/hosts'
```

`test`
```
$ ffuf -w /opt/useful/seclists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://test.academy.htb:49630/indexFUZZ

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://test.academy.htb:49630/indexFUZZ
 :: Wordlist         : FUZZ: /opt/useful/seclists/Discovery/Web-Content/web-extensions.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.php                    [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 3986ms]   <-----
.phps                   [Status: 403, Size: 284, Words: 20, Lines: 10, Duration: 4996ms] <---------
:: Progress: [41/41] :: Job [1/1] :: 8 req/sec :: Duration: [0:00:05] :: Errors: 0 ::
```

`archive`
```
$ ffuf -w /opt/useful/seclists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://archive.academy.htb:49630/indexFUZZ

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://archive.academy.htb:49630/indexFUZZ
 :: Wordlist         : FUZZ: /opt/useful/seclists/Discovery/Web-Content/web-extensions.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.php                    [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 77ms]  <-----
.phps                   [Status: 403, Size: 287, Words: 20, Lines: 10, Duration: 3690ms]  <---------
:: Progress: [41/41] :: Job [1/1] :: 8 req/sec :: Duration: [0:00:04] :: Errors: 0 ::
```

`faculty`
```
$ ffuf -w /opt/useful/seclists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://faculty.academy.htb:49630/indexFUZZ

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://faculty.academy.htb:49630/indexFUZZ
 :: Wordlist         : FUZZ: /opt/useful/seclists/Discovery/Web-Content/web-extensions.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.php                    [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 4861ms]  <---------- ANSWER
.php7                   [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 4863ms]  <---------- ANSWER
.phps                   [Status: 403, Size: 287, Words: 20, Lines: 10, Duration: 4864ms]  <---------- ANSWER
:: Progress: [41/41] :: Job [1/1] :: 8 req/sec :: Duration: [0:00:04] :: Errors: 0 ::
```

---

```
ffuf -w /opt/useful/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://faculty.academy.htb:49630/FUZZ -recursion -recursion-depth 1 -e .php,.phps,.php7 -fs 287 -mr "You don't have access!" -t 100

    /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://faculty.academy.htb:30511/FUZZ
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt
 :: Extensions       : .php .php .php7 
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Regexp: You don't have access!
 :: Filter           : Response size: 287
________________________________________________

[INFO] Adding a new job to the queue: http://faculty.academy.htb:30511/courses/FUZZ
```

```
 ffuf -w /opt/useful/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://faculty.academy.htb:49630/courses/FUZZ -e .php,.php,.php7 -fs 287 -mr "You don't have access!" -t 100

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://faculty.academy.htb:30511/courses/FUZZ
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt
 :: Extensions       : .php .php .php7 
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Regexp: You don't have access!
 :: Filter           : Response size: 287
________________________________________________

linux-security.php7     [Status: 200, Size: 774, Words: 223, Lines: 53, Duration: 3ms]   <-------- http://faculty.academy.htb:PORT/courses/linux-security.php7
'''

---
$ ffuf -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://faculty.academy.htb:49630/courses/linux-security.php7 -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -fs 774 -t 100

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://faculty.academy.htb:32569/courses/linux-security.php7
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : FUZZ=key
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
 :: Filter           : Response size: 774
________________________________________________

user                    [Status: 200, Size: 780, Words: 223, Lines: 53, Duration: 1ms]   <------- here ANSWER
username                [Status: 200, Size: 781, Words: 223, Lines: 53, Duration: 431ms] <---------- here ANSWER
:: Progress: [2588/2588] :: Job [1/1] :: 286 req/sec :: Duration: [0:00:06] :: Errors: 0 ::
```

---

```
$ ffuf -w /opt/useful/SecLists/Usernames/Names/names.txt:FUZZ -u http://faculty.academy.htb:49630/courses/linux-security.php7 -X POST -d 'username=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded'

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://faculty.academy.htb:31312/courses/linux-security.php7
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Usernames/Names/names.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : username=FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

abbie                   [Status: 200, Size: 781, Words: 223, Lines: 53, Duration: 2ms]
aaliyah                 [Status: 200, Size: 781, Words: 223, Lines: 53, Duration: 2ms]
abahri                  [Status: 200, Size: 781, Words: 223, Lines: 53, Duration: 1ms]
abbi                    [Status: 200, Size: 781, Words: 223, Lines: 53, Duration: 3ms]
 
```

```
$ ffuf -w /opt/useful/seclists/Usernames/Names/names.txt:FUZZ -u http://faculty.academy.htb:49630/courses/linux-security.php7 -X POST -d 'username=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded' -fs 781 -t 100

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.4.1-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://faculty.academy.htb:31312/courses/linux-security.php7
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Usernames/Names/names.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : username=FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
 :: Filter           : Response size: 781
________________________________________________

harry                   [Status: 200, Size: 773, Words: 218, Lines: 53, Duration: 0ms]
:: Progress: [10164/10164] :: Job [1/1] :: 215 req/sec :: Duration: [0:00:24] :: Errors: 0 ::
```

```
└──╼ [★]$ curl -s http://faculty.academy.htb:49630/courses/linux-security.php7 -X POST -d 'username=harry' | grep "HTB{.*}"

<div class='center'><p>HTB{w3b_fuzz1n6_m4573r}</p></div>
```

---

FINISHED


