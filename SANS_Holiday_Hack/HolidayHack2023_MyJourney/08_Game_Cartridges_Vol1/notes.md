# OBJECTIVE 9 - Game Cartridge Vol 1 #


## Challenge:
Find the first Gamegosling cartridge hidden in Tarnished Trove and complete the in-game puzzle to obtain the flag.

---

## Steps I Took:

I started by checking the source code and found the following line in `script.js`:
```javascript
const ROM_FILENAME = "rom/game.gb";
```
This told me the ROM file could be downloaded from:  
[https://gamegosling.com/vol1-uWn1t6xv4VKPZ6FN/rom/game.gb](https://gamegosling.com/vol1-uWn1t6xv4VKPZ6FN/rom/game.gb)

I downloaded the file and opened it in a Game Boy emulator. The emulator’s save/load state features made solving the puzzle much easier. The game involved sliding 7 blocks into their proper places.

Once I solved the puzzle, a QR code appeared on the screen. I scanned it using my phone, which led me to:  
[https://8bitelf.com/](https://8bitelf.com/)

That page displayed the flag.

---

## Result:
I successfully completed the block puzzle, scanned the QR code, and retrieved the flag:  
**`flag:santaconfusedgivingplanetsqrcode`**

---

## Lesson Learned:
Sometimes examining source code reveals hidden assets that can be used directly. Emulator tools like save states made this puzzle much more manageable, and combining both technical and observational skills was key to completing this objective.
