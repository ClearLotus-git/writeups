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
Checking the browser console led to a dead-end, showing only a list of Pokémon names. Looking further in the source code, I found another comment above this one:
```
<!--check console for extra surprise!)--> 
```
This seemed to be a rabbit hole as it only had a list of pokemon names ;(
I again looked at the source aand looked above the previous "surprise"

![image](https://user-images.githubusercontent.com/71709864/220814080-0b063f36-5633-4bc3-9bdf-a2ab4db83550.png)

I suspected these might be credentials, so I attempted to SSH into the machine using them:
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


