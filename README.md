# IoT_Labs
Current Lab structure:
```bash
.
├─Hardware
├───Part1
├─────Es1
├───────2led
├─────Es2
├───────2led
├─────Es3
├───────PIR
├─────────PIR
├─────Es4
├───────fan
├─────Es5
├───────temperatura
├─────Es6
├───────temperatura
├───Part2
├─────smartHome
├───Part3
├─Software
├───Part1
├─────Es1
├─────Es2
├─────Es3
├─────Es4
├───────css
├───────dashboard
├───────img
├───────js
├───────plugins
├─────────freeboard
├─────────mqtt
├─────────thirdparty
├───Part2
├─────1
├─────2
├─────3
├─────5
├─────6
├───Part3
├─────3
├───Part4
├─────TelegramBot
└─────Weather

```

# Postman Collection Request
It is possible to import this collection in Postman to quickly access some prototype request to test and interact with the APIs

# Telegram Bot
To try the bot, first install the Python APIs on which the bot relies:
```bash
pip install python-telegram-bot
```
Then, launch "main.py" and "bot.py" cointained in /TelegramBot/ and start a chat from the following link:
```bash
https://t.me/polito_iotlabs_invokecatalog_bot
```
Further explaination will be given by using the "/help" command in chat

# JSON Templates:
Devices
```json
{
    "device_id_one" : {
     "device_id" : "device_id_one",
      "resources" : ["resource_one", "resource_two", "other_resources"],
      "endpoints" : ["endpoint_one", "endpoint_two", "other_resources"],
      "insertion_timestamp" : "seconds_since_epoch"
    },
    "device_id_two":{
     "device_id" : "device_id_two",
      "resources" : ["resource_one", "resource_two", "other_resources"],
      "endpoints" : ["endpoint_one", "endpoint_two", "other_endpoints"],
      "insertion_timestamp" : "seconds_since_epoch"
    },
    "other_devices_ids"
}
```
Services
```json
{
    "service_id_one" : { 
     "service_id" : "service_id_one",
      "description" : "This is a description",
      "endpoints" : ["endpoint_one", "endpoint_two", "other_endpoints"],
      "insertion_timestamp" : "seconds_since_epoch"
    },
    "service_id_two" : { 
     "service_id" : "service_id_two",
      "description" : "This is a description",
      "endpoints" : ["endpoint_one", "endpoint_two", "other_endpoints"],
      "insertion_timestamp" : "seconds_since_epoch"
    },
    "other_services_ids"
}
```

Users
```json
{
    "user_id_one" : {
      "user_id" : "user_id_one",
      "name" : "John",
      "surname" : "Doe",
      "email" : ["email_one", "email_two", "other_emails"]
    },
    "user_id_two" : {
      "user_id" : "user_id_two",
      "name" : "Doe",
      "surname" : "John",
      "email" : ["email_one", "email_two", "other_emails"]
    },
    "other_users_ids"
}
```

Weather
```json
{
  "temperature":"value + ' deg Cel'",
  "wind":"value + 'm/s' + direction",
  "weather":"current_weather",
  "humidity":"'humidity' value + '%'"
}
```

Actuation and sensing messages:
-Template:
```json
{"bn":"ID of master in this communication",
  "e":[
    {
    "n":"led",
    "t":"timestamp",
    "v":"value",
    "u":"unit"
    }
  ]
}
```
-Available values for field "n" are the last fields of the topics (following)


Endpoints
-Template:
```json
{
  "description":"This is a description",
  "value":"some endpoint"
}
```
-Available descriptions are the last fields of the topics (following)

#MQTT topics:
```
- /tiot/18/temperature
- /tiot/18/led (normal led)
- /tiot/18/heating (thermistor)
- /tiot/18/fan
- /tiot/18/setpoints
- /tiot/18/people (PIR + noise)
```