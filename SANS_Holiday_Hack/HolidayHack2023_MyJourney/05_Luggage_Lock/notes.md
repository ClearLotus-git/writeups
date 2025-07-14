# OBJECTIVE 6 - Luggage Lock



## OBJECTIVE
Help Garland Candlesticks on the Island of Misfit Toys get back into his luggage by finding the correct position for all four dials.

## HINTS

Hints provided for Objective 6
    Chris Elgee's [talk](https://www.youtube.com/watch?v=ycM1hBSEyog) regarding his and his wife's luggage. 


---

## My Approach

### Method 1: Manual Lock Picking 
I began by following the guidance from Chris Elgee’s lockpicking talk. The idea is to apply light pressure on the lock’s button and slowly rotate each of the four wheels until resistance is felt. This indicates a likely correct number for that dial. I repeated this for all four digits until the correct combination was found, and the lock opened successfully.

This method simulates a physical lockpick approach, encouraging attention to detail and feel, even in a virtual simulation.

### Method 2: JavaScript Brute-Force (For Fun)

While not practical in the real world, this environment allowed a script-based shortcut. I opened the developer console in the browser and ran a JavaScript snippet to try every possible combination automatically:

```javascript
for(a=0;a<10;a++)for(b=0;b<10;b++)for(c=0;c<10;c++)for(d=0;d<10;d++)
  socket.emit('message', { "Type":"Open", "Combo":""+a+b+c+d });
```

This brute-force strategy loops from 0000 to 9999 and sends attempts directly to the backend via WebSocket. The correct combination is eventually hit, unlocking the luggage.

## Result

I was able to unlock the suitcase using both the manual lockpicking approach and the script automation. The inside revealed a fun digital reward!

## Lessons Learned

This was a fun crossover between physical security principles and technical scripting. It showed how lockpicking knowledge can be applied virtually — and how automation can provide a fallback (though less elegant) solution.
