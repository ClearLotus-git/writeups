# Web Proxies - Skills Assessment

We are performing internal penetration testing for a local company. As you come across their internal web applications, 
you are presented with different situations where Burp/ZAP may be helpful. Read each of the scenarios in the questions below, and determine the features that would be the most useful for each case. 
Then, use it to help you in reaching the specified goal.

---

### 1.) The /lucky.php page has a button that appears to be disabled. Try to enable the button, and then click it to get the flag. 

Use ZAP to open up a proxy to the targeted page:

<img width="1922" height="690" alt="image" src="https://github.com/user-attachments/assets/ffcbfcb2-f466-4ef3-b2f1-d52c9021f69a" />

In the GET response sent to /lucky.php the button has the attribute disabled:

<img width="1911" height="600" alt="image" src="https://github.com/user-attachments/assets/23503812-b75e-40fc-be20-0490b822ed55" />

Using Replacer by `CTRL+R` and selecting the  `Add...`: 

<img width="972" height="763" alt="image" src="https://github.com/user-attachments/assets/5f87dacf-ae7d-4b1e-8bb9-42a2b22cd7bc" />

Set Match Type to `Response Body String`, Match String to `disabled>`, Replacement String to `>`, check `Enable`, and click on `Save`:

<img width="672" height="530" alt="image" src="https://github.com/user-attachments/assets/8adbd1b5-bb1e-412e-a71a-b42882b19898" />

Select the GET request and click on Open/Resend with Request Editor...: 

<img width="1116" height="859" alt="image" src="https://github.com/user-attachments/assets/f5c1767f-4bf8-4c8b-b11c-a8db32c49e38" />

The response body no longer contains disabled:

<img width="992" height="729" alt="image" src="https://github.com/user-attachments/assets/ac73b6a7-d22d-4cb4-b00d-200738556cdc" />

Right-click on the response and choose Open URL in System Browser to notice you can click the button as it is not disabled anymore: 

<img width="1095" height="785" alt="image" src="https://github.com/user-attachments/assets/7c2defdb-3fc2-4df8-92f8-6b6077800c79" />

Then, right-click once more and open in the browser:

<img width="1539" height="799" alt="image" src="https://github.com/user-attachments/assets/b9f113d4-4cc0-438d-800c-8405c499253a" />

Click the chance to win a flag about 8 times:

<img width="757" height="406" alt="image" src="https://github.com/user-attachments/assets/295cd992-272d-4073-b1de-83e11aba40c7" />

--- 

### 2.) The /admin.php page uses a cookie that has been encoded multiple times. Try to decode the cookie until you get a value with 31-characters. Submit the value as the answer.

Go to /admin.php to capture the request in ZAP and notice the cookie value within the Cookie header:

<img width="1706" height="594" alt="image" src="https://github.com/user-attachments/assets/0aecac3c-919b-46e1-aa58-3aa7652a69d5" />

<img width="1252" height="639" alt="image" src="https://github.com/user-attachments/assets/39325290-49a8-4daa-8601-f1999b102d00" />

<img width="1590" height="482" alt="image" src="https://github.com/user-attachments/assets/0c0ba501-8a52-4b0f-b23c-8806932229ab" />

Select the hash after cookie=, right-click and select Encode/Decode/Hash...:

<img width="1467" height="807" alt="image" src="https://github.com/user-attachments/assets/01fc09cf-b600-49f8-818c-272b1ee9f965" />

Click on the Decode tab and copy the ASCII Hex Decode value:

<img width="1009" height="758" alt="image" src="https://github.com/user-attachments/assets/7ac30d11-9536-400d-955e-724dfc080a30" />

Paste the ASCII Hex Decode Value in the top bar; the answer will be under the Base64 Decode:

<img width="842" height="494" alt="image" src="https://github.com/user-attachments/assets/4a704feb-7c77-4865-aaa5-62e18813820d" />

---

### 3.) Once you decode the cookie, you will notice that it is only 31 characters long, which appears to be an md5 hash missing its last character. So, try to fuzz the last character of the decoded md5 cookie with all alpha-numeric characters, while encoding each request with the encoding methods you identified above.

Using Burp Suite and navigating to the /admin.php page, capture the request and look at the cookie value within the Cookie header. Send to Intruder:

<img width="1543" height="316" alt="image" src="https://github.com/user-attachments/assets/f18e9aa5-b9bc-4abe-8883-e877e315facb" />
<img width="1158" height="568" alt="image" src="https://github.com/user-attachments/assets/3c564f65-0049-4792-bba6-d027fd297b76" />

Replace the default cookie with the MD5 hash 3dac93b8cd250aa8c1a36fffc79a17a, select it, and click on Add § on both sides:

<img width="1295" height="596" alt="image" src="https://github.com/user-attachments/assets/828b90b3-bff8-4465-8e29-1992dc442921" />

Click on the Payloads tab then on Load ... under Payload Options and load the file alphanum-case.txt from /opt/useful/SecLists/Fuzzing/:

<img width="1000" height="765" alt="image" src="https://github.com/user-attachments/assets/34c1e982-619e-4c83-9d35-ddb471e70c35" />

Under Payload Processing, click on Add, select Add prefix as the processing rule, and paste in the MD5 hash 3dac93b8cd250aa8c1a36fffc79a17a for Prefix:

<img width="1847" height="679" alt="image" src="https://github.com/user-attachments/assets/ab0b860a-675d-4e9a-881c-d6820205366f" />

<img width="730" height="365" alt="image" src="https://github.com/user-attachments/assets/499c0d23-2369-4250-885a-5107d3c53c12" />

Add the Base64-encode and Encode as ASCII hex processing rules:

<img width="720" height="350" alt="image" src="https://github.com/user-attachments/assets/80433328-845a-416d-89e3-e238235bd06e" />

Start Attack:

<img width="874" height="681" alt="image" src="https://github.com/user-attachments/assets/ac1dbddc-035d-4bbb-b769-1c6dabd74e24" />

<img width="759" height="406" alt="image" src="https://github.com/user-attachments/assets/b157579d-c119-40f4-8ff3-7f272827c068" />

--- 

### You are using the 'auxiliary/scanner/http/coldfusion_locale_traversal' tool within Metasploit, but it is not working properly for you. You decide to capture the request sent by Metasploit so you can manually verify it and repeat it. Once you capture the request, what is the 'XXXXX' directory being called in '/XXXXX/administrator/..'?

Lanching msfconsole and adding the following: 

<img width="1292" height="557" alt="image" src="https://github.com/user-attachments/assets/6545f91b-f8e5-4e7e-bec4-33508ccfd12e" />

Before running the scan, make sure that Burp Suite is intercepting requests, and then run the exploit:

<img width="1086" height="167" alt="image" src="https://github.com/user-attachments/assets/b3ffc367-54d9-4220-a8d2-db29639a3101" />

Checking back in Burp Suite the directory can be seen: 

<img width="1309" height="205" alt="image" src="https://github.com/user-attachments/assets/2f6c77ec-bcb3-4866-bb9c-c9f5b09663b2" />

---

 
<p align="center">
  <img width="300" height="128" alt="image" src="https://github.com/user-attachments/assets/9d4e61ff-adb8-4821-a522-302c8751f272" />
</p>


















