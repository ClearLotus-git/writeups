Retro Revovery

Difficulty: 2/5

Objective:

Join Mark in the retro shop. Analyze his disk image for a blast from the retro past and recover some classic treasures.

Task:

<img width="1350" height="583" alt="image" src="https://github.com/user-attachments/assets/250a85a4-d9f0-4002-9ef5-ffb2836159f1" />

<img width="439" height="321" alt="image" src="https://github.com/user-attachments/assets/fb62ce24-1cb0-4bfa-b9a6-d70be0a02a25" />

Obtain Old floppy disk (This feels like an MMORPG but work at the same time...)

<img width="713" height="188" alt="image" src="https://github.com/user-attachments/assets/51b40330-510c-497d-b91f-3a2464eb749f" />

I had to use the hint because I wasnt sure where this was going..
```
hint:

I miss old school games. I wonder if there is anything on this disk? I remember, when kids would accidentlly delete things.......... it wasn't to hard to recover files. I wonder if you can still mount these disks?
****
```

```
.\strings64.exe "C:\Users\Nick\Downloads\floppy (1).img" > .\floppy-strings.txt
```


```
notepad floppy-strings.txt
```
<img width="680" height="551" alt="image" src="https://github.com/user-attachments/assets/714006a6-9b23-4707-9b7d-892a7af9a9d6" />

Line 211

<img width="765" height="331" alt="image" src="https://github.com/user-attachments/assets/4be658f8-a3e0-4f78-8d52-98eaab887e7d" />

Using cyberchef

<img width="1544" height="641" alt="image" src="https://github.com/user-attachments/assets/b041bf29-701b-457c-a35c-924ee954559e" />


Alternative method: 

Using TestDisk & PhotoRec 7.3-WIP, Data Recovery

```
testdisk-7.3-WIP> .\testdisk_win.exe "C:\Users\Nick\Downloads\floppy (1).img"
```

In the new opened window press enter

<img width="694" height="500" alt="image" src="https://github.com/user-attachments/assets/be3bf1d7-1792-40af-81bd-b6217ef3adb5" />

Enter again on `none`

<img width="605" height="485" alt="image" src="https://github.com/user-attachments/assets/104ef2bb-b0ce-47a4-b227-0e605eed923d" />

Enter again

<img width="650" height="498" alt="image" src="https://github.com/user-attachments/assets/9a85d3c7-fba4-447f-8498-4d6befa6d781" />

Enter on `list`

<img width="684" height="500" alt="image" src="https://github.com/user-attachments/assets/be6d262d-1928-40bd-a166-8b1ac6edd21e" />

Big `C` to copy the file

<img width="728" height="505" alt="image" src="https://github.com/user-attachments/assets/8b899d40-d845-40eb-a62a-ddafef66e1a1" />

Big `C` again to copy it to directory

<img width="719" height="505" alt="image" src="https://github.com/user-attachments/assets/28e1c286-cacb-4533-bf26-7cef46a19434" />

Open in notepad and `all_i-want_for_christmas.bas` is recovered to system

<img width="1892" height="769" alt="image" src="https://github.com/user-attachments/assets/b99e7cf9-87b3-4fa1-9a0e-f8fbdfcec256" />












