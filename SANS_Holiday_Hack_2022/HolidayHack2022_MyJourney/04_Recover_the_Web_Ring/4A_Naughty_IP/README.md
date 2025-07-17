# Recover the Web Ring: Naughty IP  
**SANS Holiday Hack Challenge 2022 – KringleCon V: Golden Rings**  
**Difficulty:** 🎄

## Overview  
This challenge required identifying the most suspicious (or "naughty") IP address communicating with a web server. Provided with logs from a web environment, I analyzed connection patterns to determine which host stood out as the top talker — indicating potential malicious activity.

---

## Steps Performed

### 1. Analyze the Web Error Logs  
The `weberror.log` file contained numerous entries with IP addresses. I focused on identifying the IP address that appeared the most, using the following shell command:

```bash
for i in $(grep -E "^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" weberror.log | cut -d " " -f 1 | sort | uniq); do 
  a=$(grep $i weberror.log | wc -l); 
  echo $a $i; 
done | sort -nr
```

---

### 2. Identify the Top Talker  
This analysis produced a list of IPs sorted by frequency. The top IP address — making **1384 requests** — was:

```
18.222.86.32
```

This IP had significantly more requests than the next highest, clearly identifying it as the most active (and likely naughty) host.

---

## Outcome  
Using simple command-line log analysis, I isolated the IP generating the most traffic toward the victim server (`10.12.42.16`), fulfilling the objective.

**Final Answer:**  
```
18.222.86.32
```
