# Attacking Thick Client Applications

Perform an analysis of C:\Apps\Restart-OracleService.exe and identify the credentials hidden within its source code. Submit the answer using the format username:password.

---

Navigate to to C:\TOOLS\ProcessMonitor and launch Procmon64: 

<img width="1770" height="715" alt="image" src="https://github.com/user-attachments/assets/55d94f0d-8bea-434a-a239-cb1df1d537b4" />

Copy the Restart-OracleService script from the sysvol share to the Desktop:

<img width="1896" height="798" alt="image" src="https://github.com/user-attachments/assets/f23dd8f3-8842-4cc9-8c5f-a830ef6f552d" />

Run the Restart-OracleService.exe application through command prompt:

```
Microsoft Windows [Version 10.0.17763.1879]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Users\cybervaca>cd Desktop

C:\Users\cybervaca\Desktop>.\Restart-OracleService.exe
```

In procmon filter for restart: 

<img width="1011" height="612" alt="image" src="https://github.com/user-attachments/assets/04baf143-34a7-4320-8211-1a20d2382359" />

The executable creates a temp file in C:\Users\cybervaca\AppData\Local\Temp:

<img width="901" height="227" alt="image" src="https://github.com/user-attachments/assets/58e753c3-9dd4-4987-a1b5-b67fc5e0cf1e" />

Remove permission entries leaving only `cybervaca` , disabling inheritance on the folder and unchecking the boxes for Delete / Delete subfolders and files:

<img width="1250" height="778" alt="image" src="https://github.com/user-attachments/assets/18ee2a83-9d6d-452a-9931-b541ec36586b" />
<img width="484" height="645" alt="image" src="https://github.com/user-attachments/assets/990f8d28-26ae-42e8-82c7-4982d927f38d" />
<img width="994" height="655" alt="image" src="https://github.com/user-attachments/assets/41ba61a7-c3bc-4b4b-8ace-6892d34de81f" />
<img width="958" height="653" alt="image" src="https://github.com/user-attachments/assets/f4e7b751-7a24-4fa7-8c28-5a6281de14b1" />
<img width="1154" height="765" alt="image" src="https://github.com/user-attachments/assets/f1b319ac-1c21-4bf5-8edc-75213ca5d50c" />

Repeat with same permission entries on SYSTEM and Administrators:

<img width="1149" height="756" alt="image" src="https://github.com/user-attachments/assets/437312da-2161-4d78-92c6-3f5fdf1354a8" />
<img width="1151" height="744" alt="image" src="https://github.com/user-attachments/assets/0ecf4501-d339-4ed0-88a0-696ab79933cd" />

All three users shown with special access: 
<img width="968" height="648" alt="image" src="https://github.com/user-attachments/assets/fb577366-3352-4ad2-b1fd-7b5fabba41bc" />

Running the Restart-OracleService.exe application, the creation of a Windows Batch File will appear:

<img width="1398" height="690" alt="image" src="https://github.com/user-attachments/assets/cacdc971-de2a-4926-9828-38dc97bdf9d9" />

Edit the script in Notepad, modifying it to no longer delete the monta.ps1 and oracle.txt files:

<img width="1431" height="716" alt="image" src="https://github.com/user-attachments/assets/5bfb2fb5-13f5-4563-bd59-b65b7193a3a8" />
<img width="1416" height="712" alt="image" src="https://github.com/user-attachments/assets/56cbd76c-da94-434b-aa87-ad00abd417ac" />
<img width="1423" height="714" alt="image" src="https://github.com/user-attachments/assets/6356d60a-7947-49ca-afab-a47e93bd9097" />

Run the script again by double-clicking it. Then confirm that monta.ps1 and oracle.txt files exist in C:\ProgramData:

<img width="1211" height="544" alt="image" src="https://github.com/user-attachments/assets/da875633-4082-47d5-8b02-01fb8cef66d3" />

<img width="1495" height="559" alt="image" src="https://github.com/user-attachments/assets/4654391c-ac03-4620-b788-c8fd8ca21fba" />

Launch PowerShell as administrator and run monta.ps1: 

| (The lab wasn't allowing opening of powershell so changing from remmina to xfreerdp worked for me...) 


```
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Windows\system32> cd C:\Programdata

PS C:\Programdata> cat .\monta.ps1
$salida = $null; $fichero = (Get-Content C:\ProgramData\oracle.txt) ; foreach ($linea in $fichero) {$salida += $linea }; $salida = $salida.Replace(" ",""); [System.IO.File]::WriteAllBytes("c:\programdata\restart-service.exe", [System.Convert]::FromBase64String($salida))

PS C:\Programdata> .\monta.ps1
```

Restart-service.exe, inside of C:\ProgramData and copy it to the Desktop:

<img width="834" height="466" alt="image" src="https://github.com/user-attachments/assets/b5deb191-183e-4874-8b4f-fc83bd9e70c1" />

Open x64dbg as Administrator and select `File`, `Open`, and `select` the restart-service.exe file:

<img width="839" height="350" alt="image" src="https://github.com/user-attachments/assets/327937f0-8b07-4e25-bb3b-86336550d40e" />

The preferences must also be set to break on Exit Breakpoint and saved:

<img width="836" height="596" alt="image" src="https://github.com/user-attachments/assets/ed9f075e-9469-47e1-acd7-5f3e1d8a1256" />

Check the Memory map, looking for Type MAP with Read/Write protection:

<img width="837" height="353" alt="image" src="https://github.com/user-attachments/assets/28ffb285-cc98-4419-a058-e82acf32b896" />

Right click and Follow in Dump. The ASCII header is seen when running the executable:

<img width="841" height="356" alt="image" src="https://github.com/user-attachments/assets/eb7ca78e-6f05-45a5-93b3-3c73f748033f" />

Dump Memory to File, save the memory dump to the Desktop. Drag and drop the memory dump onto de4dot.exe under C:\TOOLS\de4dot\:

<img width="839" height="367" alt="image" src="https://github.com/user-attachments/assets/91ada8d9-6d21-4580-9661-9792a5bf5a9a" />

Drop the cleaned .bin file onto dnSpy, finding the credentials: 

<img width="840" height="359" alt="image" src="https://github.com/user-attachments/assets/2466bde3-6d40-4a48-8267-8d09f308b5d8" />

---


