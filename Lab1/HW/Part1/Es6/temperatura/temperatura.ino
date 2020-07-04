
#include <math.h>
#include <LiquidCrystal_PCF8574.h>

LiquidCrystal_PCF8574 lcd(0x27);

const int pin = A1;
const int timestamp = 10;

const int B=4275;                 // B value of the thermistor
const int R0 = 100000;      // R0 = 100k

void setup() {
  
  Serial.begin(9600);
  pinMode(pin,INPUT);
  Serial.println("Lab 1.5 starting");

  lcd.begin(16,2);
  lcd.setBacklight(255);
  lcd.home();
  lcd.clear();
 }

void loop() {
  int a = analogRead(pin);
  float R = 1023.0/((float)a)-1.0;
  
  R = 100000.0*R;//convert to temperature via datasheet ;
  float temperature=1.0/(log(R/100000.0)/B+1/298.15)-273.15;
  
  lcd.print("Temperature:");
  lcd.print(temperature);
  
  delay(timestamp*1000);
  lcd.clear();
  
}
