#include <Arduino.h>
#include <ESP32Servo.h> // Required for the servos
#include "MotorDriver.h" // Required for the Cytron motor driver that is connected to the electromagnet 

// Updated on 5/4/24
// This file includes code that runs the servos, electromagnet, and IR camera on the gripper.  

// Create two servo objects
Servo servo1;
Servo servo2;

// Pins connected to the Cytron Motor Driver
const int DIRPin = 39; // connected to DIR1 pin on Cytron
const int PWMPin = 41; // connected to PWM1 pin on Cytron
MotorDriver motor(DIRPin, PWMPin, 5); // channel 5

int pos; // Initial position for servos
int GRASP_DELTA = 70;
int OUT_POS_RIGHT = 0;
int IN_POS_RIGHT = OUT_POS_RIGHT + GRASP_DELTA;
int IN_POS_LEFT = 0;
int OUT_POS_LEFT = IN_POS_LEFT + GRASP_DELTA;
int MID_POS_RIGHT = (OUT_POS_RIGHT + GRASP_DELTA) / 2;
int MID_POS_LEFT = (IN_POS_LEFT + GRASP_DELTA) / 2;

void setup() {
  // Attach servos to digital pins on the Arduino and assign channels
  ESP32PWM::allocateTimer(0); // channel 0
	ESP32PWM::allocateTimer(1); // channel 1
	ESP32PWM::allocateTimer(2); // channel 2
	ESP32PWM::allocateTimer(3); // channel 3
	servo1.setPeriodHertz(50); // standard 50 hz servo
	servo1.attach(9, 500, 2500); // Servo 1 on pin 9
  servo2.setPeriodHertz(50); // standard 50 hz servo
  servo2.attach(6, 500, 2500); // Servo 2 on pin 6

  motor.setup(); // Set up the electromagnet
  
  Serial.begin(115200); // Initialize serial communication at 115200 bits per second
  servo1.write(OUT_POS_RIGHT); // Move servo1 to its initial position
  servo2.write(OUT_POS_LEFT); // Move servo2 to its initial position
}

void loop() {
  if (Serial.available() > 0) 
  {
    char input = Serial.read(); // Read the incoming byte

    if (input == 'o') 
    { // If 'o' is pressed, move outward
      Serial.println("Servo Position: Out");
      servo1.write(OUT_POS_RIGHT);
      servo2.write(OUT_POS_LEFT);
    } 
    
    else if (input == 'i') 
    { // If 'i' is pressed, move inward
      Serial.println("Servo Position: In");
      servo1.write(IN_POS_RIGHT);
      servo2.write(IN_POS_LEFT);
    }

     else if (input == 'm') 
    { // If 'm' is pressed, move to middle
      Serial.println("Servo Position: Middle");
      servo1.write(MID_POS_RIGHT);
      servo2.write(MID_POS_LEFT);
    }

    if (input == '1') {
      motor.drive(1.0);
      Serial.println("Electromagnet turned on");
    } else if (input == '0') {
      motor.drive(0.0);
      Serial.println("Electromagnet turned off");
    }
  }
}

  