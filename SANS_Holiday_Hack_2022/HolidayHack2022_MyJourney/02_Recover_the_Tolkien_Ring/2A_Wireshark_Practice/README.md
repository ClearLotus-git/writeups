
# OBJECTIVE 2 - Recover the Tolkien Ring  
**Difficulty:** 🎄

---

## Challenge  
Analyze a suspicious PCAP file using Wireshark tools provided in the Tolkien Ring terminal. Investigate HTTP traffic, extract potential malware, and answer key questions related to attacker infrastructure and infection indicators.

---

## Steps I Took  

**Step 1:**  
Accessed the Wireshark Phishing terminal in the Tolkien Ring area and reviewed the instructions to begin the challenge.

**Step 2:**  
Downloaded the PCAP file from the terminal and verified that `suspicious.pcap` and `pcap_challenge.pcap` had matching MD5 hashes (`f0450df7d1bf6e695f80a61259083307`).

**Step 3:**  
Used Wireshark’s “Export Objects > HTTP” feature to examine downloadable content. Identified `app.php` as the largest file, with two versions containing different payloads. Detected embedded Base64 data in the larger one.

**Step 4:**  
Located the packet where `app.php` begins using the Export Objects window — packet number `687`.

**Step 5:**  
Determined the Apache server IP by isolating packet 687 with `tshark`, revealing `192.185.57.242` as the source IP.

**Step 6:**  
Decoded and reviewed the JavaScript payload within `app.php`. Confirmed it downloads `Ref_Sept24-2020.zip`, which contains a `.scr` file flagged by VirusTotal as Dridex malware.

**Step 7:**  
Investigated TLS certificates in the capture using `tshark` and found multiple suspicious certificates registered to `Ireland`, `Israel`, and `South Sudan`.

**Step 8:**  
Confirmed the host was infected by identifying DNS requests to `adv.epostoday.uk`, a known Dridex IOC.

---

## Result  
Successfully analyzed the malicious traffic within the PCAP. Confirmed malware delivery, suspicious TLS certificate origins, and outbound beaconing to a known Dridex command-and-control domain. Marked the host as infected and completed the objective.



