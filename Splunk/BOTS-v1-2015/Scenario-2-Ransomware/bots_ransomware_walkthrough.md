#  Objective

A ransomware incident has occurred within the environment. Your task as a SOC analyst is to investigate the infection:
- Identify the infected host(s)
- Understand how the ransomware was delivered
- Examine which processes were executed
- Find indicators of compromise (IOCs)
- Suggest detection methods for future prevention

Ransomware screen shot: https://botscontent.netlify.app/v1/cerber-sshot.png

Bots v1 sourcetype summary: https://botscontent.netlify.app/v1/bots_sourcetypes.html

https://www.splunk.com/pdfs/solution-guides/splunk-quick-reference-guide.pdf (** Reference**)

## Question #200

**Question:**  
What was the most likely IPv4 address of `we8105desk` on 24AUG2016?

---

**Steps Taken:**

- Set date range between **08/24/2016** and **08/25/2016**  
- Thought sourcetypes: `wineventlog` / `sysmonlogs`
- Event sampling 1:1000
- Query used:  
  ```splunk
  index=botsv1 sourcetype="xmlwineventlog:microsoft-windows-sysmon/operational" "we8105desk"
[View the Screenshot: Splunk search results](screenshots/Screenshot%202025-05-27%20153321.png)

Answer:
192.168.250.100

## Question #201
**Question:**  
Amongst the Suricata signatures that detected the Cerber malware, which one alerted the fewest number of times? Submit ONLY the signature ID value as the answer.

---

**Steps Taken:**

- Suricada is an ids to catch host events (similar to snort) -> source_type  
- Cerber malware
- alert field/signature id field
- Query used:  
  ```splunk
  index=botsv1 sourcetype="suricata" "Cerber" | stats count by suricata_signature_id

[View Screenshot: Splunk search results](screenshots/Screenshot%202025-05-27%20160323.png)

Answer:
2816763 (1:2816763:4 but only 7 digits)

## Question #202
**Question:**  
What fully qualified domain name (FQDN) does the Cerber ransomware attempt to direct the user to at the end of its encryption phase?

---

**Steps Taken:**

- sysmonlogs has events whenever a process executes dns query X
- Search stream: dns datas
- requests made from infected host: 192.168.250.100
- what kind of query was made A records/query_type{}
  ```splunk
  index=botsv1 sourcetype="stream:dns" "192.168.250.100" record_type=A |stats count by "query{}"

[View Screenshot: Splunk search results](screenshots/Screenshot%202025-05-27%20162732.png)

[View Screenshot: VirusTotal](screenshots/Screenshot%202025-05-27%20162844.png)

Answer:
cerberhhyed5frqa.xmfir0.win

## Question #203
**Question:**  
What was the first suspicious domain visited by we8105desk on 24AUG2016?

---

**Steps Taken:**

- Staying in the same search query
- two of them stood out to me

  ```splunk
  index=botsv1 sourcetype="stream:dns" "192.168.250.100" record_type=A |stats count by "query{}" | sort -_time

Answer:
solidaritedeproximite.org

## Question #204
**Question:**  
During the initial Cerber infection a VB script is run. The entire script from this execution, pre-pended by the name of the launching .exe, can be found in a field in Splunk. What is the length of the value of this field?

---

**Steps Taken:**

- .vbs extensions VB "VisualBasic"
- looking for a script that has run -> syslogs have process IDS
- ParentCommandLine
  ```splunk
  index=botsv1 sourcetype="xmlwineventlog:microsoft-windows-sysmon/operational" "*.vbs"
  | eval length=len(ParentCommandLine)
  | table ParentCommandLine, length
  
[View Screenshot: Splunk search results](screenshots/Screenshot%202025-05-27%20172151.png)

Answer: 4490

## Question #205

**Question:**  
What is the name of the USB key inserted by Bob Smith?

---

**Steps Taken:**

- registry events -> usb and adding/ user experience events
- key_path field
- online searching for windows registry usb artifacts
- website: https://www.magnetforensics.com/blog/artifact-profile-usb-devices/ 
  ```splunk
  index=botsv1 sourcetype="winregistry" key_path="*Windows Portable Devices*"

