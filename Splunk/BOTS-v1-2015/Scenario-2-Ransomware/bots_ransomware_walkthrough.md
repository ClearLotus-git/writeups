#  Objective

A ransomware incident has occurred within the environment. Your task as a SOC analyst is to investigate the infection:
- Identify the infected host(s)
- Understand how the ransomware was delivered
- Examine which processes were executed
- Find indicators of compromise (IOCs)
- Suggest detection methods for future prevention

Ransomware screen shot: https://botscontent.netlify.app/v1/cerber-sshot.png
Bots v1 sourcetype summary: https://botscontent.netlify.app/v1/bots_sourcetypes.html

## #200 
# Question:
What was the most likely IPv4 address of we8105desk on 24AUG2016?
-set date range ->  between 08/24/2016 through 08/25/2016
-sourcetype list-> wineventlog/sysmonlogs
`index=botsv1 sourcetype="xmlwineventlog:microsoft-windows-sysmon/operational" "we8105desk"`
-event sampling 1:1000
![We8105desk IP on 24AUG2016](https://github.com/ClearLotus-git/writeups/blob/main/Splunk/BOTS-v1-2015/Scenario-2-Ransomware/screenshots/Screenshot%202025-05-27%20153321.png)

