// Code to control the electromagnet attached to the end effector 
#include <Arduino.h>
#include "MotorDriver.h"

// Pins connected to the Cytron Motor Driver
const int DIRPin = 39; // connected to DIR1 pin on Cytron
const int PWMPin = 41; // connected to PWM1 pin on Cytron
MotorDriver motor(DIRPin, PWMPin, 0); 

void setup() {
  Serial.begin(115200);
  
  motor.setup();
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == '1') {
      motor.drive(1.0);
      Serial.println("Electromagnet turned on");
    } else if (command == '0') {
      motor.drive(0.0);
      Serial.println("Electromagnet turned off");
    }
  }
}
