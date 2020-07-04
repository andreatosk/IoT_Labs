#include <TimerOne.h>

const int RLED_PIN = 12;
const int GLED_PIN = 11;

const float R_HALF_PERIOD = 1.5;
const float G_HALF_PERIOD = 3.5;

int greenLedState = LOW;
int redLedState = LOW;

char c;

void blinkGreen(){
  greenLedState = !greenLedState;
  digitalWrite(GLED_PIN, greenLedState);
  
}
void setup() {
  
  pinMode(RLED_PIN,OUTPUT);
  pinMode(GLED_PIN,OUTPUT);
  Timer1.initialize(G_HALF_PERIOD * 1e06);
  Timer1.attachInterrupt(blinkGreen);

  Serial.begin(9600);
  while(!Serial);
  
  
}

void loop() {
  redLedState = !redLedState;
  digitalWrite(RLED_PIN, redLedState);
  delay(R_HALF_PERIOD * 1e03);

  if(Serial.available()>0){
    c = Serial.peek();
    Serial.read();
    if(c=='R'){
      Serial.print("Red led State:");
      Serial.println(redLedState);
    }
    else if(c=='G'){
      Serial.print("Green led State:");
      Serial.println(greenLedState);
    }
  }
  c = ' ';

}
