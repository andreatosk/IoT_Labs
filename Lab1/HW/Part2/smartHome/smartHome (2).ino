//solo pin 7 per interrupt PIR
//pin 2 e 3 per i2c
#include <math.h>
#include <LiquidCrystal_PCF8574.h>

LiquidCrystal_PCF8574 lcd(0x27);

//PINS
const int tempPin = A1;
const int fPin = 11;
const int ledPin = 10;
const int pirPin = 7;
const int soundPin = 9;
//const int testPin = 13;


const int maxlen = 10;
const int timestamp = 2;
const int timeout_pir = 30000;

//Costanti Temperatura
const int B = 4275;
const long int R0 = 100000;

//setPoint in utilizzo nel presente



//Convenzione:
//c per Condizionamento r per Riscaldamento
//P per presenza, a per assenza
//min e max per valori minimi e massimi
short cpMinSetPoint = 20;   //Condizionamento
short cpMaxSetPoint = 26;

short rpMinSetPoint = 28;   //Riscaldamento
short rpMaxSetPoint = 20;

short caMinSetPoint = 24;   //Condizionamento
short caMaxSetPoint = 30;

short raMinSetPoint = 24;   //Riscaldamento
short raMaxSetPoint = 16;

short cMinSetPoint = caMinSetPoint;
short cMaxSetPoint = caMaxSetPoint;
short rMinSetPoint = raMinSetPoint;
short rMaxSetPoint = raMaxSetPoint;

volatile int tot_count = 0;

//Valori di presenza
boolean PIRpresence = 0;
boolean soundPres = 0;
boolean Ppres = 0;

//Gestione dei suoni
long sound_interval = 120000; //2 min
long timeout_sound = 30000; //60 min
long V[maxlen];
short start = 0, endl = 0;


//Timer per temporizzazione
int t, tto;
long int timer;
int timerMult = 0;
int lcd_timer;


long t1; //timer casuali

//flag per gestire il cambio dei setPoint
short changed = 0;

//Utilizzo risorse
float temperature;
int percFan;
int percLed;

//Input
char inputC;
int i;
int v[4];
boolean changingVal = 0;
char choice;

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



