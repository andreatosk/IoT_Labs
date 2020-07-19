#include <ArduinoJson.h>
#include <Bridge.h>
#include <BridgeClient.h>
#include <BridgeServer.h>
#include <Process.h>

const int tempPin = A1;
const int ledPin = 8;
const int capacity = JSON_OBJECT_SIZE(2) + JSON_ARRAY_SIZE(1) + JSON_OBJECT_SIZE(4) + 40;
const int timestamp = 10;

const int B=4275;                 // B value of the thermistor
const long int R0 = 100000;      // R0 = 100k
unsigned long first;
unsigned long second;

DynamicJsonDocument doc_snd(capacity);

int my_curl(String data, String address)
{
    Process p;
    p.begin("curl");
    p.addParameter("-H");
    p.addParameter("Content-Type:application/json");
    p.addParameter("-X");
    p.addParameter("POST");
    p.addParameter("-d");
    p.addParameter(data);
    p.addParameter(address);
    p.run();
    return(p.exitValue());
}

float calcTemp(){
  int a = analogRead(tempPin);
  
  float R = 1023.0/((float)a)-1.0;
  
  R = 100000.0*R;//convert to temperature via datasheet ;
  float temperature=1.0/(log(R/100000.0)/B+1/298.15)-273.15;
  return temperature;
}


String sendMlEncode(float v){
  doc_snd.clear();
  second = millis();
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
  Bridge.begin();
  digitalWrite(ledPin, HIGH);

  first = millis();

}

void loop() {
    float temp = calcTemp();
    String data = sendMlEncode(temp);
    int exval = my_curl(data, "http://<hostname>:<port>/log");
    Serial.print("Curl exitval : ")
    Serial.println(exval)
    
    delay(1000);
}
