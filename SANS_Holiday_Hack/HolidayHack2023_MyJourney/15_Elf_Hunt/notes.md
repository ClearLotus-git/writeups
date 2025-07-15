# OBJECTIVE 16 - Elf Hunt  

## OBJECTIVE  
Piney Sappington needs help understanding JSON Web Tokens. Hack the Elf Hunt game and score at least 75 points.

## Hints

Hints provided for Objective 16  
- Learn how JWTs work with [PortSwigger’s JWT Guide](https://portswigger.net/web-security/jwt).  
- The elves are fast — maybe there’s a way to slow them down... like tweaking a magic cookie?

---

## My Approach

This challenge is all about manipulating a **JWT (JSON Web Token)** that’s used to control elf speed in the game.

### Step 1: Inspect the Cookie  
Opening the browser's developer tools and checking storage, I found a cookie named:

```
ElfHunt_JWT
```

It looked like this:

```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzcGVlZCI6LTUwMH0.
```

This is clearly a JWT. It’s made up of three parts:
1. Header
2. Payload
3. Signature (which in this case is **missing**)

### Step 2: Decode the Payload  
The second section (`eyJzcGVlZCI6LTUwMH0`) is the **payload**, which is base64-encoded. Using [CyberChef](https://gchq.github.io/CyberChef/), I decoded it:

```json
{"speed": -500}
```

That explains why the elves are moving so fast — negative speed makes them hyperactive.

### Step 3: Modify the Payload  
Because this JWT is unsigned (i.e., `alg: none`), it’s not protected. That means I can edit the payload freely.

So, I changed the speed to a positive number:

```json
{"speed": 5}
```

Re-encoded the modified payload using base64 (no padding), then rebuilt the full token with the original header:

```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzcGVlZCI6NX0.
```

I replaced the cookie value with the modified JWT in browser storage, refreshed the page, and now the elves were moving slowly.

### Step 4: Win the Game  
With slow-moving elves, it was easy to reach 75+ points in the game and complete the challenge.

---

## Result

I successfully tampered with an unsigned JWT by modifying the base64-encoded payload. By setting a slower speed, I was able to catch the elves easily and complete the objective.

---

## Lessons Learned

This was a great demonstration of how dangerous it is to use unsigned JWTs (`alg: none`). Without a signature, anyone can manipulate the token contents, leading to logic abuse or privilege escalation. Always validate JWTs server-side and avoid relying on client-modifiable tokens for critical gameplay mechanics or access control.

