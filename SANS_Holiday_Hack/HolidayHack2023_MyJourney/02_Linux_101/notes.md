## Objective 3 – Linux 101


---

###  Objective  
I met Ginger Breddie inside Santa’s Shack on Christmas Island, located in the southwest corner of Frosty’s Beach. He needed help with a series of Linux terminal tasks. My goal was to track down and eliminate mischievous trolls by following various system clues.

---

###  Procedure

```bash
# Start the challenge
yes

# List files in home directory
ls
# Output: HELP  troll_19315479765589239  workshop

# Peek inside the troll file
cat troll_19315479765589239
# Output: troll_24187022596776786

# Remove the original troll
rm troll_19315479765589239

# Show current directory
pwd
# Output: /home/elf

# Look for hidden files
ls -a
# Output includes: .troll_5074624024543078

# Check command history
history
# Output includes: echo troll_9394554126440791

# Look for trolls in environment variables
printenv | grep -i troll
# Output: z_TROLL=troll_20249649541603754

# Move into workshop directory
cd workshop/

# Search toolboxes for troll
grep -i troll *
# Output: tRoLl.4056180441832623

# Make present_engine executable and run it
chmod +x present_engine && ./present_engine
# Output: troll.898906189498077

# Go to electrical and rename fuse
cd electrical/
mv blown_fuse0 fuse0

# Create a symlink
ln -s fuse0 fuse1

# Copy symlink to fuse2
cp fuse1 fuse2

# Add troll repellent
echo "TROLL_REPELLENT" > fuse2

# Search for troll files in troll_den
find /opt/troll_den/ -iname "*troll*"

# Find file owned by troll
find /opt/troll_den/ -user troll

# Find file between 108K and 110K
find /opt/troll_den/ -size +108k -size -110k

# Check running processes
ps -fae
# Output includes: 14516_troll

# See listening ports
netstat -an
# Output includes: 0.0.0.0:54321 LISTEN

# Interact with the local HTTP server
curl localhost:54321
# Output: troll.73180338045875

# Kill the troll process
kill <PID>
exit
```

---

###  Outcome  
I used standard Linux commands to hunt and eliminate each troll. From environment variables to network sockets and symlinks, the challenge covered a wide range of CLI basics.

---

###  Lesson Learned  
This was a hands-on, practical refresher for working with the Linux shell. It tested command history, file manipulation, permissions, process control, and basic grep/find usage — all while chasing down virtual trolls.

