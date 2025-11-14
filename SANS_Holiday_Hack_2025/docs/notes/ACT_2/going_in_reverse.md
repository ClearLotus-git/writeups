Going in Reverse

Difficulty: 2/5

Objective:
Kevin in the Retro Store needs help rewinding tech and going in reverse. Extract the flag and enter it here.

Task:

<img width="582" height="611" alt="image" src="https://github.com/user-attachments/assets/3bc68b44-8eb6-4a46-a970-6cdc80ec18ad" />

<img width="719" height="212" alt="image" src="https://github.com/user-attachments/assets/e34b3af9-3837-4d88-afa0-3c023ee0c74f" />


Clicking on the Basic Program: 

```
10 REM *** COMMODORE 64 SECURITY SYSTEM ***
20 ENC_PASS$ = "D13URKBT"
30 ENC_FLAG$ = "DSA|auhts*wkfi=dhjwubtthut+dhhkfis+hnkz" ' old "DSA|qnisf`bX_huXariz"
40 INPUT "ENTER PASSWORD: "; PASS$
50 IF LEN(PASS$) <> LEN(ENC_PASS$) THEN GOTO 90
60 FOR I = 1 TO LEN(PASS$)
70 IF CHR$(ASC(MID$(PASS$,I,1)) XOR 7) <> MID$(ENC_PASS$,I,1) THEN GOTO 90
80 NEXT I
85 FLAG$ = "" : FOR I = 1 TO LEN(ENC_FLAG$) : FLAG$ = FLAG$ + CHR$(ASC(MID$(ENC_FLAG$,I,1)) XOR 7) : NEXT I : PRINT FLAG$
90 PRINT "ACCESS DENIED"
100 END
```

The program stores an encoded password and an encoded flag:
```
20 ENC_PASS$ = "D13URKBT"
30 ENC_FLAG$ = "DSA|auhts*wkfi=dhjwubtthut+dhhkfis+hnkz"
```

It then asks for user input and checks if the input is correct by XOR’ing each character with 7:

```
70 IF CHR$(ASC(MID$(PASS$,I,1)) XOR 7) <> MID$(ENC_PASS$,I,1) THEN GOTO 90
```

Decode the Password. I XOR’d each character in ENC_PASS$ with 7 to get the original password:

```
enc_pass = "D13URKBT"
password = ''.join([chr(ord(c) ^ 7) for c in enc_pass])
print(password)
```
Output/ Password:

```
K48]YNER
```

Decode: 

```
enc_flag = "DSA|auhts*wkfi=dhjwubtthut+dhhkfis+hnkz"
flag = ''.join([chr(ord(c) ^ 7) for c in enc_flag])
print(flag)
```

Flag:

```
CTF{frost-plan:compressors,coolant,oil}
```













