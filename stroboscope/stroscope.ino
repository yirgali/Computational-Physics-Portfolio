int dcPin=9;
int w=200;//we will measure this variable


int potPin=A5;
int potVal;

int ledPin=5;

unsigned long startTime;
unsigned long currentTime;
float period;
bool isOn;
bool per=false;

float v; //frequency

void setup() {
  pinMode(dcPin,OUTPUT);
  pinMode(ledPin,OUTPUT);
  Serial.begin(9600);
  startTime=micros();
}

void loop() {
  analogWrite(dcPin,w);
  potVal=analogRead(potPin);
  frequency(potVal);
  cycle();
  Serial.println(v);
}


void cycle() {
  isOn=wait();
  if (isOn==true) {
    digitalWrite(ledPin,HIGH);
  }
  else if (isOn==false) {
    digitalWrite(ledPin,LOW);
  }
}


bool wait() {  
  currentTime=micros();
  if (currentTime-startTime >= period) {
    per=!per;
    startTime=currentTime;
  }
  return per;
}

void frequency(int potVal) {
  v=(150./1023)*potVal; //frequency of the led 
  period= 1000000./(2.*v); //we use 1000000 since we use micros()
}