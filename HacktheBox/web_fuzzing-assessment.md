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

.php                    [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 4861ms]  <----------
.php7                   [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 4863ms]  <----------
.phps                   [Status: 403, Size: 287, Words: 20, Lines: 10, Duration: 4864ms]  <---------- 
:: Progress: [41/41] :: Job [1/1] :: 8 req/sec :: Duration: [0:00:04] :: Errors: 0 ::
```







