#  Objective

A ransomware incident has occurred within the environment. Your task as a SOC analyst is to investigate the infection:
- Identify the infected host(s)
- Understand how the ransomware was delivered
- Examine which processes were executed
- Find indicators of compromise (IOCs)
- Suggest detection methods for future prevention

Ransomware screen shot: https://botscontent.netlify.app/v1/cerber-sshot.png

Bots v1 sourcetype summary: https://botscontent.netlify.app/v1/bots_sourcetypes.html

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
[View the Screenshot:Splunk search results](screenshots/Screenshot%202025-05-27%20153321.png)

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
  
[View Screenshot](screenshots/Screenshot%202025-05-27%20172151.png)

Answer: 4490

## Question #205

**Question:**  
[Write the question here exactly as asked]

---

**Steps Taken:**

- [Describe step 1]
- [Describe step 2]
- [Any queries used – paste as a code block:]
  ```splunk
  [your Splunk query here]


## Question #206
**Question:**  
[Write the question here exactly as asked]

---

**Steps Taken:**

- [Describe step 1]
- [Describe step 2]
- [Any queries used – paste as a code block:]
  ```splunk
  [your Splunk query here]