[View Screenshot: online search magnet forensics ](screenshots/Screenshot%202025-05-27%20173011.png)  
[View Screenshot: Splunk search results  ](screenshots/Screenshot%202025-05-27%20173641.png)  
[View Screenshot: Splunk search results ](screenshots/Screenshot%202025-05-27%20173654.png)

Answer: MIRANDA_PRI

## Question #206
**Question:**  
Bob Smith's workstation (we8105desk) was connected to a file server during the ransomware outbreak. What is the IPv4 address of the file server?

---

**Steps Taken:**

- smb traffic stream
- dest_ip top number
  ```splunk
  index=botsv1 sourcetype="stream:smb"
[View Screenshot: Splunk search results  ](screenshots/Screenshot%202025-05-27%20174830.png)

Answer: 192.168.250.20

## Question #207
**Question:**  
How many distinct PDFs did the ransomware encrypt on the remote file server?

---

**Steps Taken:**

- win event logs looking for pdf
- deal with windows shares and narrow the search by looking for distinct filenames for the extension in question
- hostnames
  ```splunk
  index=botsv1 sourcetype="wineventlog*" "*.pdf" dest_nt_host="we9041srv.waynecorpinc.local" Source_Address="192.168.250.100" | table Relative_Target_Name | dedup Relative_Target_Name | stats count
  
[View Screenshot: Splunk search results](screenshots/Screenshot%202025-05-27%20184144.png)

Answer: 257 

## Question #208

**Question:**  

The VBscript found in question 204 launches 121214.tmp. What is the ParentProcessId of this initial launch?

---

**Steps Taken:**

- temp file, sysmon
- ParentProcessId, image id
- 121214.tmp
  ```splunk
  index=botsv1 sourcetype="xmlwineventlog:microsoft-windows-sysmon/operational" "121214.tmp"
  | table _time, host, Image, CommandLine, ParentImage, ParentCommandLine, ProcessId, ParentProcessId, User
  | sort _time
  
[View Screenshot: Splunk search results](screenshots/Screenshot%202025-05-27%20191920.png)

Answer: 3968 

## Question #209

**Question:**  

The Cerber ransomware encrypts files located in Bob Smith's Windows profile. How many .txt files does it encrypt?

---

**Steps Taken:**

- user profile, sysmon, filename extension
- text files. file server, workstatiopn limit: we8105desk
- Event code2 
- -Bob's windows profile
  ```splunk
  index=botsv1 sourcetype="xmlwineventlog:microsoft-windows-sysmon/operational"  "we8105desk" TargetFilename="C:\\Users\\bob.smith.WAYNECORPINC\\*.txt"
  
[View Screenshot:Splunk search results](screenshots/Screenshot%202025-05-27%20192628.png)  
[View Screenshot: Splunk search results](screenshots/Screenshot%202025-05-27%20192916.png)  
[View Screenshot: Splunk search results](screenshots/Screenshot%202025-05-27%20193014.png)  
[View Screenshot: Splunk search results](screenshots/Screenshot%202025-05-27%20193557.png)
 
Answer: 406 

## Question #210  

**Question:**   

The malware downloads a file that contains the Cerber ransomware cryptor code. What is the name of that file?

---

**Steps Taken:**

- suricada
- related to a url: cerberhhyed5frqa.xmfir0.win X
-  http event; solidaritedeproximite.org    V
  ```splunk
   index=botsv1 sourcetype="suricata" "solidaritedeproximite.org"
```

[View Screenshot: Splunk search results](screenshots/Screenshot%202025-05-27%20195437.png)

Answer: mhtr.jpg

## Question #211
**Question:**  
Now that you know the name of the ransomware's encryptor file, what obfuscation technique does it likely use?

---

**Steps Taken:**

- jpg
- malware hidden inside the file  
  ```splunk
  index=botsv1 sourcetype="stream:http" "mhtr.jpg"
[View Screenshot: Splunk search result](screenshots/Screenshot%202025-05-27%20200739.png)

Answer:
steganography
  


