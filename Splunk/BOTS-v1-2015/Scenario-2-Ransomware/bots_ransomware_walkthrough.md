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
[View the Screenshot](screenshots/Screenshot%202025-05-27%20153321.png)
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

[View the Screenshot]
Answer:
2816763 (1:2816763:4 but only 7 digits)
## Question #202

**Question:**  
[Write the question here exactly as asked]

---

**Steps Taken:**

- [Describe step 1]
- [Describe step 2]
- [Any queries used – paste as a code block:]
  ```splunk
  [your Splunk query here]


## Question #203
**Question:**  
[Write the question here exactly as asked]

---

**Steps Taken:**

- [Describe step 1]
- [Describe step 2]
- [Any queries used – paste as a code block:]
  ```splunk
  [your Splunk query here]


## Question #204

**Question:**  
[Write the question here exactly as asked]

---

**Steps Taken:**

- [Describe step 1]
- [Describe step 2]
- [Any queries used – paste as a code block:]
  ```splunk
  [your Splunk query here]


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




