# Gotta Catch'em All Room

<p align="left">
  <img src="https://github.com/user-attachments/assets/56cd072b-fc45-4deb-a4b0-7ba43aca8ec6" alt="gottacatchemallthm" width="300">
</p>




---

## Overview  
이 방은 포켓몬 시리즈에서 아이디어를 얻었어요. 여러 가지 문제를 풀면서 방 안에 숨겨진 포켓몬들을 모두 모으는 것이 목표예요.

---

## Question 1

이 방에서는 먼저 attack machine에서 nmap 스캔으로 시작했어요.

```
nmap -sC -sV {Machine-IP}
```
browser console 체크했는데 완전 dead-end였어요… 그냥 Pokémon 이름 리스트만 나왔어요. 그래서 source code 좀 더 봤는데, 그 밑에 있던 comment 위에 또 하나 더 있더라고요:
```
<!--check console for extra surprise!)--> 
```
이건 그냥 rabbit hole 같았어요 ㅠㅠ Pokémon 이름 리스트밖에 없었어요. 그래서 다시 source 봤고, 아까 봤던 "surprise" 코멘트 위쪽도 체크해봤어요.

![image](https://user-images.githubusercontent.com/71709864/220814080-0b063f36-5633-4bc3-9bdf-a2ab4db83550.png)

혹시 이게 credentials일 수도 있겠다 싶어서, SSH로 그 머신에 로그인 시도해봤어요:
```
ssh username@{Machine-IP}
```

The SSH connection succeeded. Once connected, I navigated to the user's home directory and found a zipped file. I extracted it using:


```
unzip <file_name.zip>
```

This file contained data related to Grass-type Pokémon, but it was encoded in hexadecimal. To decode it, I used Cryptii’s Hex Decoder.



## Question 2

To find the next Pokémon, I used the locate command with the keyword from the question:
```
locate --all water-type 2>/dev/null
```

After locating the file, I decoded its contents, which appeared to be encrypted with a Caesar cipher. I used the Caesar cipher decoder on Cryptii to get the answer.


## Question 3

For the third Pokémon, I navigated to the /etc/ directory and discovered an oddly named directory:
```
/etc/Why_am_i_here?
```
Inside this directory was the file needed for Question 3. The content was Base64 encoded, so I decoded it using:

```
echo -n 'string' | base64 --decode
```

## Question 4 

The final question asked for the root's favorite Pokémon. Earlier, I noticed a user named ash and tried to explore possible privilege escalation routes but had no luck initially. I searched the /home directory and found a suspicious file inside /home/ash/Videos.

The file, named something like Could_this_be_what_Im_looking_for?.cplusplus, looked like a fake C++ file. I opened it with:

```
cat Could_this_be_what_Im_looking_for?.cplusplus
```

Using information from this file, I was able to log in as ash. Running:

```
su ash
```
Now that i was the ash user i can check privileges using:

```
sudo -lah
```
It shows that ash has permission to open the last file.  We see that (ALL : ALL ) ALL , that means if we’ll type “sudo su” command in our terminal we don’t need to put any creds using:
```
sudo su
```
Now that we are root, we should be able to read roots favorite pokemon :).
```
cat roots-pokemon.txt
```

Here we have the final flag and can mark this room as complete. 


