# Attacking Windows Credential Manager
Windows stores saved credentials (e.g., domain logins, service access) in the Credential Manager, backed by encrypted vaults protected with DPAPI. 
You can enumerate saved credentials for the current user using:

## Initial Access

Access to the target system (`10.129.234.171`) was obtained via Remote Desktop Protocol (RDP) using valid credentials:

- **Username:** `sadams`
- **Password:** `totally2brow2harmon@`
- **Hostname:** `ACADEMY-PWATTCK-CREDDEV01`

Authentication was performed using Remmina, providing a full desktop environment under the user context `sadams`.

##  Enumeration

After successfully logging in via RDP as the user `sadams`, basic enumeration was performed to confirm the user context and identify any stored credentials or opportunities for privilege escalation.

###  Confirmed User Context

<img width="791" height="509" alt="image" src="https://github.com/user-attachments/assets/95afaec4-20ca-4c22-8cec-7a1e4f712c75" />

### Stored Credentials in Credential Manager

The following command was run to check for any saved credentials:

`cmdkey /list`

<img width="499" height="180" alt="image" src="https://github.com/user-attachments/assets/63aecfce-05be-42e2-8aef-579933191a02" />

The presence of a Domain Password for SRV01\mcharles indicates that this account had previously authenticated on the system, and its credentials were saved. 
This is a strong indicator of lateral movement potential or escalation.


##  Credential Access via Mimikatz
Since the stored credential for `SRV01\mcharles` could not be extracted directly through user-level tools, 
Mimikatz was brought onto the target machine to dump credentials from memory.

### Transferring Mimikatz to the Target

The 64-bit version of `mimikatz.exe` was hosted on the attacker's machine using a simple Python HTTP server:

```sudo python3 -m http.server 8000```

<img width="1012" height="252" alt="image" src="https://github.com/user-attachments/assets/18f9e120-272e-4f74-be9d-ea32e53cbe6c" />

On the target system, Mimikatz was downloaded to a user-writable directory:

<img width="777" height="221" alt="image" src="https://github.com/user-attachments/assets/cd3c5a1e-13ec-4179-9367-beacbf94a1d8" />

###  UAC Bypass via msconfig GUI

Initial attempts to run Mimikatz failed with access errors due to lack of administrative privileges. Trying
to run the Administrator Command Prompt also required a password that was not present: 

<img width="616" height="559" alt="image" src="https://github.com/user-attachments/assets/51553eca-88f7-4568-abc6-a1e65ee37daa" />

To gain an elevated shell, a **User Account Control (UAC) bypass** was performed using the built-in `msconfig.exe` tool.

From the RDP session:

1. `msconfig.exe` was launched via the Windows search bar.
2. In the **Tools** tab, **Command Prompt** was selected.
3. The **"Launch"** button was clicked, which opened a high-integrity (Administrator) command prompt.

<img width="710" height="490" alt="image" src="https://github.com/user-attachments/assets/d653fee1-9d4e-405a-8a3e-80991fd3882e" />

This provided an **elevated shell** without triggering a UAC prompt, allowing `mimikatz.exe` to be executed with full privileges.

## Credential Extraction (LSASS Dump)

With Mimikatz running under an elevated shell, LSASS memory was successfully accessed to extract stored credentials.

The following commands were run to execute and find credentials within Mimikatz:

<img width="883" height="607" alt="image" src="https://github.com/user-attachments/assets/a5b916c9-88a0-4df3-8541-f93c9acf8863" />

<img width="729" height="378" alt="image" src="https://github.com/user-attachments/assets/7b2655c1-80b0-404a-8e1e-96e54b244649" />


<img width="945" height="115" alt="image" src="https://github.com/user-attachments/assets/827f039c-8305-4be9-b34a-16a473942803" />

## Final Summary

These steps demonstrate how Windows Credential Manager can retain domain credentials in memory and how a 
low-privileged user with access to GUI tools and UAC misconfigurations can escalate and extract sensitive authentication data.







