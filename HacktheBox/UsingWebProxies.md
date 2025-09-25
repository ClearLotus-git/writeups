# Web Proxies - Skills Assessment

We are performing internal penetration testing for a local company. As you come across their internal web applications, 
you are presented with different situations where Burp/ZAP may be helpful. Read each of the scenarios in the questions below, and determine the features that would be the most useful for each case. 
Then, use it to help you in reaching the specified goal.


1. The /lucky.php page has a button that appears to be disabled. Try to enable the button, and then click it to get the flag.

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

<img width="992" height="729" alt="image" src="https://github.com/user-attachments/assets/ac73b6a7-d22d-4cb4-b00d-200738556cdc" />















