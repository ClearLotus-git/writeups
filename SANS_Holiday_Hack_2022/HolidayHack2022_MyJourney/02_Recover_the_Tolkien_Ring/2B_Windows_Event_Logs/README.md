# OBJECTIVE 3 - Recover the Tolkien Ring: Windows Event Logs  
**Difficulty:** 🎄🎄

---

## Challenge  
Analyze a PowerShell event log from a Windows system to identify malicious activity. Use event log analysis tools to uncover suspicious behavior, data manipulation, and potential compromise.

---

## Steps I Took  

**Step 1:**  
Accessed the Windows Event Logs terminal in the Tolkien Ring and downloaded the `powershell.evtx` file. Converted the log into a readable format using `evtx_dump.py`, resulting in `powershell.evtx.dump`.

**Step 2:**  
Identified the primary date of malicious activity by counting PowerShell log events per day. Determined the attack occurred on `12/24/2022`.

**Step 3:**  
Searched for commands referencing secrets. Discovered the attacker accessed `recipe_updated.txt` using PowerShell’s `Get-Content` command.

**Step 4:**  
Found the last command that retrieved and altered file contents, storing them in a variable. The final relevant command was:  
`$foo = Get-Content .\Recipe| % {{$_ -replace 'honey', 'fish oil'}}`

**Step 5:**  
Identified the last command that wrote the altered content to a file:  
`$foo | Add-Content -Path 'Recipe'`

**Step 6:**  
Verified that the most commonly targeted file for write actions was `Recipe.txt`.

**Step 7:**  
Searched for deletion commands and confirmed that files were deleted.  
Two entries found:  
- `del .\Recipe.txt`  
- `del .\recipe_updated.txt`

**Step 8:**  
Confirmed that the original file `recipe_updated.txt` was not deleted.

**Step 9:**  
Identified the event ID that captures executed PowerShell commands as `4104`.

**Step 10:**  
Verified that the secret ingredient in the original recipe was compromised via content substitution.

**Step 11:**  
Confirmed the original secret ingredient was `Honey`.

---

## Result  
Successfully parsed the PowerShell event logs to determine the timeline, commands used, and impacted files. Verified the compromise of the secret ingredient and identified malicious activity through Event ID 4104. Completed the Windows Event Logs challenge.
