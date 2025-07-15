# OBJECTIVE 9 - Game Cartridge Vol 1

## OBJECTIVE
Find the first Gamegosling cartridge hidden around Tarnished Trove and complete the game to recover the flag.

## Hints

Hints provided for Objective 9  
- Listen for the Gameboy cartridge detector’s sound when you're near buried treasure.  
- Explore the strange toys in Tarnished Trove.  
- Sometimes things need a little push.  
- QR code fixed? Make sure you scan it and see where it leads.

---

## My Approach

### Step 1: Locating the Cartridge  
Following the hints, I searched the strange toys scattered throughout the Tarnished Trove area. One of them revealed the hidden game cartridge.

### Step 2: Finding the ROM File  
I examined the JavaScript source code and found this line in `script.js`:

```javascript
const ROM_FILENAME = "rom/game.gb";
```

This pointed me to the downloadable ROM file located at:  
[https://gamegosling.com/vol1-uWn1t6xv4VKPZ6FN/rom/game.gb](https://gamegosling.com/vol1-uWn1t6xv4VKPZ6FN/rom/game.gb)

I downloaded the file and loaded it in a Game Boy emulator that supports save/load states, making the game more manageable.

### Step 3: Solving the Puzzle  
The game involved sliding seven blocks into the correct positions. After some careful movement and use of save states, I managed to complete the puzzle.

### Step 4: Scanning the QR Code  
Once the blocks were placed correctly, a full QR code appeared. Scanning it led me to this page:  
[https://8bitelf.com/](https://8bitelf.com/)

On that site was the flag needed to complete the objective:

```
flag:santaconfusedgivingplanetsqrcode
```

## Result

I successfully downloaded and loaded the ROM, completed the in-game puzzle, and retrieved the final flag by scanning the QR code.

## Lessons Learned

This challenge was a great example of combining code analysis, emulator tools, and puzzle-solving. It highlighted how reviewing source code can lead directly to exploitable content and how emulator features like save states can make retro-style challenges much more approachable.

