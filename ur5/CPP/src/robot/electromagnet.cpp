// Code to control the electromagnet attached to the end effector 
#include <Arduino.h>

const int electromagnetPin = 13; // Choose the pin connected to the electromagnet

void setup() {
  Serial.begin(115200);
  
  pinMode(electromagnetPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == '1') {
      digitalWrite(electromagnetPin, HIGH); // Turn on electromagnet
      Serial.println("Electromagnet turned on");
    } else if (command == '0') {
      digitalWrite(electromagnetPin, LOW); // Turn off electromagnet
      Serial.println("Electromagnet turned off");
    }
  }
}
