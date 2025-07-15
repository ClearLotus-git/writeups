# OBJECTIVE 11 - Na'an  
_Completed by 8.13% of challenge participants_

## OBJECTIVE  
Outsmart Shifty McShuffles in a rigged card game on Film Noir Island to secure a win and uncover the objective flag.

## Hints

Hints provided for Objective 12  
- Try to confuse Shifty by submitting a value he doesn’t expect.  
- He mentioned building the game in Python — maybe there’s a vulnerability involving [NaN injection](https://www.tenable.com/blog/python-nan-injection).

---

## My Approach

### Step 1: Understand the Game Mechanics  
When the challenge starts, you're asked to choose 5 cards — each represented by a number between 0 and 9. You type the numbers in manually. Once your hand is submitted, Shifty plays his, and the two hands are compared.

It quickly became obvious that **Shifty is cheating** — replaying the same hand results in him always picking the exact cards needed to beat you. That told me he’s probably reading your inputs and tailoring his responses to win.

### Step 2: Analyze the Pattern  
While I couldn’t fully reverse-engineer Shifty’s logic, I noticed he always includes `0` and `9` in his hand, and when I submitted `0, 1, 8, 9`, he would mirror most of it. So I tested various combinations and noticed he was likely choosing the lowest unused number for his fifth card. A hand like `0, 1, 2, 8, 9` would cause a tie — but I needed a win.

### Step 3: NaN Injection Trick  
I remembered the hint about Python and `NaN` (Not-a-Number). In Python, if you write:

```python
float('nan') < 0  # False
float('nan') > 9  # False
```

This means that a poorly written bounds check like:

```python
if input < 0 or input > 9:
    reject()
```

…would let `nan` slip through.

Sure enough, I tried entering `nan` as one of the five card values — and the game accepted it.

### Step 4: Construct a Winning Hand  
With that, I submitted the following hand:

```
0, 1, 8, 9, nan
```

Shifty responded with his usual cheating hand, but because `nan` isn’t a real number, it’s treated as **both smaller than and greater than everything else** depending on context. That gave me 2 points in the comparison — enough to win the round.

I played this same hand 5 times, and Shifty never adapted. Turns out he’s smart — but not smart enough to handle `nan`.

---

## Result

By exploiting Python’s weak `NaN` comparison handling, I was able to sneak `nan` into my hand, confuse Shifty’s logic, and win every round. Repeating the same hand five times resulted in victory.

---

## Lessons Learned

This was a clever use of language-specific quirks — in this case, Python's handling of `NaN` in comparisons. The challenge highlights how small logic flaws (especially in input validation) can completely break a system. Also: never trust a hustling elf.

