// Code to control the electromagnet attached to the end effector 
#include <Arduino.h>

// Pins connected to the Cytron Motor Driver
const int DIRPin = 1; // connected to DIR1 pin on Cytron
const int PWMPin = 2; // connected to PWM1 pin on Cytron 

void setup() {
  Serial.begin(115200);
  
  pinMode(DIRPin, OUTPUT);
  pinMode(PWMPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == '1') {
      digitalWrite(DIRPin, HIGH); // Turn on electromagnet
      analogWrite(PWMPin, 255);
      Serial.println("Electromagnet turned on");
    } else if (command == '0') {
      digitalWrite(DIRPin, LOW); // Turn off electromagnet
      analogWrite(PWMPin, 0);
      Serial.println("Electromagnet turned off");
    }
  }
}
