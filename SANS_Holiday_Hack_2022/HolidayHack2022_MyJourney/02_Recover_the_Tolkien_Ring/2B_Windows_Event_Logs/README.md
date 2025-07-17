# Recover the Tolkien Ring: Windows Event Logs  
**SANS Holiday Hack Challenge 2022 – KringleCon V: Golden Rings**  
**Difficulty:** 🎄🎄

## Overview  
This challenge focused on analyzing a PowerShell event log file (`powershell.evtx`) to investigate suspicious attacker behavior, identify file manipulation, and confirm whether a secret was compromised. The logs were converted into a human-readable format using the `evtx_dump.py` tool from the `python-evtx` package.

---

## Analysis Summary

###  Date of Attack  
The majority of PowerShell activity occurred on **December 24, 2022**.  
This was determined by counting the number of log entries per day:

```bash
for i in $(grep "TimeCreated" powershell.evtx.dump | cut -d '"' -f 2 | cut -d " " -f 1 | sort | uniq); do 
  a=$(grep "$i" powershell.evtx.dump | wc -l) 
  echo -e "$a\t$i" 
done | sort -rn
```

---

###  Compromised File  
The attacker accessed a file named `recipe_updated.txt`, which contained sensitive data. Multiple commands used `Get-Content` to extract information from this file.

---

###  Variable Assignment & Data Manipulation  
The attacker modified the contents of another file, `Recipe`, and stored the results in a variable named `$foo`.  
The last full PowerShell line used for this operation was:

```powershell
$foo = Get-Content .\Recipe| % {$_ -replace 'honey', 'fish oil'}
```

---

###  File Write Operation  
The modified contents stored in `$foo` were written back to a file using:

```powershell
$foo | Add-Content -Path 'Recipe'
```

This command was run multiple times, indicating repeated attempts to overwrite or append to the file.

---

###  File Activity Frequency  
From reviewing the logs, the file **Recipe.txt** appeared most frequently in write operations, suggesting it was the main target for the attacker’s modifications.

---

###  File Deletion Evidence  
Two deletion commands were observed:

```powershell
del .\Recipe.txt
del .\recipe_updated.txt
```

Both files were deleted at some point in the timeline.

---

###  Was the Original File Deleted?  
Despite being accessed and manipulated, the original file (`recipe_updated.txt`) was **not** deleted.

---

###  Event ID Used  
PowerShell commands and script blocks were logged under **Event ID 4104**, which is known for capturing PowerShell execution details.

---

###  Was the Secret Ingredient Compromised?  
Yes. The command below shows that the attacker replaced the word “honey” with “fish oil”:

```powershell
$foo = Get-Content .\Recipe| % {$_ -replace 'honey', 'fish oil'} $foo | Add-Content -Path 'recipe_updated.txt'
```

---

###  What Was the Secret Ingredient?  
The original secret ingredient was **Honey**.

---

## Conclusion  
Through log parsing and analysis, I was able to reconstruct the attacker’s actions: extracting data from `recipe_updated.txt`, altering `Recipe.txt`, and attempting to conceal the tampering by replacing key ingredients. The use of Event ID 4104 was instrumental in capturing these script executions and confirming that the secret was indeed compromised.

## Result  
Successfully parsed the PowerShell event logs to determine the timeline, commands used, and impacted files. Verified the compromise of the secret ingredient and identified malicious activity through Event ID 4104. Completed the Windows Event Logs challenge.
