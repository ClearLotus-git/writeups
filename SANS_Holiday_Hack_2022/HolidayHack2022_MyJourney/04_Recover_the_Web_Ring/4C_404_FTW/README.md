# Recover the Web Ring: 404 FTW  
**SANS Holiday Hack Challenge 2022 – KringleCon V: Golden Rings**  
**Difficulty:** 🎄

## Overview  
This challenge involved analyzing forced browsing behavior — a type of attack where an adversary repeatedly tries to access various URL paths in the hope of discovering unsecured or hidden content. The objective was to identify the first successful (HTTP 200) request following a series of failed (HTTP 404) attempts.

---

## Steps Performed

### 1. Focus on the Attacker's IP  
Using the previously identified malicious IP address:

```
18.222.86.32
```

I examined the `weberror.log` file for HTTP 404 errors followed by a 200 status code, indicating a successful guess.

---

### 2. Extract First Successful Guess  
I used the following command chain to search for the pattern:

```bash
grep "18.222.86.32" weberror.log | grep -B1 "404 -" | grep "200 -"
```

This produced:

```
18.222.86.32 - - [05/Oct/2022 16:47:46] "GET /proc HTTP/1.1" 200 -
18.222.86.32 - - [05/Oct/2022 16:47:47] "GET /maintenance.html HTTP/1.1" 200 -
```

---

## Outcome  
The first successfully accessed URL after multiple failed guesses was:

**Final Answer:**  
```
/proc
```
