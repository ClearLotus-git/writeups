Its All About Defang

Difficulty: 1/5

Objective:

Find Ed Skoudis upstairs in City Hall and help him troubleshoot a clever phishing tool in his cozy office.



<img width="979" height="716" alt="image" src="https://github.com/user-attachments/assets/27e7e25f-0dba-45ee-95d6-bd493b2ec275" />

<img width="1144" height="591" alt="image" src="https://github.com/user-attachments/assets/06d2c654-9131-4eab-8445-6a81a62de506" />


<img width="431" height="308" alt="image" src="https://github.com/user-attachments/assets/4e55dc32-6507-49b0-8320-bf411ec04c62" />


Challenge: 

You are greeted with the Dosis Neighborhood SOC

<img width="1708" height="875" alt="image" src="https://github.com/user-attachments/assets/80b5d226-8fba-4fe7-b160-e11a10d0c7f4" />

Step Objectives: 

Step 1:

This phishing email may be connected to the mysterious Gnome activities reported throughout our neighborhood! Extracting IOCs (Indicators of Compromise) is essential to protect the Counter Hack Crew and identify the threat actors behind this campaign. Your mission:

Extract all suspicious domains, IPs, URLs, and email addresses
Use the tabs below to extract each IOC type from the email. Be sure not to include legitimate assets!

We need to use the regex patterns to extract each of the fields. This can be found by looking in the reference section 

<img width="1002" height="765" alt="image" src="https://github.com/user-attachments/assets/af57bf0a-214d-4378-a895-983478bf0f9d" />


Use what we found above to filter out the patterns in Step 1:

<img width="995" height="420" alt="image" src="https://github.com/user-attachments/assets/7f11b97a-c2c5-413e-adf0-e607a7f9ba7a" />


<img width="1008" height="397" alt="image" src="https://github.com/user-attachments/assets/6fd2d013-64ee-4eb8-819e-c619dee00ef5" />


<img width="1007" height="378" alt="image" src="https://github.com/user-attachments/assets/b3dd2147-f4f3-4150-b8ea-b4f1bdc8eb4b" />


<img width="1001" height="384" alt="image" src="https://github.com/user-attachments/assets/2b3337ad-5dd3-407d-a6fd-81ee82d69fb9" />





Step 2:

Defanging IOCs (Indicators of Compromise) is crucial to ensure that malicious content cannot be accidentally activated. This phishing campaign may be connected to the recent Gnome activities! Your mission:

Replace dots/periods with [.]
Replace @ in email addresses with [@]
Replace http with hxxp in URLs
Replace :// with [://] in URLs
Submit the defanged IOCs to the Counter Hack Security Team

Check the Reference page for SED commands Defanging

<img width="973" height="603" alt="image" src="https://github.com/user-attachments/assets/2db8c32c-ad11-4f43-bc2c-4ef9044138eb" />

```
Custom SED Command(s):
s/http/hxxp/g; s#://#[://]#g; s/@/[@]/g; s/\./[.]/g

Defanged IOCs
9

Domains (3)
icicleinnovations[.]mail
mail[.]icicleinnovations[.]mail
core[.]icicleinnovations[.]mail
IP Addresses (2)
172[.]16[.]254[.]1
192[.]168[.]1[.]1
URLs (2)
hxxps[://]icicleinnovations[.]mail/renovation-planner[.]exe
hxxps[://]icicleinnovations[.]mail/upload_photos
Email Addresses (2)
sales[@]icicleinnovations[.]mail
info[@]icicleinnovations[.]mail
```

After submitting the report :

<img width="529" height="821" alt="image" src="https://github.com/user-attachments/assets/2106e4b4-2e0d-41f1-87f3-9029d7e3751e" />














