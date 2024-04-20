#include <ESP32Servo.h>

// Adapted from https://github.com/madhephaestus/ESP32Servo/blob/master/examples/Multiple-Servo-Example-Arduino/Multiple-Servo-Example-Arduino.ino

Servo myServo1;
Servo myServo2;

const int servoPin1 = 9; // GPIO pin to which the servo is connected
const int servoPin2 = 10;

void setup() 
{
  myServo1.attach(servoPin1);
  myServo2.attach(servoPin2);
}

void loop() 
{
  myServo1.write(0);    // Move the servo to 0 degrees
  delay(1000);         // Wait for 1 second
  myServo1.write(90);   // Move the servo to 90 degrees
  delay(1000);         // Wait for 1 second
  myServo1.write(150);  // Move the servo to 180 degrees
  delay(1000);         // Wait for 1 second
}