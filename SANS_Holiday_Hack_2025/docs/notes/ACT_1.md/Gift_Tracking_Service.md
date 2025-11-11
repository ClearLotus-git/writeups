Santa's Gift-Tracking Service Port Mystery

Difficulty: 1/5

Objective: Chat with Yuri near the apartment building about Santa's mysterious gift tracker and unravel the holiday mystery.


Task:

<img width="770" height="709" alt="image" src="https://github.com/user-attachments/assets/b2f08ceb-6d36-477e-a1f1-c0b53ad06594" />

```
======= Neighborhood Santa-Tracking Service =======

Oh no! Mischievous gnomes have tampered with the neighborhood's Santa-tracking service,
built by the local tinkerer to help everyone know when Santa arrives on Christmas Eve!

The tracking application was originally configured to run on port 8080, but after the
gnomes' meddling, it's nowhere to be found. Without this tracker, nobody in the neighborhood
will know when to expect Santa's arrival!

The tinkerer needs your help to find out which port the santa_tracker process is 
currently using so the neighborhood tracking display can be updated before Christmas Eve!

Your task:
1. Use the 'ss' tool to identify which port the santa_tracker process is 
   listening on
2. Connect to that port to verify the service is running

Hint: The ss command can show you all listening TCP ports and the processes 
using them. Try: ss -tlnp

Good luck, and thank you for helping save the neighborhood's Christmas spirit!

- The Neighborhood Tinkerer 🔧🎄
🎄 tinkerer @ Santa Tracker ~ 🎅 $
```

```
🎄 tinkerer @ Santa Tracker ~ 🎅 $ ss -ltnp
State                    Recv-Q                   Send-Q                                       Local Address:Port                                        Peer Address:Port                   Process                   
LISTEN                   0                        5                                                  0.0.0.0:12321                                            0.0.0.0:*
```

Connect using telnet: 

```
🎄 tinkerer @ Santa Tracker ~ 🎅 $ telnet 127.0.0.1 12321
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 1193
Connection: close

{
  "status": "success",
  "message": "\ud83c\udf84 Ho Ho Ho! Santa Tracker Successfully Connected! \ud83c\udf84",
  "santa_tracking_data": {
    "timestamp": "2025-11-11 21:19:11",
    "location": {
      "name": "Evergreen Estates",
      "latitude": 35.204823,
      "longitude": -72.447927
    },
    "movement": {
      "speed": "1670 mph",
      "altitude": "8349 feet",
      "heading": "305\u00b0 NW"
    },
    "delivery_stats": {
      "gifts_delivered": 1447827,
      "cookies_eaten": 6179,
      "milk_consumed": "924 gallons",
      "last_stop": "Candy Cane Court",
      "next_stop": "Frosty's Passage",
      "time_to_next_stop": "14 minutes"
    },
    "reindeer_status": {
      "rudolph_nose_brightness": "80%",
      "favorite_reindeer_joke": "Why don't reindeer like picnics? Because of all the ants!",
      "reindeer_snack_preference": "magical carrots"
    },
    "weather_conditions": {
      "temperature": "32\u00b0F",
      "condition": "Holiday sparkles"
    },
    "special_note": "Thanks to your help finding the correct port, the neighborhood can now track Santa's arrival! The mischievous gnomes will be caught and will be put to work wrapping presents."
  }
}Connection closed by foreign host.
```








