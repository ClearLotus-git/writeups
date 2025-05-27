# Scenario 2: Ransomware (Splunk BOTS v1 - 2015)

This directory contains my personal analysis and walkthrough for **Scenario 2 - Ransomware** from Splunk's Boss of the SOC v1 (2015) challenge.

## Overview / Story
After the excitement of yesterday, Alice has started to settle into her new job. Sadly, she realizes her new colleagues may not be the crack cybersecurity team that she was led to believe before she joined. Looking through her incident ticketing queue she notices a “critical” ticket that was never addressed. Shaking her head, she begins to investigate. Apparently on August 24th Bob Smith (using a Windows 10 workstation named we8105desk) came back to his desk after working-out and found his speakers blaring (click below to listen), his desktop image changed (see below) and his files inaccessible.

Alice has seen this before... ransomware. After a quick conversation with Bob, Alice determines that Bob found a USB drive in the parking lot earlier in the day, plugged it into his desktop, and opened up a word document on the USB drive called "Miranda_Tate_unveiled.dotm". With a resigned sigh she begins to dig into the problem...

## Contents
There are 12 questions that you need to go through and answer using splunk. 
-`bots_ransomware_walkthrough.md` will contain the step by analysis
-`queries/` folder is for relevant Splunk SPL queries
-`screenshots/` folder is for any Splunk dashboard screenshots or visualizations

## Source and Credits
This challenge scenario is part of [Splunk Boss of the SOC (BOTS) v1 – 2015](https://bots.splunk.com/event/3oQ7sqI5bajOCP43o0svqT/scenario/5vqgZJanGgTCXawi4nliIF).  
All rights to the scenario, data, and challenge content belong to Splunk.  
Splunk quick reference guide:
https://www.splunk.com/pdfs/solution-guides/splunk-quick-reference-guide.pdf

This write-up is an independent analysis for educational and portfolio purposes only.
