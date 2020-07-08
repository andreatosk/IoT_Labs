#include <ArduinoJson.h>
#include <Bridge.h>
#include <BridgeClient.h>
#include <BridgeServer.h>

const int tempPin = A1;
const int ledPin = 8;
const int capacity = JSON_OBJECT_SIZE(2) + JSON_ARRAY_SIZE(1) + JSON_OBJECT_SIZE(4) + 40;
const int timestamp = 10;

const int B=4275;                 // B value of the thermistor
const long int R0 = 100000;      // R0 = 100k


DynamicJsonDocument doc_snd(capacity);
BridgeServer server;


int first,second ;

float calcTemp(){
  int a = analogRead(tempPin);
  
  float R = 1023.0/((float)a)-1.0;
  
  R = 100000.0*R;//convert to temperature via datasheet ;
  float temperature=1.0/(log(R/100000.0)/B+1/298.15)-273.15;
  return temperature;
}

void printResponse(BridgeClient client, int code, String body) {
  client.println("Status: " + String(code));
  if (code == 200) {
    client.println(F("Content-type: application/json; charset=utf-8"));
    client.println();
    client.println(body);
  }
}

String sendMlEncode(String res, float v, String unit){
  doc_snd.clear();
  second = millis();
  doc_snd["bn"] = "tiot_18";

   doc_snd["e"][0]["n"] = res;
   doc_snd["e"][0]["t"] = second-first;
   doc_snd["e"][0]["v"] = v;
  
    if(unit != ""){
      doc_snd["e"][0]["u"]=unit;
    }
    else
      doc_snd["e"][0]["u"]=(char*) NULL;

    String output;
    serializeJson(doc_snd, output);
    return output;
}

//Processa tutto ciò che segue //http://hostname:porta/arduino/...

void process(BridgeClient client) {
  first = millis();
  String command = client.readStringUntil('/'); //parse prima parte
  command.trim(); //cancella \n


  if (command == "led") {
    int val = client.parseInt();
    if (val == 0 || val == 1) {
      digitalWrite(ledPin, val);
      printResponse(client, 200, sendMlEncode(F("led"), val, F("")));
    }
    else
      printResponse(client, 400,"");
  }
  else if (command == "temperature") {
    printResponse(client,200,sendMlEncode(F("temperature"),calcTemp(),F("")));
  }
  else
    //risposta not found
    printResponse(client, 404, "");
}


void setup() {
  // put your setup code here, to run once:
  pinMode(ledPin, OUTPUT);
  pinMode(tempPin, INPUT);

  digitalWrite(ledPin, LOW);
  Bridge.begin();
  digitalWrite(ledPin, HIGH);

  //server.listenOnLocalhost();
  server.begin();

}

void loop() {
  BridgeClient client = server.accept();

  if (client) {
    process(client);
    client.stop();
  }

  delay(50);
}
