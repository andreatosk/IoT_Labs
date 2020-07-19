#include <Process.h>
#include <Bridge.h>

Process r;
char json[150];

void setup(){
  Serial.begin(9600);
  while(!Serial) continue;
  strcpy(json,
   "{\"device_id\":\"arduino\",\"resources\":[\"temperature\",\"led\",\"heating\",\"fan\",\"setpoints\",\"people\"],\"endpoints\":[\"/tiot/18/temperature\",\"/tiot/18/led\",\"/tiot/18/heating\",\"/tiot/18/fan\",\"/tiot/18/setpoints\",\"/tiot/18/people\"]}");
  
  r.begin("curl");
  r.addParameter("http://127.0.0.1/8080/devices");
  r.addParameter("--request");
  r.addParameter("PUT");
  r.addParameter("--data");
  r.addParameter(json);

}

void loop(){
  r.run();
  delay(1000*60);
}
