# Active Directory Lab 

## Introduction

In this lab, I’ll walk you through what it’s like to step into the role of a Domain Administrator for the fictional company Inlanefreight. 
The IT department has opened several work orders, and together we’ll work through them one by one. 
By the end of this session, you’ll have hands-on experience with Active Directory administration tasks such as managing users, groups, and Group Policy.

<img width="1010" height="467" alt="image" src="https://github.com/user-attachments/assets/0aac5ae3-6601-449b-b043-01330b0e1bc2" />

## Tasks
The following tasks need to be completed as part of the lab scenario:

 **Add New Hires into Active Directory**  
   - Create accounts for new employees starting Monday.

 **Remove Inactive User and Computer Objects**  
   - Clean up old accounts identified during the audit.

 **Unlock Adam Masters’ Account**  
   - Resolve the account lockout issue (see trouble-ticket).

 **Create a Security Group and New OU**  
   - Set up a new Security Group for the new-hire analysts.  
   - Create a new OU for the group and their corresponding PCs.

 **Add New-Hire Computers to the Domain**  
   - Join provisioned computers to the domain.  
   - Verify that the objects are placed in the correct OU.

 **Create and Apply a New Group Policy Object (GPO)**  
   - Duplicate an existing GPO in GPMC.  
   - Modify it for Analyst users.

 **Validate DNS Records**  
   - Ensure DNS records exist for the host:  
     `Sharepoint02.inlanefreight.local`

## Lab Environment Setup: Connecting via RDP

### Overview

For this lab, you’ll be working with a domain-joined Windows Server. This machine is preconfigured for you to carry out all of the required administrative tasks. 
To access it, you will connect remotely over RDP (Remote Desktop Protocol) using either Pwnbox or your own virtual machine connected through the VPN.


## Manage Users

### Adding an AD User via the GUI
To add an AD user via the GUI we first need to open Active Directory Users and Computers via the Start Menu folder Administrative Tools.

### Users to Add

Each user should have the following attributes configured:

- **Full Name**
- **Email** (`first-initial.lastname@inlanefreight.local`)
- **Display Name**
- **User must change password at next logon**

---

| Full Name          | Email Address                        | Display Name        | Password Setting                       |
|--------------------|--------------------------------------|---------------------|----------------------------------------|
| Andromeda Cepheus  | a.cepheus@inlanefreight.local        | Andromeda Cepheus   | Must change password at next logon     |
| Orion Starchaser   | o.starchaser@inlanefreight.local     | Orion Starchaser    | Must change password at next logon     |
| Artemis Callisto   | a.callisto@inlanefreight.local       | Artemis Callisto    | Must change password at next logon     |


Right click on "IT" and Select "New" > "User":

<img width="1708" height="722" alt="image" src="https://github.com/user-attachments/assets/5219c6ff-c2d9-429c-9744-8f81462093ea" />

Add the information into the fields:

<img width="547" height="471" alt="image" src="https://github.com/user-attachments/assets/eaab19af-ae0a-4a8d-981a-1049c6b41d0b" />

Set a password of `NewP@ssw0rd123!`and check the box for "User must change password at next login":

 <img width="545" height="476" alt="image" src="https://github.com/user-attachments/assets/934809c3-67c8-470b-91ca-c3eca7d44fbb" />

If all attributes look correct, select "Finish" in the last window:
 
 <img width="546" height="471" alt="image" src="https://github.com/user-attachments/assets/33434757-376a-4b12-bf16-92eca957ee06" />

New User is now shown: 

<img width="1485" height="722" alt="image" src="https://github.com/user-attachments/assets/2a619412-76f6-4824-b556-c74a076e4876" />

Add email address to the user by selecting properties and filling in email address:

<img width="925" height="590" alt="image" src="https://github.com/user-attachments/assets/6ebbd8a7-aaa4-4e36-bed0-86f15337489b" />

<img width="517" height="701" alt="image" src="https://github.com/user-attachments/assets/4e159098-fc92-48a5-ac67-0757ae2f0845" />


> Repeat these steps for the other users

 ### Adding an AD User via Powershell:

 Open PowerShell as an administrator. To ADD a user into Active Directory. If not done already, load the module with the "Import-Module -Name ActiveDirectory" cmdlet. 
 The AD module can be installed via the RSAT feature pack.

 <img width="1054" height="699" alt="image" src="https://github.com/user-attachments/assets/efb01f6b-f43c-43cd-81d0-6bbf5a2d6768" />

Check where new user landed and move from `default Users` to `IT OU`

<img width="998" height="209" alt="image" src="https://github.com/user-attachments/assets/71ceb254-7e2b-4356-9c2b-926c1e13ec9e" />

TIP: If not seeing user inside IT OU click F5 and new user should appear:

<img width="661" height="205" alt="image" src="https://github.com/user-attachments/assets/fecf314d-33af-49c3-9984-e8b349e5ebdd" />

### Adding last AD User

Choose a technique mentioned above to add the last user requested. 


