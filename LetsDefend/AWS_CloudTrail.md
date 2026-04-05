***AWS CloudTrail***

A new SIA secret agent transforms into a fearless hacktivist by spilling his country's most heinous secrets to the world.

```
1- Navigate into the AWSlogs directory
2- cd /home/analyst/AWSLogs/670756667180/CloudTrail/us-east-1/2023/03/11/
3- find . -type f -exec gunzip {} \;
```

What is the name of the IAM user account being used by the SIA agent?

Command:

```
grep agent ./*
```

Command:

```
grep -l agentdarius ./*
```

<img width="736" height="141" alt="image" src="https://github.com/user-attachments/assets/b56ce7b3-9ac4-433a-a5e6-2e172c909253" />


`agentdarius`

What is the source IP the SIA agent is authenticating from?

Command: 

```
cat json_file | jq
```
<img width="737" height="461" alt="image" src="https://github.com/user-attachments/assets/8251e724-90b4-43c5-81b1-eeffba46a21e" />

`185.202.237.209`

What was the SIA agent’s activity related to enumerating identities & permissions?

eventName keypair

| select(.userIdentity.userName=="agentdarius")

What managed policy did the SIA agent have?

How did the SIA agent attempt to establish persistence in the environment?

What permissions were associated with this persistence attempt?

What other resource did the SIA agent enumerate?

What bucket enumeration activities did the SIA agent perform? Answer format: XXX & XXX

What is the ARN of the bucket that the SIA agent tampered with?

How did the SIA agent expose his country’s secrets? Answer format: XXX & XXX








