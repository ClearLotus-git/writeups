# Objective:
Disclaimer:
This writeup is for educational purposes only. The challenge is part of a non-graded lab from the TCM Security Practical Security Analyst (PSAA) course. No answers to certification exams or assessments are shared here. 

Overview:
In this challenge, we analyze a Windows memory dump using Volatility3. The goal is to identify signs of malicious behavior, extract process and network information, 
and examine persistence mechanisms.
Commands will be show below and screenshots will be put into the `/screenshots` folder.

Instructions:
A System Administrator at Earthworm Solutions recently dusted off a memory capture from a Windows workstation that was suspected to have been compromised. Unfortunately, nobody at the company can remember the details of the incident, and they now require someone to investigate the capture for signs of suspicious activity.

Your task is to test out your memory analysis skills by examining the challenge.vmem file and analyze it for anything out of place or indicative of malware.

Tools Used
Volatility3 v2.26.2

windows.info, windows.pslist, windows.cmdline, windows.dlllist, windows.netscan, windows.hashdump.

---

## 1. What was the system time at which the memory dump was captured?
Use windows.info to retrieve the capture time.

`vol -f '/home/lotus/Desktop/volatility_challenge_1./challenge/challenge.vmem' windows.info`

Answer: 2024-10-29 19:18:00+00:00

## 2. What was the major/minor version of the system set to?
This also appears in the windows.info output.

`vol -f '/home/lotus/Desktop/volatility_challenge_1./challenge/challenge.vmem' windows.info`

Answer: 15.19041

## 3. What is the name of the process(es) that appears malicious or out of place?
Cross-reference process names and command-line arguments with known system processes.

`vol -f '/home/lotus/Desktop/volatility_challenge_1./challenge/challenge.vmem' windows.pslist`

` vol -f '/home/lotus/Desktop/volatility_challenge_1./challenge/challenge.vmem' windows.psscan`

Answer: crss.exe

## 4. Which legitimate Windows process is it attempting to obfuscate as?
Think of common Windows services that malware mimics (e.g., svchost, explorer, etc.).

Answer: csrss.exe
...

## 5. How many established network connections did the process have active at the time of capture?
Use windows.netstat or windows.netscan. Filter by the PID of the suspicious process.

`vol -f '/home/lotus/Desktop/volatility_challenge_1./challenge/challenge.vmem' windows.netstat | grep "3076" | grep 
"ESTABLISHED"`

Answer: 3

## 6. Using the PID identified in the previous question, what is the name of its parent process?
Use windows.pslist or windows.pstree to track down the parent-child relationship.

`vol -f '/home/lotus/Desktop/volatility_challenge_1./challenge/challenge.vmem' windows.pstree | grep -A 5 3076`

`vol -f '/home/lotus/Desktop/volatility_challenge_1./challenge/challenge.vmem' windows.pstree | grep -A 5 5676`

`vol -f '/home/lotus/Desktop/volatility_challenge_1./challenge/challenge.vmem' windows.pstree | grep  1560`

Answer: explorer.exe


## 7. What is the full system path of the malicious process executable?
Use windows.dlllist or windows.cmdline to retrieve the path.
`vol -f '/home/lotus/Desktop/volatility_challenge_1./challenge/challenge.vmem' windows.pstree | grep -A 5 5676`

Answer: C:\Windows\System\crss.exe


## 8. What are the SHA-256 hash values of both malicious process executables?
Use filescan, dumpfiles, or windows.dumpfiles to extract executables, then hash them.

`vol -f '/home/lotus/Desktop/volatility_challenge_1./challenge/challenge.vmem' windows.pslist --pid 5676 1560 --dump`

`sha256sum 3076.crss.exe.0x7ff7fe9f0000.dmp`

`sha256sum 5676.crss.exe.0x7ff7fe9f0000.dmp`

(check hashes on virustotal to confirm)

Answer:
629a3c75dfaa0d87c01cf49011671448553b5ead04bb63128cde803d36d518e7, e3e024afec178c1b9d5410c9ddc0810c94c3cb18ec52830d72d8f38a622b2131

## 9. What is the name of the persistent run entry set by the malware?
Use windows.registry.printkey or windows.autoruns to inspect persistence keys.

`vol -f /home/lotus/Desktop/volatility_challenge_1./challenge/challenge.vmem windows.registry.printkey --key "Software\\Microsoft\\Windows\\CurrentVersion\\Run" | grep "crss"`

Answer: :>7;O:    (This took me an hour to notice!!!!!!!!!!!)

