# Gotta Catch'em All Room


![image](https://user-images.githubusercontent.com/71709864/220810615-fbeacb2d-d011-4b65-b7a9-d6e2543b5cff.png)


____________________________________________________________

## This room is based on the original Pokemon series. Can you obtain all the Pokemon in this room?


## Question 1

For this room I started with an nmap scan on the attack machine.

```
nmap -sC -sV {Machine-IP}
```
I can see there is an ssh & HTTP port open. We will use both of these ports for this room.
I then opened my browser and searched the ip address. Looking through the page source I came across 
a comment in the code that read:  

```
<!--check console for extra surprise!)--> 
```
This seemed to be a rabbit hole as it only had a list of pokemon names ;(
I again looked at the source aand looked above the previous "surprise"

![image](https://user-images.githubusercontent.com/71709864/220814080-0b063f36-5633-4bc3-9bdf-a2ab4db83550.png)

I assumed this could be username and password so I attemptted to ssh into the machine.
```
ssh username@{Machine-IP}
```

The ssh worked and I was now connected to the machine. I went to the users home directory and found an 
unzip file.


```
unzip <file_name.zip>
```

This is the first file for Question 1 Grass-Type Pokemon

I looks like the file contents are in hexidecimal. I used

 [https://cryptii.com/pipes/hex-decoder](https://hexdecoder.com/)


## Question 2

I used the 'locate' command along with the name in the question to find the next pokemon

```
locate --all water-type 2>/dev/null
```

After decoding, I Found my answer!

Caesar Cipher Decoder: https://cryptii.com/pipes/caesar-cipher


## Question 3

After locating the first two Pokemon, you'll move over to the '/etc/' directory, and there will be a weird directory located there titled 'Why_am_i_here?'

After changing to the correct directory, you'll see the file we need for our third question!

This one needs to be decoded using base64.

```
echo -n 'string' | base64 --decode
```

## Question 4 

Question 4 we need to find roots favorite pokemon. I previously saw an ash username and search around to 
see if we could escalate privieges. Having no luck, I searched around in the /home directory. Here in the /Videos file 
a file inside that looked suspicious.  
As I transversed through the directories I found the end file and opened it.

Hmm, this looks like a fake C++ file, maybe it has something in it?

```
cat Could_this_be_what_Im_looking_for?.cplusplus
```

I used this to login to the ash user. I then ran a command to check the permissions of the ash user

```
sudo -lah
```
It shows that ash has permission to open the last file 
```
roots-pokemon.txt
```

Here we have the final flag and can mark this room as complete. 

