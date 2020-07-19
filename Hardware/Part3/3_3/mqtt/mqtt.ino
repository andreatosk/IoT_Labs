#include <ArduinoJson.h>
#include <Bridge.h>
#include <BridgeClient.h>
#include <BridgeServer.h>
#include <MQTTclient.h>


const int tempPin = A1;
const int ledPin = 8;
const int capacity = JSON_OBJECT_SIZE(2) + JSON_ARRAY_SIZE(1) + JSON_OBJECT_SIZE(4) + 40;
const int timestamp = 10;

const int B=4275;                 // B value of the thermistor
const long int R0 = 100000;      // R0 = 100k
unsigned long first;
unsigned long second;

MQTTclient mymqtt;


DynamicJsonDocument doc_snd(capacity);

void onMessage(String topic, String subtopic, String message){
    return;
}

float calcTemp(){
  int a = analogRead(tempPin);
  
  float R = 1023.0/((float)a)-1.0;
  
  R = 100000.0*R;//convert to temperature via datasheet ;
  float temperature=1.0/(log(R/100000.0)/B+1/298.15)-273.15;
  second = millis();
  return temperature;
}


String sendMlEncode(float v){
  doc_snd.clear();
  doc_snd["bn"] = "tiot_18";

   doc_snd["e"][0]["n"] = "temperature";
   doc_snd["e"][0]["t"] = second-first;
   doc_snd["e"][0]["v"] = v;
  
   doc_snd["e"][0]["u"] = "Cel";

    String output;
    serializeJson(doc_snd, output);
    return output;
}


void setup() {
  // put your setup code here, to run once:
  pinMode(ledPin, OUTPUT);
  pinMode(tempPin, INPUT);

  digitalWrite(ledPin, LOW);
  digitalWrite(ledPin, HIGH);

  mymqtt.begin("test.mosquitto.org",1883);
  first = millis();

  mymqtt.subscribe("/tiot/18/led",onMessage);
}


void loop() {
    float temp = calcTemp();
    String data = sendMlEncode(temp);
    
    mymqtt.publish("/tiot/18/temperature", data);
    
    delay(10000);
}
