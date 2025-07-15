# OBJECTIVE 14 - Phish Detection Agency  
_Completed by 8.01% of challenge participants_

## OBJECTIVE  
Help Fitzy Shortstack on Film Noir Island investigate a suspicious inbox and identify phishing emails by analyzing their headers.

## Hints

Hints provided for Objective 14  
- Learn the basics of email authentication — [Cloudflare’s guide on DMARC, DKIM, and SPF](https://www.cloudflare.com/en-gb/learning/email-security/dmarc-dkim-spf/) is a great place to start.

---

## My Approach

This challenge was all about reviewing email headers and applying foundational email security knowledge. Specifically, I focused on evaluating each email’s **SPF**, **DKIM**, and **DMARC** results to identify malicious messages.

### Step 1: Look for Obvious Failures  
Some emails were very easy to classify — any message with a header line showing:

```
DMARC: Fail
```

...was immediately flagged as phishing. These were the low-hanging fruit.

### Step 2: Compare Header Fields  
For the remaining emails, I looked closer at discrepancies between:

- The `From:` address  
- The `Return-Path:` address

If these two didn’t match — especially if the Return-Path came from a totally different domain — that was a red flag. Combined with missing or failing DKIM/SPF values, these emails were also marked as phishing.

### Step 3: Review All Messages  
I worked through each message one by one. By focusing on:

- DMARC results  
- Domain mismatch (From vs Return-Path)  
- Suspicious reply-to addresses  
- Failed SPF/DKIM alignment

...I was able to confidently identify the malicious messages.

---

## Result

I reviewed the full inbox and successfully identified **10 phishing emails** using a mix of DMARC failures, mismatched header fields, and email authentication clues.

---

## Lessons Learned

This challenge was a great refresher on real-world email header analysis. Understanding how SPF, DKIM, and DMARC work — and how attackers try to spoof trusted domains — is critical for identifying phishing. Even when DMARC doesn’t fail, subtle header mismatches can reveal malicious intent.

