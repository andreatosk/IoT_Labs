//Arduino Sample Code for Fan Module
//www.DFRobot.com
//Version 1.0

#define Fan 5    //define driver pins

char c;
int value = 0;

void setup()
{
  pinMode(Fan,OUTPUT);
  Serial.begin(9600);    //Baudrate: 9600
}
void loop()
{
        analogWrite(Fan, value);   //PWM
        if(Serial.available() > 0)
          c = Serial.peek();
        Serial.read();
        
        if(c=='+'){
          if(value<244){
            value+=10;
            Serial.print("Aumentando la velocità a: ");
            Serial.println(value);

          }
          else
            Serial.println("Velocità massima raggiunta");
        }
        if(c=='-'){
          if(value>9){
            value-=10;
            Serial.print("Diminuendo la velocità a: ");
            Serial.println(value);
            
          }
          else
            Serial.println("Velocità minima raggiunta");
        }
}