void soundOccurrence() {
  if (digitalRead(soundPin) == LOW  && ((t1 - timer) >= (timerMult * 500))) {
    V[endl] = millis();
    endl++;

    start = start % (maxlen - 1);


    if (abs(endl - start) == (maxlen - 1) && ( V[endl] - V[start] < sound_interval)) {
      soundPres = 1;
      tto = millis();
      Serial.println((V[endl] - V[start]) / 1000);
    }

    if (endl > (maxlen - 1)) {
      endl = 0;
    }


    if (start >= endl)
      start++;

    if (endl == start - 1) {
      if (V[endl] - V[start] < sound_interval)
        soundPres = 1;
      tto = millis();
    }
  }

  else {

    if (tto > timeout_sound && soundPres == 1) {
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
  //double R = (val-cpMinSetPoint)/(cpMaxSetPoint-cpMinSetPoint);
  //double y = (255*R) ;
  return map(val, cpMinSetPoint, cpMaxSetPoint, 0, 255);
}

double tempMapLed(float val) {
  //a = third, b = fourth
  //c = 0 d = 255
  //double R = (val-rpMinSetPoint)/(rpMinSetPoint-rpMaxSetPoint);
  //double y = (255*R) ;
  return map(val, rpMaxSetPoint, rpMinSetPoint, 0, 255);
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


//TODO: Aggiungere il ritorno a 0
void switchP() {
  if (PIRpresence || soundPres) {
    Ppres = 1;
    if (changed == 0) {
      cpMinSetPoint = caMinSetPoint;
      cpMaxSetPoint = caMaxSetPoint;
      rpMinSetPoint = raMinSetPoint;
      rpMaxSetPoint = raMaxSetPoint;
      changed = 1;

      Serial.println("Modalità comfort.");
      printSetPoint();
    }
    if (!PIRpresence && !soundPres) {
      Ppres = 0;
      if (changed == 0) {
        cpMinSetPoint = caMinSetPoint;
        cpMaxSetPoint = caMaxSetPoint;
        rpMinSetPoint = raMinSetPoint;
        rpMaxSetPoint = raMaxSetPoint;
        changed = 1;
        Serial.println("Modalità mantenimento.");
        printSetPoint();
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

  lcd_timer = (timer - t1) / 1000;
  Serial.println(timer);
  Serial.println(t1);

  if (lcd_timer % 2 == 0) {

    lcd.clear();
    lcd.print("AC m:");
    lcd.print(cpMinSetPoint);
    lcd.print(" M:");
    lcd.print(cpMaxSetPoint);
    lcd.setCursor(0, 1);
    lcd.print("HT m:");
    lcd.print(rpMinSetPoint);
    lcd.print(" M:");
    lcd.print(rpMaxSetPoint);
  }

  Serial.println("Rumore");
}

void Serialfree() {
  while (Serial.available())
    Serial.read();
}

void printSetPoint() {
  Serial.println("Attuali setPoint:"); 
  Serial.println();
  Serial.println("A regime:");
  Serial.println("Condizionamento:");
  Serial.print("(");
  Serial.print(cpMinSetPoint);
  Serial.print(",");
  Serial.print(cpMaxSetPoint);
  Serial.println(")");


  Serial.println("Riscaldamento");
  Serial.print("(");
  Serial.print(rpMinSetPoint);
  Serial.print(",");
  Serial.print(rpMaxSetPoint);
  Serial.println(")");  
  
  Serial.println();
  Serial.println("A risparmio energetico:");
  Serial.println("Condizionamento:");
  Serial.print("(");
  Serial.print(caMinSetPoint);
  Serial.print(",");
  Serial.print(caMaxSetPoint);
  Serial.println(")");


  Serial.println("Riscaldamento");
  Serial.print("(");
  Serial.print(raMinSetPoint);
  Serial.print(",");
  Serial.print(raMaxSetPoint);
  Serial.println(")");
  Serial.println();
  
}

void printCurrentSetPoint(){
  Serial.println("Attuali setPoint in utilizzo:"); 
  Serial.println();
  
  Serial.println("Condizionamento:");
  Serial.print("(");
  Serial.print(cMinSetPoint);
  Serial.print(",");
  Serial.print(cMaxSetPoint);
  Serial.println(")");


  Serial.println("Riscaldamento");
  Serial.print("(");
  Serial.print(rMinSetPoint);
  Serial.print(",");
  Serial.print(rMaxSetPoint);
  Serial.println(")");  
  Serial.println();
  
}

void checkInput() {
  printSetPoint();

  Serial.println("Inserire 1 o 2 se si vogliono rispettivamente modificare i valori a regime o i valori a risparmio energetico");
  Serialfree();
  while(!Serial.available());
  choice = Serial.peek();
  Serialfree();
  
  Serial.println("Inserire in ordine da 1 a 4 i valori di minCond, maxCond, minRisc, maxRisc");
  Serialfree();
  while (true) {
    changingVal = 1;
    int i = 0;
    while (i < 4) {
      Serial.print("Inserisci il ");
      Serial.println(i + 1);
      Serial.read();
      Serial.read();
      while (Serial.available() == 0);
      v[i] = Serial.parseInt();
      i++;
    }

    if(choice == '1'){
      cpMinSetPoint = v[0];
      cpMaxSetPoint = v[1];
      rpMinSetPoint = v[2];
      rpMaxSetPoint = v[3];
     }
    if(choice == '2'){
      caMinSetPoint = v[0];
      caMaxSetPoint = v[1];
      raMinSetPoint = v[2];
      raMaxSetPoint = v[3];
     }

    if (i == 4)
      break;

    if (Serial.available() && Serial.peek() == '-')
      break;
  }
  printSetPoint();
  changingVal = 0;
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
  printCurrentSetPoint();

  Serial.println("Inserire il carattere + se si vuole inserire dei setPoint diversi.");
  timer = millis();
}

void loop() {
  if (!changingVal) {
    t1 = millis();
    
    switchP();
    tempRegulator(tempCalc());
    soundOccurrence();


    //test();
    //lcdShow();
  }
  if (Serial.available() > 0 && Serial.peek() == '+') {
    Serialfree();
    checkInput();
  }
}
