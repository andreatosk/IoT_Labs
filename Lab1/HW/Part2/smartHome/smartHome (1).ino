//solo pin 7 per interrupt PIR
//pin 2 e 3 per i2c


#include <math.h>
#include <LiquidCrystal_PCF8574.h>

LiquidCrystal_PCF8574 lcd(0x27);


const int tempPin = A1;
const int fPin = 11;
const int ledPin = 10;
const int pirPin = 7;
const int soundPin = 9;
//const int testPin = 13;

const int maxlen = 10;
const int timestamp = 2;
const int timeout_pir = 30000;

const int B = 4275;               // B value of the thermistor
const long int R0 = 100000;      // R0 = 100k

int firstSetPoint = 20;
int secondSetPoint = 30;

int thirdSetPoint = 28;   //condizionamento
int fourthSetPoint = 18;


volatile int tot_count = 0;

short PIRpresence = 0;
short soundPres = 0;
short Ppres = 0;

long sound_interval = 120000; //2 min
long timeout_sound = 30000; //60 min
long V[maxlen];
short start = 0, endl = 0;


int t, tto;
long int timer;
int timerMult = 0;
int lcd_timer;


long t1; //timer casuali

short changed = 0;

float temperature;
int percFan;
int percLed;

//DA MODIFICARE
void PIRcheckPresence() {
  PIRpresence = !PIRpresence;
  if (PIRpresence == 1) {
    tot_count++;
  }
}

void resetTimers() {
  timer = millis();
  tto = millis();
  t = millis();
  timerMult = 0;
}



void soundOccurrence(){
    if(digitalRead(soundPin) == LOW  && ((t1-timer) >= (timerMult*500))){
        V[endl] = millis();
        endl++;

        start = start% (maxlen-1);
        
        
        if(abs(endl-start)==(maxlen-1) && ( V[endl]-V[start] < sound_interval)){
            soundPres = 1;
            tto = millis();
            Serial.println((V[endl]-V[start])/1000);
        }

        if(endl>(maxlen-1)){
            endl = 0;
        }

        
        if(start>=endl)
            start++;
        
        if(endl == start-1){
            if(V[endl]-V[start] < sound_interval)
            soundPres = 1;
            tto = millis();
        }
    }

    else{

      if(tto>timeout_sound && soundPres == 1){
        soundPres = 0;
      }
    }

}


/*
  void test(){
  if(digitalRead(testPin)==HIGH){
    soundPres = 1;
  }
  else
    soundPres = 0;
  }
*/

float tempCalc() {
  delay(timestamp * 500);
  int a = analogRead(tempPin);
  float R = 1023.0 / ((float)a) - 1.0;

  R = 100000.0 * R; //convert to temperature via datasheet ;
  temperature = 1.0 / (log(R / 100000.0) / B + 1 / 298.15) - 273.15;

  Serial.print("temperature = ");
  Serial.println(temperature);
  return temperature;
}

double tempMap(float val) {
  //a = first b = sec
  //c = 0 d = 255
  //double R = (val-firstSetPoint)/(secondSetPoint-firstSetPoint);
  //double y = (255*R) ;
  return map(val, firstSetPoint, secondSetPoint, 0, 255);
}

double tempMapLed(float val) {
  //a = third, b = fourth
  //c = 0 d = 255
  //double R = (val-thirdSetPoint)/(thirdSetPoint-fourthSetPoint);
  //double y = (255*R) ;
  return map(val, fourthSetPoint, thirdSetPoint, 0, 255);
}

//Voglio che il condizionatore sia mappato tra i valori del primo e secondo set point:
//first:second = 0:255

float tempRegulator(float currentTemp) {
  int c = (int)tempMap(currentTemp); //da levare
  if (c >= 255)
    c = 255;
  else if (c <= 0)
    c = 0;
  analogWrite(fPin, c);
  percFan = (c * 100) / 255;

  c = (int)tempMapLed(currentTemp);
  if (c >= 255)
    c = 255;
  else if (c <= 0)
    c = 0;
  analogWrite(ledPin, c);
  percLed = (c * 100) / 255;
  /*
    Serial.print("Utilizzo del fan: ");
    Serial.print(percFan);
    Serial.println("% ");
    Serial.print("Utilizzo del led: ");
    Serial.print(percLed);
    Serial.println("% ");
  */
}

void switchP() {
  if (PIRpresence || soundPres) {
    Ppres = 1;
    if (changed == 0) {
      firstSetPoint = 20;
      secondSetPoint = 24;
      changed = 1;

      Serial.println("Modalità comfort.");
      Serial.print("Attuali setPoint: (");
      Serial.print(firstSetPoint);
      Serial.print(",");
      Serial.print(secondSetPoint);
      Serial.println(")");
    }
    if (!PIRpresence && !soundPres) {
      Ppres = 0;
      if (changed == 0) {
        firstSetPoint = 20;
        secondSetPoint = 30;
        changed = 1;
        Serial.println("Modalità mantenimento.");
        Serial.print("Attuali setPoint: (");
        Serial.print(firstSetPoint);
        Serial.print(",");
        Serial.print(secondSetPoint);
        Serial.println(")");
      }
    }
  }
}


void lcdShow() {
  
    lcd.clear();
    lcd.print("T:");
    lcd.print(temperature);
    lcd.print(" Pres:");
    lcd.print(Ppres);
    lcd.setCursor(0, 1);
    lcd.print("AC:");
    lcd.print(percFan);
    lcd.print("% HT:");
    lcd.print(percLed);
    lcd.print("%  ");

    lcd_timer = (timer-t1)/1000;
    Serial.println(timer);
    Serial.println(t1);
    
    if(lcd_timer%2 == 0){

    lcd.clear();
    lcd.print("AC m:");
    lcd.print(firstSetPoint);
    lcd.print(" M:");
    lcd.print(secondSetPoint);
    lcd.setCursor(0, 1);
    lcd.print("HT m:");
    lcd.print(thirdSetPoint);
    lcd.print(" M:");
    lcd.print(fourthSetPoint);
    }
  
  Serial.println("Rumore");
}

void setup() {
  Serial.begin(9600);
  pinMode(tempPin, INPUT);
  pinMode(fPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(pirPin, INPUT);
  pinMode(soundPin, INPUT);
  
  //  pinMode(testPin,INPUT); //DEBUGGING
  while (!Serial);

  lcd.begin(16, 2);
  lcd.setBacklight(255);
  lcd.home();
  lcd.clear();
  attachInterrupt(digitalPinToInterrupt(pirPin), PIRcheckPresence, CHANGE);

  Serial.print("Attuali setPoint: (");
  Serial.print(firstSetPoint);
  Serial.print(",");
  Serial.print(secondSetPoint);
  Serial.println(")");

  timer = millis();
}

void loop() {
  t1 = millis();

  Serial.println(digitalRead(pirPin));
  tempRegulator(tempCalc());
  soundOccurrence();
  switchP();

  //test();
  //lcdShow();
}