## Removing the users `Mike O'Hare` and `Paul Valencia`

### Removal via Powershell: 

<img width="1072" height="236" alt="image" src="https://github.com/user-attachments/assets/8e2bec90-4306-4e4d-9a62-294363afd0b2" />

### Removal via GUI:

Locate the user by "Right Click" and select "Find":

<img width="917" height="707" alt="image" src="https://github.com/user-attachments/assets/176169b3-ad70-4863-9cb0-5d320f292391" />

Search for the user: 

<img width="651" height="387" alt="image" src="https://github.com/user-attachments/assets/7c2fc351-ad0f-47c2-858b-90d63443320b" />

Right Click user and DELETE:

<img width="645" height="502" alt="image" src="https://github.com/user-attachments/assets/8679ddf2-22d0-4c20-adf1-20c67b398660" />

<img width="471" height="194" alt="image" src="https://github.com/user-attachments/assets/3d4400f6-ee8c-4c84-9e0d-f2d8c6a7a8dd" />


## Unlock Adam Masters' Account

In Powershell: 

```
 Unlock-ADAccount -Identity amasters
 Set-ADAccountPassword -Identity 'amasters' -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "NewP@ssw0rdReset!" -Force)
```

<img width="1058" height="170" alt="image" src="https://github.com/user-attachments/assets/139fb149-de0f-4af5-8711-d0d707e510cd" />

Then Force Password Change setting on the account:

```
Set-ADUser -Identity amasters -ChangePasswordAtLogon $true
```

<img width="799" height="59" alt="image" src="https://github.com/user-attachments/assets/c4b57796-b63c-4f38-a7c1-bf3a2d9129b1" />


## Create a Security Group and New OU

### Set up a new Security Group for the new-hire analysts.

Open PowerShell as administrator, and then create a both a new AD OU and Security Group. 
This will be accomplished with the New-ADOrganizationalUnit and New-ADGroup Cmdlets:

```
PS C:\Windows\system32> New-ADOrganizationalUnit -Name "Security Analysts" -Path "OU=IT,OU=HQ-NYC,OU=Employees,OU=CORP,DC=INLANEFREIGHT,DC=LOCAL"

PS C:\Windows\system32> New-ADGroup -Name "Security Analysts" -SamAccountName analysts -GroupCategory Security -GroupScope Global -DisplayName "Security Analysts"
-Path "OU=Security Analysts,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL" -Description "Members of this group are Security Analysts under the IT OU"
```

<img width="1061" height="85" alt="image" src="https://github.com/user-attachments/assets/7082dd42-466d-42e7-ae6d-d2ff469d7bd8" />


Create a new OU for the group and their corresponding PCs.
Add the three new users to the Group: 

```
Add-ADGroupMember -Identity analysts -Members ACepheus
Add-ADGroupMember -Identity analysts -Members ACallisto
Add-ADGroupMember -Identity analysts -Members OStarchaser
```

<img width="1051" height="255" alt="image" src="https://github.com/user-attachments/assets/1dca371f-00eb-4140-8d6f-5ea6612fd523" />

ERROR appeared because when the first user was created with the New-ADUser Cmdlet, 
the flag -SamAccountName was not specified. 

Using the ADUS MMC right click on INLANEFREIGHT.LOCAL domain and select Find, 
then search for Orion Starchaser:

<img width="1097" height="581" alt="image" src="https://github.com/user-attachments/assets/8c9b575a-0db8-4951-a072-2ca8b7964b7d" />

<img width="656" height="620" alt="image" src="https://github.com/user-attachments/assets/31992b98-5eac-461c-af16-1bcadeb2decd" />

Double click Orion Starchaser, go to the Account tab, and input a username then press enter when finished:

<img width="1109" height="700" alt="image" src="https://github.com/user-attachments/assets/69c32757-6c9e-400b-9d13-1afb7f26b8ca" />

Right Click the Orion user and select "Add to a group..."

<img width="649" height="642" alt="image" src="https://github.com/user-attachments/assets/55cc1983-e641-44c4-8e9f-02e47166f9b4" />

Under Object Types, students need to select Groups:

<img width="630" height="404" alt="image" src="https://github.com/user-attachments/assets/3ed9d227-1c7e-4cd4-9129-a7dac649e8af" />

Enter Security Analysts and press OK: 

<img width="584" height="385" alt="image" src="https://github.com/user-attachments/assets/5f293c0a-409b-4c05-87b7-ed80c6af4c25" />

<img width="486" height="186" alt="image" src="https://github.com/user-attachments/assets/1454cfcd-e838-4579-bdac-5f77bbeb9247" />

## Manage Group Policy Objects

Duplicate the group policy Logon Banner and rename it Security Analysts Control. 
This is best accomplished with an elevated PowerShell and the Copy-GPO Cmdlet:

<img width="1073" height="403" alt="image" src="https://github.com/user-attachments/assets/0d12014a-810d-4de5-a393-3baa727599a6" />

Open `Group Policy Management` to confirm that the GPO was created:

