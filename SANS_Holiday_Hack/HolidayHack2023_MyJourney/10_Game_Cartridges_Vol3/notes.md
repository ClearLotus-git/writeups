# OBJECTIVE 11 - Game Cartridge Vol 3  


## OBJECTIVE  
Find the third Gamegosling cartridge and complete the game to uncover the final flag.

## Hints

Hints provided for Objective 11  
- The treasure in Rusty Quay is marked by a sparkle on the ground — zooming out and adjusting the camera can help with navigation.  
- The game is lengthy, so take advantage of save states.  
- 8-bit systems don’t handle large values well — think about overflows.  
- The coin count seems to be... **overflowing**?

---

## My Approach

### Step 1: Locate and Load the ROM  
I started by checking the game’s source code and found the ROM filename defined in `script.js` as:

```javascript
const ROM_FILENAME = "rom/game.gb";
```

That meant the ROM could be downloaded directly from:  
[https://gamegosling.com/vol3-7bNwQKGBFNGQT1/rom/game.gb](https://gamegosling.com/vol3-7bNwQKGBFNGQT1/rom/game.gb)

I loaded the ROM into the **BGB Game Boy Emulator**, which allows state saving and direct memory register inspection — extremely useful for analyzing how values are stored and manipulated.

### Step 2: Identify Coin Register Values  
While playing, I tried to locate which memory registers were storing the coin count. Using BGB’s memory tools, I was able to narrow it down after monitoring register changes as I collected coins.

Here’s how the coin digits were mapped:

| Digit | Registers             |
|-------|------------------------|
| Hundreds | `C160`, `CB9E`     |
| Tens     | `C12C`, `CB9C`     |
| Units    | `C1F8`, `CBA2`     |

### Step 3: Overflow the Coins  
Once I knew where the coin values lived, I froze all 6 registers to `09`, giving me **999 coins**. This allowed me to max out the coin counter and (intentionally) cause a buffer overflow.

### Step 4: Cross the Cliff & Get the Flag  
Normally at the end of the game, the elf jumps into a cliff with no path forward. But with the overflowed coin count, new floating platforms appeared across the chasm — likely a side effect of the overflow bug.

I used those platforms to cross, met a hacker NPC who gave me a **passcode**, and brought it to ChatNPT. After entering the code, ChatNPT moved a large boulder that had been blocking the flag.

Final result? A dramatic victory with:

```
MUCH GLOOOOOOOOORYYY
```

---

## Result

By editing and freezing memory registers in BGB, I gave myself 999 coins and triggered a buffer overflow. This unlocked a hidden path at the end of the game and led me to the final flag with help from a hacker and ChatNPT.

---

## Lessons Learned

This challenge highlighted how manipulating memory in retro systems can lead to unexpected behavior — especially overflows. Understanding how registers store digits and how to control them with an emulator gave me full control over the game’s logic. Plus, this was a fun nod to old-school hacking tricks!
