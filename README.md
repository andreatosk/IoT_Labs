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
    "device 1":{
     "device_id":"device 1",
      "resources":[],
      "endpoints":[],
      "insertion_timestamp":"milliseconds"
   
    }
}
```
Services
```json
{
    "service 1":{ 
     "service_id":"service 1",
      "description":"This is a description",
      "endpoints":[],
      "insertion_timestamp":"milliseconds"
   
    }
}
```

Users
```json
{
    "user 1":{
      "user_id":"user 1",
      "name":"John",
      "surname":"Doe",
      "email":[]
   
    }
}
```