<img width="1915" height="660" alt="image" src="https://github.com/user-attachments/assets/93e3b981-d1f0-4ffa-b2e9-8d975339f51d" />

Link the GPO to the Security Analysts OU:

<img width="1059" height="240" alt="image" src="https://github.com/user-attachments/assets/8acd6fc8-c363-452a-bd9c-efdda759d49b" />

With the link now established, revisit the Group Policy Management dashboard, right clicking on the Security Analysts Control object and selecting Edit:

<img width="1542" height="473" alt="image" src="https://github.com/user-attachments/assets/1381e782-9f41-4988-b83c-b6db01563fe7" />

Go to the following directory:

`User Configuration --> Policies --> Administrative Templates --> System --> Removable Storage Access`:

<img width="993" height="696" alt="image" src="https://github.com/user-attachments/assets/6b0178bb-ee08-4287-99a4-85f6f6ace61c" />

Configure the All Removable Storage classes setting, by right clicking and selecting Edit:

<img width="899" height="571" alt="image" src="https://github.com/user-attachments/assets/859e329c-c37c-4320-8fee-b8079912272b" />

Enable it and click Apply --> OK:

<img width="764" height="283" alt="image" src="https://github.com/user-attachments/assets/abf4e120-ef6c-43c9-8ad3-0769f9e1429e" />

For the computer configuration, navigate the Group Policy Management editor, down into Computer Configuration 
`--> Policies --> Windows Settings --> Security Settings --> Account Policies --> Password Policy`:

<img width="1233" height="652" alt="image" src="https://github.com/user-attachments/assets/9cdebb83-40f6-4930-981b-8771970500f6" />

Right click the Minimum Password Age Properties: 

<img width="858" height="270" alt="image" src="https://github.com/user-attachments/assets/7178fb0d-7e1b-41f9-bacc-e211c1dd0bcf" />

Define the policy setting:

<img width="527" height="635" alt="image" src="https://github.com/user-attachments/assets/775d4c31-1362-48f4-8268-94342a37717b" />

Repeat these steps, configuring the properties for the Password History policy and Enforce password history policies:

<img width="519" height="634" alt="image" src="https://github.com/user-attachments/assets/92a1bc72-887e-40b5-889c-30c0a147bed2" />

<img width="519" height="643" alt="image" src="https://github.com/user-attachments/assets/79542975-5589-47b0-bd18-d9696f1a8548" />

## Adding local machine to the domain


Using the Add-Computer Cmdlet, add the local machine to the domain and then restart it:

<img width="1077" height="688" alt="image" src="https://github.com/user-attachments/assets/5c0d70ce-5f7e-49ec-a41a-0346f73413b0" />

<img width="1280" height="782" alt="image" src="https://github.com/user-attachments/assets/32c48475-b11d-4c77-ae99-c9dc51256cc1" />

## Verify the machine has joined the domain:

```
New Certificate details:
	Common Name: ACADEMY-IAD-W10.INLANEFREIGHT.LOCAL
	Subject:     CN = ACADEMY-IAD-W10.INLANEFREIGHT.LOCAL
	Issuer:      CN = ACADEMY-IAD-W10.INLANEFREIGHT.LOCAL
	Thumbprint:  e3:b4:1a:9d:07:18:0f:53:42:1d:48:6a:5a:e2:27:9c:2d:2d:6c:fe:d4:0c:75:19:31:1f:89:a6:48:a2:8b:66

Old Certificate details:
	Subject:     CN = ACADEMY-IAD-W10
	Issuer:      CN = ACADEMY-IAD-W10
	Thumbprint:  7a:86:c9:7c:d5:d3:b8:03:f2:35:ce:ea:e0:70:c7:39:d4:ed:25:80:81:74:d9:b7:82:19:ce:1b:6c:db:ff:22
```

Open the ADUC MMC, navigate to Computers, and confirm the `ACADEMY-IAD-W10` machine is there:

<img width="763" height="284" alt="image" src="https://github.com/user-attachments/assets/e426dcda-ef6b-436f-8061-8a1360de17fa" />

Right click the `ACADEMY-IAD-W10` machine, select "Move...", and add it to the Security Analysts OU:

<img width="760" height="564" alt="image" src="https://github.com/user-attachments/assets/d7afb605-65e9-4cd3-a608-1a7ebec508da" />

<img width="764" height="280" alt="image" src="https://github.com/user-attachments/assets/bccc940f-2f78-43c3-8adc-7d06a3d5615a" />

An administrator PowerShell can be used to confirm the OU membership:

```
PS C:\Windows\system32> Get-ADComputer -Identity "ACADEMY-IAD-W10" -Properties * | select CN,CanonicalName,IPv4Address

CN              CanonicalName                                                                  IPv4Address
--              -------------                                                                  -----------
ACADEMY-IAD-W10 INLANEFREIGHT.LOCAL/Corp/Employees/HQ-NYC/IT/Security Analysts/ACADEMY-IAD-W10 172.16.6.135
```


















