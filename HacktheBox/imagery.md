# Imagery Seasonal HTB

## Enumeration 

```
┌──(kali㉿kali)-[~]
└─$ nmap -A 10.10.11.88   
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-28 12:39 EDT
Nmap scan report for 10.10.11.88
Host is up (0.036s latency).
Not shown: 997 closed tcp ports (reset)
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 9.7p1 Ubuntu 7ubuntu4.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 35:94:fb:70:36:1a:26:3c:a8:3c:5a:5a:e4:fb:8c:18 (ECDSA)
|_  256 c2:52:7c:42:61:ce:97:9d:12:d5:01:1c:ba:68:0f:fa (ED25519)
8000/tcp open  http        Werkzeug httpd 3.1.3 (Python 3.12.7)
|_http-title: Image Gallery
|_http-server-header: Werkzeug/3.1.3 Python/3.12.7
8080/tcp open  http-proxy?
Device type: general purpose|router
Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 4.15 - 5.19, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 21/tcp)
HOP RTT      ADDRESS
1   32.92 ms 10.10.14.1
2   33.41 ms 10.10.11.88

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 101.88 seconds

```
Werkzeug httpd 3.1.3

<img width="1834" height="897" alt="image" src="https://github.com/user-attachments/assets/fe7f23c5-3da0-4128-8e24-88766ebacfe9" />


Registering a user: 

<img width="797" height="466" alt="image" src="https://github.com/user-attachments/assets/7476d4f7-24e6-4e7f-8372-3cbb999b681a" />


Login to user:

<img width="1195" height="803" alt="image" src="https://github.com/user-attachments/assets/1d274c3f-7e8a-4d6e-9f53-0642e1d5447c" />


Upload page: 

<img width="513" height="636" alt="image" src="https://github.com/user-attachments/assets/b993e120-f46c-44a4-8b52-d850b581f1ef" />


Stealing Cookie for Admin: 














