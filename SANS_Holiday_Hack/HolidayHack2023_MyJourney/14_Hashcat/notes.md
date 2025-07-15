# OBJECTIVE 15 - Hashcat  


## OBJECTIVE  
Help Eve Snowshoes recover a password using Hashcat by cracking a Kerberos ASREP hash found on the Island of Misfit Toys.

---

## My Approach

This was a classic password-cracking challenge, and Hashcat made it straightforward.

### Step 1: Identify the Hash Type  
After inspecting the `hash.txt` file, I noticed the hash started with:

```
$krb5asrep$23
```

That prefix tells us this is a **Kerberos ASREP hash**, which maps to **Hashcat mode `18200`**.

### Step 2: Prepare the Command  
We’re also given a `password_list.txt` wordlist, so this is a simple dictionary attack.

The challenge recommends using low-resource options in Hashcat:

```bash
-w 1 -u 1 --kernel-accel 1 --kernel-loops 1
```

So the full command becomes:

```bash
hashcat -a 0 -w 1 -u 1 --kernel-accel 1 --kernel-loops 1 -m 18200 hash.txt password_list.txt --force
```

### Step 3: Crack the Hash  
I ran the command, and after a short while, Hashcat found the password. The cracked password is stored in:

```
~/.hashcat/hashcat.potfile
```

Reading that file revealed the password:

```
IluvC4ndyC4nes!
```

I then submitted it using the `/bin/runtoanswer` utility to complete the challenge.

---

## Result

Hashcat successfully cracked the Kerberos ASREP hash using the provided wordlist.  
**Recovered password:** `IluvC4ndyC4nes!`

---

## Lessons Learned

This was a quick but valuable exercise in Kerberos hash cracking. Knowing how to identify the hash type and match it to Hashcat’s mode system is crucial. Also, using system-friendly flags is helpful when working on limited resources or in live environments.

