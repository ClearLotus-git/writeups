# Recover the Tolkien Ring: Suricata Regatta  
**SANS Holiday Hack Challenge 2022 – KringleCon V: Golden Rings**  
**Difficulty:** 🎄🎄🎄

## Overview  
In this challenge, I was tasked with writing custom Suricata rules to detect indicators of Dridex malware activity based on DNS, HTTP, and TLS traffic patterns. The rules were to be added to the `suricata.rules` file and verified using the built-in `./rule_checker` tool.

---

## Existing Rules Review  
The provided `suricata.rules` file included several pre-written examples demonstrating various detection patterns across HTTP, DNS, IP, and TLS traffic. These were useful for syntax reference and understanding rule structure.

Examples included:
- HTTP content-type mismatch (possible ELF binaries)
- Spamhaus DROP list IP monitoring
- DNS queries to suspicious domains
- TLS misbehavior (no TLS after STARTTLS)
- IPv4 checksum anomalies

---

## Objective-Specific Rule Requirements  
The challenge required four custom Suricata alert rules to detect the following:

1. **DNS lookup for `adv.epostoday.uk`**  
2. **Any HTTP traffic to IP `192.185.57.242`**  
3. **TLS certificate subject containing `heardbellith.Icanwepeh.nagoya`**  
4. **HTTP response body using the JavaScript function `let byteCharacters = atob` (base64 decoding logic)**

---

## Final Suricata Rules Written  
```suricata
alert dns any any -> any any (
  msg:"Known bad DNS lookup, possible Dridex infection"; 
  dns.query; content:"adv.epostoday.uk"; nocase; 
  sid:1; rev:1;
)

alert http any any <> 192.185.57.242 any (
  msg:"Investigate suspicious connections, possible Dridex infection"; 
  sid:2; rev:1;
)

alert tls any any <> any any (
  msg:"Investigate bad certificates, possible Dridex infection"; 
  tls.cert_subject; content:"CN=heardbellith.Icanwepeh.nagoya"; 
  isdataat:!1,relative; 
  sid:3; rev:1;
)

alert http any any <> any any (
  msg:"Suspicious JavaScript function, possible Dridex infection"; 
  http.accept_enc; http.response_body; 
  content:"let byteCharacters = atob"; 
  sid:4; rev:1;
)
```

---

## Rule Verification  
To validate the rules, I appended them to `suricata.rules` and ran the provided `./rule_checker`:

```bash
echo '...rule...' >> suricata.rules
./rule_checker
```

### Output Summary:
```
6/1/2023 -- 12:37:19 - <Notice> - This is Suricata version 6.0.8 RELEASE running in USER mode
...
First rule looks good!
Second rule looks good!
Third rule looks good!
Fourth rule looks good! You've done it - thank you!
```

---

## Conclusion  
All four Suricata rules successfully matched their respective malicious indicators and were verified by the rule checker. This challenge provided hands-on experience with crafting IDS signatures to detect malware behaviors at the network level using Suricata’s rule syntax.
