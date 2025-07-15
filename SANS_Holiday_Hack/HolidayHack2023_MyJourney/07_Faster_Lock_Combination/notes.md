# Objective 8 - Faster Lock Combination

## Challenge:
Help Bow Ninecandle open a stubborn padlock on Steampunk Island by researching techniques to crack a combination lock using minimal guesswork.

---

## Steps I Took:

I started by watching a video linked in the challenge that demonstrated how to decode a typical Master combination lock. The method involved some hands-on manipulation and simple math.

First, I applied steady upward pressure on the shackle while slowly turning the dial. The dial locked up at number **31**, which I noted as the “sticky number.”

Next, I released the shackle, reset the dial to 0, then re-applied heavier pressure and turned the dial counter-clockwise. I found two numbers where the dial got stuck between positions: **5** and **6**. These became my guess values.

To get the **first digit**, I added 5 to the sticky number:  
`31 + 5 = 36` → First digit is **36**.

Then, I calculated `36 mod 4`, which gave a **remainder of 0**. This remainder was key for determining the **third digit**.

I created two number sets by adding 10, 20, and 30 to both guess numbers:

- Row 1 (from 5): 5, 15, 25, 35  
- Row 2 (from 6): 6, 16, 26, 36

From both rows, I picked numbers where `number mod 4 = 0`. That gave me **16** and **36**. I tested both on the lock and found **16** provided more movement when pressure was applied—indicating it was the correct **third digit**.

For the **second digit**, I used the earlier remainder (0) and built two more rows:

- Row 1 (0+2): 2, 10, 18, 26, 34  
- Row 2 (0+6): 6, 14, 22, 30, 38

I eliminated numbers that were within 2 of the third digit (16), leaving:  
Valid options: 2, 6, 10, 22, 26, 30, 34, 38

I tried different combinations with the structure `36 - X - 16`. On my third attempt, **36-10-16** opened the lock.

---

## Result:
Successfully unlocked the combination lock using logic-based deduction and some light trial-and-error. The working combination was **36-10-16**.

---

## Lesson Learned:
Even without knowing the original combo, physical feedback and simple math can be used to crack a combination lock efficiently. This simulated challenge demonstrated a realistic and surprisingly effective method for lock manipulation that could be useful in physical security assessments.

