# Recover the Tolkien Ring: Wireshark Practice  
**SANS Holiday Hack Challenge 2022 – KringleCon V: Golden Rings**  
**Difficulty:** 🎄

## Overview  
In this challenge, I analyzed a suspicious network capture (PCAP) file using Wireshark to uncover signs of malicious activity. The goal was to inspect HTTP traffic, extract files, investigate TLS certificates, and determine whether the host was compromised.

---

## Analysis Summary

###  PCAP Validation  
I used both `suspicious.pcap` (downloaded manually) and `pcap_challenge.pcap` (from the terminal). A hash comparison confirmed both files were identical (`md5: f0450df7d1bf6e695f80a61259083307`).

---

###  Exported Object Types  
Using Wireshark’s **File > Export Objects > HTTP** feature, I discovered that only HTTP objects were available for extraction.

---

###  Largest Exported File  
Among the exported objects, the file with the largest size was `app.php`. Two versions of this file appeared with different sizes, one containing an embedded base64 payload.

---

###  Start Packet for app.php  
The download of `app.php` began at **packet number 687**, as shown in the export objects list.

---

###  Apache Server IP  
Using `tshark` to inspect packet 687 revealed the Apache server's IP address:  
**192.185.57.242**

```bash
tshark -r pcap_challenge.pcap -T fields -e ip.src "frame.number == 687"
```

---

###  File Dropped on Victim  
Analysis of the JavaScript embedded in `app.php` revealed that the malicious payload saved a ZIP file named:  
**Ref_Sept24-2020.zip**

```js
saveAs(blob1, 'Ref_Sept24-2020.zip');
```

Inside this archive was `Ref_Sept24-2020.scr`, identified by VirusTotal as **Dridex** malware.

---

###  Malicious TLS Certificates  
I parsed the packet capture using `tshark` and extracted country codes from TLS certificates:

```bash
tshark -r pcap_challenge.pcap -V | grep "id-at-countryName=" | cut -d = -f 2 | cut -d ")" -f1 | sort | uniq
```

Suspicious certificates were registered to:
- **Ireland (IE)**
- **Israel (IL)**
- **South Sudan (SS)**

The United States was excluded as it was considered a default background domain.

---

###  Host Infection Confirmation  
The host attempted to connect to `adv.epostoday.uk` after downloading the malicious content. This domain is a known **Dridex Command & Control** endpoint, confirming that the host was infected.

```bash
tshark -r pcap_challenge.pcap -V "frame.number > 687 && ip.src == 10.9.24.101 && dns" | grep "type A"
```

Other DNS queries were routine Microsoft services, but the presence of `adv.epostoday.uk` is a confirmed Indicator of Compromise (IOC).

---

## Conclusion  
This analysis confirms a Dridex malware infection. The attacker delivered a ZIP file via a disguised `app.php` download, which was embedded with a base64 payload. The host's follow-up connection to a known Dridex domain further verified the compromise. Exporting objects, inspecting scripts, and analyzing DNS traffic proved critical in completing this objective.
