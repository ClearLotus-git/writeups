# OBJECTIVE 21 - Camera Access  

## OBJECTIVE  
Gain access to Jack's camera. What's the third item on Jack's TODO list?

## Hints

In his hubris, Wombley revealed that he thinks you won't be able to access the satellite's "Supervisor Directory". There must be a good reason he mentioned that specifically, and a way to access it. He also said there's someone else masterminding the whole plot. There must be a way to discover who that is using the nanosat.
</details>

---

## My Approach

This challenge began at **Zenith SGS** on Space Island. After interacting with the vending machine and the middle console, I obtained a **Docker image** and a **WireGuard configuration** from GateXOR the alligator.

---

### Step 1: Connect to the NanoSat Environment

I set up the WireGuard VPN:

```bash
sudo cp client.conf /etc/wireguard/wg0.conf
sudo wg-quick up wg0
```

Then launched the **NanoSat MO Base Station Tool** and connected to:

```
maltcp://10.1.1.1:1024/nanosat-mo-supervisor-Directory
```

---

### Step 2: Start the Camera App

In the GUI:

- Go to **Apps Launcher Service** tab  
- Select **Camera**  
- Click **runApp**

Next, under **Communications Settings**, connect to:

```
App: camera
```

Then under the **Action Service** tab:

- Select `Base64SnapImage`  
- Click **submitAction**

This instructs the nanosat to capture a photo.

---

### Step 3: Capture the Image Transmission

Because the interface doesn't allow copying the Base64 string directly, I used **Wireshark** on interface `wg0`:

```bash
sudo wireshark &
```

Once running:

- Go back to the **Parameter Service** tab  
- Select `Base64SnapImage`  
- Click **getValue**

After capture completes:

- Right-click on one of the TCP packets
- Choose **Follow → TCP Stream**
- Save the full stream as `output.txt`

---

### Step 4: Extract the Image

From inside Docker:

```bash
docker cp <container_id>:/root/output.txt /home/kali
```

Then decode the image:

```bash
base64 -d output.txt > image2.jpg
```

---

### Step 5: View the Result

Opening `image2.jpg` reveals Jack’s full TODO list. Zooming in reveals the **third item** clearly — the answer to this objective.

📝 **Third Item on Jack’s TODO List:**  
> _Whatever the actual flag value was in your version of the challenge (e.g., "Hack the satellites!")_  
_Add your version's correct text here when uploading._

---

## Lessons Learned

This challenge demonstrated the value of network traffic analysis for data recovery when direct access is blocked. It also reinforced how layered systems and obscure services can expose sensitive data when not properly secured.

