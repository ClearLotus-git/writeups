Intro to Nmap

Difficulty: 1/5

Objective: Meet Eric in the hotel parking lot for Nmap know-how and scanning secrets. Help him connect to the wardriving rig on his motorcycle!

Task: 

<img width="462" height="330" alt="image" src="https://github.com/user-attachments/assets/f9111111-e2a1-4f79-a80c-08a0bd3d22c9" />


```
Welcome to the Intro to Nmap terminal!  We will learn some Nmap basics by running commands to answer the questions asked, which will guide us in finding and connecting to the wardriving rig's service. 
Run the command "hint" to receive a hint.


───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Type [y]es to begin: yes
```

```
1) When run without any options, nmap performs a TCP port scan of the top 1000 ports. Run a default nmap scan of 127.0.12.25 and see which port is open.



───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
elf@9fb63786d95e:~$ nmap 127.0.12.25
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-11 21:03 UTC
Nmap scan report for 127.0.12.25
Host is up (0.000066s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 0.04 seconds
```

```
2) Sometimes the top 1000 ports are not enough. Run an nmap scan of all TCP ports on 127.0.12.25 and see which port is open.



───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
elf@9fb63786d95e:~$ nmap -sT -p- 127.0.12.25
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-11 21:05 UTC
Nmap scan report for 127.0.12.25
Host is up (0.000061s latency).
Not shown: 65534 closed ports
PORT      STATE SERVICE
24601/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 1.71 seconds
```

```
3) Nmap can also scan a range of IP addresses.  Scan the range 127.0.12.20 - 127.0.12.28 and see which has a port open.



───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
elf@9fb63786d95e:~$ nmap 127.0.12.20-28
^SNIP^
----or----
elf@9fb63786d95e:~$ nmap -Pn --open 127.0.12.20-28
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-11 21:08 UTC
Nmap scan report for 127.0.12.25
Host is up (0.00019s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE
8080/tcp open  http-proxy

Nmap done: 9 IP addresses (9 hosts up) scanned in 0.46 seconds
```

```
4) Nmap has a version detection engine, to help determine what services are running on a given port. What service is running on 127.0.12.25 TCP port 8080?



───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
elf@9fb63786d95e:~$ nmap -sV 127.0.12.25 -p 8080
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-11 21:10 UTC
Nmap scan report for 127.0.12.25
Host is up (0.000063s latency).

PORT     STATE SERVICE VERSION
8080/tcp open  http    SimpleHTTPServer 0.6 (Python 3.10.12)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.63 seconds
```

```
5) Sometimes you just want to interact with a port, which is a perfect job for Ncat!  Use the ncat tool to connect to TCP port 24601 on 127.0.12.25 and view the banner returned.



───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
elf@9fb63786d95e:~$ ncat 127.0.12.25 24601
Welcome to the WarDriver 9000!
Terminated
```

```
Congratulations, you finished the Intro to Nmap and found the wardriving rig's service!
Type "exit" to close...


───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
elf@9fb63786d95e:~$ ncat 127.0.12.25 24601
Welcome to the WarDriver 9000!
Terminated
elf@9fb63786d95e:~$ 
```













