# Recover the Web Ring: Open Boria Mine Door  
**SANS Holiday Hack Challenge 2022 – KringleCon V: Golden Rings**  
**Difficulty:** 🎄🎄🎄

## Overview  
This challenge focused on bypassing six browser-based visual input locks using a mix of HTML/JavaScript analysis, creative input injection, and client-side sanitization bypass techniques. Each lock was rendered in an iframe and had different filtering mechanisms and visual challenges.

---

## Lock Solutions

### 🔒 Lock #1 – Hidden Clue in HTML Comment  
Examining the HTML source revealed a comment:

```html
<!-- @&@&&W&&W&&&& -->
```

Entering this string in the input field solved Lock 1.

---

### 🔒 Lock #2 – CSS-Based White Box  
Here I tested basic HTML injection with a white rectangle:

```html
<div style="background:white; width:1000px; height:1000px"></div>
```

This filled the required space and passed validation.

---

### 🔒 Lock #3 – SVG Rectangle Injection  
The next lock required use of SVG to bypass stricter filtering:

```html
<svg width="1000" height="1000"><rect width="1000" height="1000" fill="blue" /></svg>
```

---

### 🔒 Lock #4 – Complex SVG Drawing  
This challenge built on Lock 3 but needed more specific patterns:

```html
<svg width="1000" height="1000">
  <rect y=23 width="1000" height="25" fill="#00ff00" />

  <rect y=60 width="1000" height="25" fill="red" />
  <rect y=60 x=190 width="10" height="1000" fill="red" />

  <rect y=100 width="180" height="25" fill="blue" />
  <rect y=100 x=140 width="10" height="1000" fill="blue" />
</svg>
```

---

### 🔒 Lock #5 – Bypassing Input Sanitization with Burp Suite  
Client-side sanitization blocked input in the browser. Using Burp Suite to inject directly at the request layer bypassed this:

```html
<svg width="1000" height="1000">
  <rect width="10" height="1000" fill="red" />
  <rect y=40 width="1000" height="10" fill="red" />

  <rect y=160 x=30 width="1000" height="10" fill="blue" />
  <rect y=50 x=190 width="10" height="1000" fill="blue" />
</svg>
```

![Lock 5](imgs/lock5.png)

---

### 🔒 Lock #6 – Similar Technique with Minor Adjustment  
Same bypass technique via Burp Suite, but with new drawing coordinates:

```html
<svg width="1000" height="1000">
  <rect y=40 width="1000" height="10" fill="white" />
  <rect y=130 width="1000" height="10" fill="blue" />
</svg>
```

![Lock 6](imgs/lock6.png)

---

## Final Result  
After solving all six locks using a mix of HTML inspection, visual crafting with SVG, and input manipulation via proxy tools, the door to the Boria Mines was successfully opened.

![All Locks Solved](imgs/allLocks.png)
