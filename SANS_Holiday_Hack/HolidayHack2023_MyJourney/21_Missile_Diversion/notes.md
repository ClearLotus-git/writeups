# OBJECTIVE 22 - Missile Diversion

---

## Challenge:  
Reconfigure a satellite's missile system so that it targets the sun instead of Earth, thwarting Jack's plan on Space Island.

---

## Steps I Took:

**Step 1:**  
Connected to the NanoSat MO Base Station Tool and explored the Action and Parameter Service tabs. I found a debug field that accepted SQL input, indicating a potential SQL injection vulnerability.

**Step 2:**  
Tested various SQL injection strings through the Debug parameter, confirming the vulnerability and enumerating the database. I discovered multiple useful tables, including `pointing_mode`, which controls the missile's target.

**Step 3:**  
Found a serialized Java object in the `satellite_query` table and retrieved the associated parsing code. I reverse-engineered the structure and built a custom Java serializer that generated a valid payload to change the `numerical_mode` in `pointing_mode` from `0` (Earth) to `1` (Sun).

**Step 4:**  
Injected the hex-encoded serialized object via SQL, inserting it into the `satellite_query` table using an `INSERT` command. This successfully triggered the update and redirected the missile.

---

## Result:  
The missile was redirected away from Earth and safely pointed toward the Sun, completing the challenge.

---

## Lesson Learned:  
This challenge taught me how dangerous insecure deserialization and SQL injection can be—especially when combined. It also reinforced how important it is to isolate debugging tools and sanitize user input in production environments.
