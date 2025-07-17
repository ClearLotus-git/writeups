# Recover the Web Ring: Credential Mining  
**SANS Holiday Hack Challenge 2022 – KringleCon V: Golden Rings**  
**Difficulty:** 🎄

## Overview  
This challenge involved identifying the first username used in a brute force login attempt against a web application. Provided with a packet capture file (`victim.pcap`), I needed to analyze HTTP POST traffic targeting the login endpoint.

---

## Steps Performed

### 1. Focus on Attacker's IP  
From the previous challenge, I knew the attacker's IP address was:

```
18.222.86.32
```

The login endpoint was located at `/login.html`.

---

### 2. Filter and Extract POST Data  
Using `tshark`, I filtered for HTTP POST requests to `/login.html` originating from the attacker IP:

```bash
tshark -r victim.pcap -T fields -e http.file_data \
  "ip.src==18.222.86.32 && http.request.uri contains login.html && http.request.method==POST" | head -n 1
```

This produced the first login attempt payload:

```
username=alice&password=philip
```

---

## Outcome  
The first brute-force login attempt used the username **alice**.

**Final Answer:**  
```
alice
```
