## Objective 2 – Snowball Hero



---

###  Objective

The goal of this challenge is to make your way to Christmas Island and interact with Morcel Nougat, who introduces a new multiplayer snowball fight game. The mission: join forces with another player to take down Santa using strategy and skill.

---

###  Hints

The game hinted that adjusting certain client-side variables could give players a significant advantage. There was also mention of a single-player mode that might allow players to take on Santa alone.

---

###  Solutions

There are a few effective ways to complete this objective depending on how creative you want to get.

---

####  Solution 1: Partner Up and Play

The most straightforward approach is to queue up with a random player and take on Santa together. This introduces some unpredictability but stays true to the spirit of the game — teamwork and coordination.

---

####  Solution 2: Summon Elf the Dwarf + Client Tweaks (Solo Mode Hack)
1. Navigate to the snowball fight room with a link like the following:

   ```
   https://hhc23-snowball.holidayhackchallenge.com/room/?username=myname&roomId=xxxxxxx&roomType=public&gameType=co-op&id=...&dna=...&singlePlayer=false
   ```

2. Before the game starts, manually change the `singlePlayer=false` to `singlePlayer=true` in the URL. This should trigger a helper bot named Elf the Dwarf to join your team.

3. Open your browser’s dev console and run the following commands to gain an advantage:

   ```javascript
   player.health = 999;
   elfThrowDelay = 999999;
   santaThrowDelay = 999999;
   playersHitBoxSize = [0, 0, 0, 0];
   ```

   These tweaks make you nearly invincible and prevent the elves and Santa from being able to attack you effectively.

4. Sometimes Elf the Dwarf doesn’t spawn properly, but you’ll still have the advantage from these variables.

---

####  Solution 3: Auto Win via WebSocket Manipulation

1. Create and join a new room.
2. Open the same room in incognito mode using a slightly modified ID to act as a second player.
3. In the dev tools console for both browser sessions, paste and run the following script:

   ```javascript
   function godMode(){
       player.health = 999;
   }

   function defeat_elves(){
       const keys = Object.keys(allElves);
       for (let i = 0; i < keys.length; i++) {
           const elfId = keys[i];
           const msg = {
               "a": "e",
               "i": player.playerId,
               "eid": elfId
           };
           ws.send(JSON.stringify(msg));
       }
   }

   function defeat_santa(){
       const msg = {
           "a": "s",
           "i": player.playerId
       };
       ws.send(JSON.stringify(msg));
   }

   function autoWin(){
       godMode();
       defeat_elves();
       defeat_santa();
   }

   const interval = setInterval(autoWin, 1000);
   ```

4. The script fakes hits using WebSocket messages and takes out enemies without needing to actually play.

---

###  Outcome

With these approaches, I completed the objective easily—either by teaming up or automating the battle entirely using client-side manipulation.

---

###  Takeaway

This challenge highlights how vulnerable browser-based games can be to client-side attacks. Whether you're exploiting variables or abusing WebSockets, knowing where to look can give you full control over the game.

