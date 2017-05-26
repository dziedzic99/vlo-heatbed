int ThermistorPin = 7;
int Vo;
float R1 = 100000;
float logR2, R2, T;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;
String inputString = "";
boolean stringComplete = false;
float desired = -273.15;
int outputPin = 2;
int delayConst = 100; //in miliseconds

void setup()
{
 Serial.begin(9600); 
 pinMode(outputPin, OUTPUT);
}

void loop()
{
  
  Vo = analogRead(ThermistorPin);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15; 
  Serial.print(T);
  Serial.print(",");
  Serial.println(desired);
  if (stringComplete) 
  {
    desired = inputString.toFloat();
    if (desired > 80)
    {
      desired = 80;
    }
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
  if (T<desired)
  {
    digitalWrite(outputPin, HIGH);
  }
  else
  {
   digitalWrite(outputPin, LOW); 
  }
  delay(delayConst);
}


void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}



