# IoT_Labs
Current Lab structure:
```bash
├─Lab1
├───HW
├─────Part1
├───────Es1
├─────────2led
├───────Es2
├─────────2led
├───────Es3
├─────────PIR
├───────────PIR
├───────Es4
├─────────fan
├───────Es5
├─────────temperatura
├───────Es6
├─────────temperatura
├─────Part2
├───────smartHome
├─────Part3
├───────3_1
├───SW
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
├─LabSW2
├───1
├─────__pycache__
├───2
├───3
├─LabSW3
└───3

```

# JSON Templates:
Devices
```json
{
    "device_id_one" : {
     "device_id" : "device_id_one",
      "resources" : ["resource_one", "resource_two', ...],
      "endpoints" : ["endpoint_one", "endpoint_two", ...],
      "insertion_timestamp" : "seconds_since_epoch"
    },
    "device_id_two":{
     "device_id" : "device_id_two",
      "resources" : ["resource_one", "resource_two", ...],
      "endpoints" : ["endpoint_one", "endpoint_two", ...],
      "insertion_timestamp" : "seconds_since_epoch"
    },
    ...
}
```
Services
```json
{
    "service_id_one" : { 
     "service_id" : "service_id_one",
      "description" : "This is a description",
      "endpoints" : ["endpoint_one", "endpoint_two", ...],
      "insertion_timestamp" : "seconds_since_epoch"
    },
    "service_id_two" : { 
     "service_id" : "service_id_two",
      "description" : "This is a description",
      "endpoints" : ["endpoint_one", "endpoint_two", ...],
      "insertion_timestamp" : "seconds_since_epoch"
    },
    ...
}
```

Users
```json
{
    "user_id_one" : {
      "user_id" : "user_id_one",
      "name" : "John",
      "surname" : "Doe",
      "email" : ["email_one", "email_two", ...]
    },
    "user_id_two" : {
      "user_id" : "user_id_two",
      "name" : "Doe",
      "surname" : "John",
      "email" : ["email_one", "email_two", ...]
    },
    ...
    
}
```
