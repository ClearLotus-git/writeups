# OBJECTIVE 10 - Game Cartridge Vol 2  
_Completed by 2.72% of challenge participants_

## OBJECTIVE
Find the second Gamegosling cartridge hidden on Pixel Island and beat the game to uncover the flag.

## Hints

Hints provided for Objective 10  
- Try walking around every tile on Pixel Island — the map is small, so don’t overlook any spots.  
- Something seems familiar here, but slightly off.  
- If you're feeling like you're going in circles, you might be missing a small detail.  
- “DIFFerent” might be a clue. Think code comparison.  
- Look for swapped values — maybe someone left a helpful hint behind.

---

## My Approach

### Step 1: Review the JavaScript
I opened the browser’s developer tools and checked the `script.js` file. At the top, it declared:

```javascript
const ROM_FILENAME = "rom/game";
```

Farther down, I found this bit of logic:

```javascript
let ranNum = Math.round(Math.random()).toString()
let filename = ROM_FILENAME + ranNum + ".gb";
console.log(filename);
```

The intention here was to randomly choose between two ROMs (`game0.gb` and `game1.gb`), but due to how `Math.round(Math.random())` works, the only possible results are `0` or `1`. That meant only **two possible ROMs** ever loaded.

### Step 2: Download Both ROM Files
I downloaded both files manually from:

- [game0.gb](https://gamegosling.com/vol2-akHB27gg6pN0/rom/game0.gb)  
- [game1.gb](https://gamegosling.com/vol2-akHB27gg6pN0/rom/game1.gb)  

You can also find local copies here:  
[game0](Assets/Vol2%20-%20game0.gb) | [game1](Assets/Vol2%20-%20game1.gb)

### Step 3: Compare the ROMs
I used `xxd` to convert both ROMs to hex format, then compared them:

```bash
xxd game0.gb > game0.hex
xxd game1.gb > game1.hex
diff game0.hex game1.hex
```

This revealed a slight difference at this offset:

```diff
< 00016a80: 2080 0c80 0300 ...
> 00016a80: 2080 0c80 0b00 ...
```

### Step 4: Patch the ROM and Explore
After patching the ROM and playing it in an emulator, a new portal appeared in the game. I entered it and found a pokeball labeled **ChatNPT**, who claimed to love "old-timey" radio.

When I interacted with the radio nearby, it started transmitting beeping sounds. I recognized this as Morse code.

### Step 5: Decode the Morse Code
I listened closely and translated the sequence into:
```
GL0RY
```

That’s the flag needed to complete this challenge.

---

## Result

I exploited a weak randomization script to download and analyze both versions of the ROM. After modifying one and following the path through a hidden portal, I found a radio that transmitted Morse code. The decoded flag was:

```
GL0RY
```

---

## Lessons Learned

This challenge was a great mix of static analysis, logic, and a bit of retro fun. Understanding the behavior of `Math.random()` helped expose a weak implementation, and using `xxd` + `diff` made comparing the ROMs easy. The hidden Morse code added a clever twist at the end.
