//solo pin 7 per interrupt PIR
//pin 2 e 3 per i2c
#include <math.h>
#include <LiquidCrystal_PCF8574.h>
#include <ArduinoJson.h>
#include <Bridge.h>
#include <BridgeClient.h>
#include <BridgeServer.h>
#include <MQTTclient.h>
#include <Process.h>
#include <MQTTClient.h>

LiquidCrystal_PCF8574 lcd(0x27);

//TEMPLATE REGISTRAZIONE
/*
{
    "device1" : {
     "device_id" : "device1",
      "resources" : ["resource_one", "resource_two", "other_resources"],
      "endpoints" : ["ep1", "ep2"],
      "insertion_timestamp" : "millis()"
    }
}
*/

const int capacityR = JSON_ARRAY_SIZE(2) + JSON_ARRAY_SIZE(6) + JSON_OBJECT_SIZE(1) + JSON_OBJECT_SIZE(4) + 140;
const int capacityBroker = JSON_ARRAY_SIZE(3) + JSON_OBJECT_SIZE(3) + 80;
const int capacityP = JSON_OBJECT_SIZE(2) + JSON_ARRAY_SIZE(1) + JSON_OBJECT_SIZE(4) + 40;
const int capacityS = JSON_OBJECT_SIZE(2) + JSON_ARRAY_SIZE(1) + JSON_OBJECT_SIZE(4) + 40;
const int capacityE = JSON_OBJECT_SIZE(2) + JSON_ARRAY_SIZE(1) + JSON_OBJECT_SIZE(4) + 40;


DynamicJsonDocument doc_sndR(capacityR); //Da inviare per la registrazione
DynamicJsonDocument doc_sndP(capacityP); //Da inviare con il publish
DynamicJsonDocument doc_sndS(capacityS); //Da ricevere e interpretare con il subscribe
DynamicJsonDocument doc_sndBroker(capacityBroker); 
DynamicJsonDocument doc_sndEP(capacityE); //Da ricevere dopo la post per ottenere gli endpoints

//PINS
const int tempPin = A1;
const int fPin = 11;
const int ledPin = 10;
const int pirPin = 7;
const int soundPin = 9;
const int ledPin2 = 12;
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
boolean PIRpresence = 0; //infrarossi
boolean soundPres = 0; //sensore di rumore
boolean Ppres = 0; //PIRpresence || soundPres

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


//Mqtt 

//TEMPLATE 
/*
{
"ip_address" : "255.255.255.255",
"port" : 8080,
"endpoints" : ["..."]
}
*/

MQTTclient mymqtt;
String host = "0.0.0.0";

String broker;
int port;
String endpoints[6];


String my_curlGET(){
    Process p;
    p.begin("curl");
    p.addParameter("-H");
    p.addParameter("Content-Type:application/json");
    p.addParameter("-X");
    p.addParameter("GET");
    p.addParameter(address);
    p.run();
    return(p.readString());

}

String my_curlPOST(){
    Process p;
    p.begin("curl");
    p.addParameter("-H");
    p.addParameter("Content-Type:application/json");
    p.addParameter("-X");
    p.addParameter("POST");
    //Json di richiesta 
    p.addParameter(host);
    p.addParameter("8080")
    p.run();
    return(p.readString());
}


void stampaMqtt(const String& topic, const String& subtopic, const String& message) {

  lcd.clear();
  lcd.print(message);

  delay(2000);
}

void interact(const String& topic, const String& subtopic, const String& message){
  //Deserializzo json in DJD
  //Controllo il campo utilizzato
  //Gestisco l'interazione con la smarthome qui
  return;

}


//Invio la registrazione al catalogo e ottengo il broker
void catalogRegister(){

    //Faccio la registrazione
    /*PARTE MANCANTE PER GESTIONE DI JSON ASSENTE: v. nella sezione 'Hardware' della relazione, 
    paragrafo 'GESTIONE DELLA (RI)CONNESSIONE'*/


    //Faccio una curl al catalog
    //ottengo il broker
    
    //Curl per la GET
    String dataBroker = my_curlGET();
    deserializeJson(doc_sndBroker,dataBroker);

    //Questa la ottengo mediante GET
    broker = doc_sndBroker[0]["ip_address"];
    port = doc_sndBroker[0]["port"];

    //Questa parte va ottenuta mediante POST
    String dataEP = my_curlPOST();
    //Deserializzazione degli endpoint da leggere come json

    deserializeJson(doc_sndEP,dataEP);
}



//DA QUA IN POI CODICE DELLA SMARTHOME
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
  int c = (int)tempMap(currentTemp); 
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

//Svuota il buffer di input
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
  pinMode(ledPin2,INPUT);

  //registroAlCatalogo
  //catalogRegister();
  //mymqtt.begin(broker, 1883);
  mymqtt.begin("0.0.0.0",1883);
  while (!Serial);

  lcd.begin(16, 2);
  lcd.setBacklight(255);
  lcd.home();
  lcd.clear();
  attachInterrupt(digitalPinToInterrupt(pirPin), PIRcheckPresence, CHANGE);
  printCurrentSetPoint();

  Serial.println("Inserire il carattere + se si vuole inserire dei setPoint diversi.");
  timer = millis();

  mymqtt.subscribe("/tiot/18/lcd",stampaMqtt);
  mymqtt.subscribe("/tiot/18/interact",interact)
}

void loop() {
  
  if (!changingVal) {
    t1 = millis();
    
    switchP();
    tempRegulator(tempCalc());
    soundOccurrence();
    //test();
    lcdShow();
  }


  if (Serial.available() > 0 && Serial.peek() == '+') {
    Serialfree();
    checkInput();
  }

  //invio in documento json serializzato contenente temerature,info su presenze e rumori
  //PARTE MANCANTE PER GESTIONE DI JSON ASSENTE
  //nessun temperatureData
  mymqtt.publish("tiot/18/temperature",temperatureData);
  delay(5000);
}


//temperatureData
//Registration
//Device
//Endpoints
//doc_sndBroker
//doc_sndEP
//doc_sndP