Gnome Tea

Difficulty: 3/5

Objective: 
Enter the apartment building near 24-7 and help Thomas infiltrate the GnomeTea social network and discover the secret agent passphrase.

Task:

<img width="438" height="403" alt="image" src="https://github.com/user-attachments/assets/917f24c0-471d-4bbb-b6f8-0cc1aafb2606" />

<img width="810" height="669" alt="image" src="https://github.com/user-attachments/assets/8a3e86d2-ac50-4fab-bcef-1e6c5cf6db6d" />

<img width="450" height="722" alt="image" src="https://github.com/user-attachments/assets/d32b729f-5569-41de-aae7-45a669aa8381" />




<img width="529" height="271" alt="image" src="https://github.com/user-attachments/assets/e883819a-ac87-4a28-9016-b86514f06a4d" />

<img width="1018" height="344" alt="image" src="https://github.com/user-attachments/assets/90337ddc-deeb-4421-9ecf-9e47a1dbcdc9" />


<img width="1265" height="539" alt="image" src="https://github.com/user-attachments/assets/55af478b-b8cc-4441-8b2d-0345154426fd" />




Looking for passphrase through license: 

```
firebase.firestore().collection("gnomes")
  .get()
  .then(snapshot => {
    snapshot.forEach(doc => {
      const data = doc.data();
      if (data.driversLicenseUrl) {
        console.log("📸 MATCH FOUND:", doc.id, data.driversLicenseUrl);
      }
    });
  });
```

Example of output: 

<img width="1249" height="489" alt="image" src="https://github.com/user-attachments/assets/f6b3a73e-d485-426d-b6f6-c87ef71cb9d2" />

<img width="1025" height="551" alt="image" src="https://github.com/user-attachments/assets/8048bdec-e068-47bf-97ee-7d39c63bc286" />

<img width="900" height="551" alt="image" src="https://github.com/user-attachments/assets/17e29c68-16b2-4057-bf3b-46c5b305543c" />


gnome without license link: 

<img width="1257" height="117" alt="image" src="https://github.com/user-attachments/assets/a7588fa9-1ee7-4223-878e-03fe45b97afc" />

<img width="1449" height="153" alt="image" src="https://github.com/user-attachments/assets/3db1376e-7db3-4520-a861-08a71df37085" />

<img width="1265" height="141" alt="image" src="https://github.com/user-attachments/assets/988313ca-36a8-43b0-9b14-683cad961f4f" />

```
C:\Users\Nick>curl -v "https://storage.googleapis.com/holidayhack2025.firebasestorage.app/gnome-documents/7sQlw9l4xUOWSjDTphvLgKVEm0j1_drivers_license.jpeg" --output license.jpg
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Host storage.googleapis.com:443 was resolved.
* IPv6: 2607:f8b0:4009:81c::201b, 2607:f8b0:4009:800::201b, 2607:f8b0:4009:808::201b, 2607:f8b0:4009:809::201b
* IPv4: 172.217.1.123, 172.217.2.59, 172.217.5.27, 142.250.191.123, 142.250.191.155, 142.250.191.187, 142.250.191.219, 142.250.191.251, 142.251.32.27, 142.251.34.251, 172.217.4.219, 142.250.190.27, 142.250.190.59, 142.250.190.91, 142.250.190.123, 142.250.190.155
*   Trying [2607:f8b0:4009:81c::201b]:443...
* schannel: disabled automatic use of client certificate
* ALPN: curl offers http/1.1
* ALPN: server accepted http/1.1
* Established connection to storage.googleapis.com (2607:f8b0:4009:81c::201b port 443) from 2600:6c64:427f:392c:d083:cfd:73ef:9cd6 port 57791
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* using HTTP/1.x
> GET /holidayhack2025.firebasestorage.app/gnome-documents/7sQlw9l4xUOWSjDTphvLgKVEm0j1_drivers_license.jpeg HTTP/1.1
> Host: storage.googleapis.com
> User-Agent: curl/8.16.0
> Accept: */*
>
* Request completely sent off
* schannel: remote party requests renegotiation
* schannel: renegotiating SSL/TLS connection
* schannel: SSL/TLS connection renegotiated
< HTTP/1.1 200 OK
< Content-Type: image/jpeg
< X-GUploader-UploadID: AOCedOGyYRQ0BOvcYIUXJv0f-I0Zq_wXrD_rTytuLt79lvoIEQcv0Mwxge4DCccf_5XOaoGMQyzhb3U
< Date: Tue, 18 Nov 2025 22:49:58 GMT
< Cache-Control: public, max-age=31536000, immutable
< Expires: Wed, 18 Nov 2026 22:49:58 GMT
< Last-Modified: Tue, 30 Sep 2025 18:21:52 GMT
< ETag: "be5e14ed19b2ba3df4428ded02dcf946"
< x-goog-generation: 1759256512434028
< x-goog-metageneration: 3
< x-goog-stored-content-encoding: identity
< x-goog-stored-content-length: 245128
< x-goog-meta-firebaseStorageDownloadTokens: 1b94b488-a159-4888-bc55-51e9db69c560
< x-goog-hash: crc32c=1FYBWg==
< x-goog-hash: md5=vl4U7Rmyuj30Qo3tAtz5Rg==
< x-goog-storage-class: REGIONAL
< Accept-Ranges: bytes
< Content-Length: 245128
< Server: UploadServer
< Alt-Svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
<
{ [379 bytes data]
100  239k  100  239k    0     0   195k      0  0:00:01  0:00:01 --:--:--  196k
* Connection #0 to host storage.googleapis.com:443 left intact

C:\Users\Nick>
```













