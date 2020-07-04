
#include <math.h>

const int pin = A1;
const int timestamp = 10;

const int B=4275;                 // B value of the thermistor
const int R0 = 100000;      // R0 = 100k

void setup() {
  
  Serial.begin(9600);
  pinMode(pin,INPUT);
  while(!Serial);
  Serial.println("Lab 1.5 starting");
}

void loop() {
  delay(timestamp*1000);
  int a = analogRead(pin);
  float R = 1023.0/((float)a)-1.0;
  
  R = 100000.0*R;//convert to temperature via datasheet ;
  float temperature=1.0/(log(R/100000.0)/B+1/298.15)-273.15;
  
  Serial.print("temperature = ");
  Serial.println(temperature);
}
