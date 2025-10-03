# Command Injections Skills Assessment 

## Objective: 

You are contracted to perform a penetration test for a company, and through your pentest, you stumble upon an interesting file manager web application. As file managers tend to execute system commands, you are interested in testing for command injection vulnerabilities.

Use the various techniques presented in this module to detect a command injection vulnerability and then exploit it, evading any filters in place.

Authenticate to 94.237.48.12:56094 with user "guest" and password "guest" and find the content of '/flag.txt'?

----
### Lab

<img width="1008" height="635" alt="image" src="https://github.com/user-attachments/assets/47822014-1d20-427c-869e-ec731a478227" />

Clicking on Copy to... on a file will redirect to a new page with two main options Copy and Move, while also being able to choose the destination folder:

<img width="1897" height="532" alt="image" src="https://github.com/user-attachments/assets/9a4e3ced-e560-4158-8197-6c420e190307" />

<img width="1408" height="515" alt="image" src="https://github.com/user-attachments/assets/819d681e-4c47-4aba-ad57-1b9de7f88d30" />

Test the Move functionality. Clicking Move on a file without the selecting the tmp folder as the destination folder will throw the following error:

<img width="1274" height="343" alt="image" src="https://github.com/user-attachments/assets/5855dffc-5b96-49d6-bc9a-3391109080e3" />

Run Burp Suite and then click on Move with no destination folder to move a file:

<img width="1134" height="491" alt="image" src="https://github.com/user-attachments/assets/037e6d11-093d-406b-8244-d0a5a4a1fc86" />

In Burp, send the request to Repeater and view the response: 
<img width="1546" height="667" alt="image" src="https://github.com/user-attachments/assets/638de1ef-3d50-4044-a322-7ce7ad1ba24c" />

There are two GET parameters being passed in the request, to and from. Injecting the & operator passes by, as the developers
may have thought that it is required for URLs, making it whitelisted:

<img width="1748" height="494" alt="image" src="https://github.com/user-attachments/assets/70c90661-cc3c-414b-b0c4-0c479e11c63f" />

Inject & cat /flag.txt to read the flag file; to bypass white-space, use $IFS, and to bypass slashes, use ${PATH:0:1}, 
therefore, the payload can either be $IFS%26c"a"t$IFS${PATH:0:1}flag.txt, or $IFS%26b"a"sh<<<$(base64%09-d<<<Y2F0IC9mbGFnLnR4dA==).

`GET /index.php?to=tmp$IFS%26c"a"t$IFS${PATH:0:1}flag.txt&from=51459716.txt&finish=1&move=1 HTTP/1.1`

<img width="1008" height="393" alt="image" src="https://github.com/user-attachments/assets/cdb6e567-f374-424f-a83d-b95f68a533de" />

---

FINISH 







