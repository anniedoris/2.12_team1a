#include <ESP32Servo.h>

Servo myServo;

const int servoPin = 9; // GPIO pin to which the servo is connected

void setup() 
{
  myServo.attach(servoPin);
}

void loop() 
{
  myServo.write(0);    // Move the servo to 0 degrees
  delay(1000);         // Wait for 1 second
  myServo.write(90);   // Move the servo to 90 degrees
  delay(1000);         // Wait for 1 second
  myServo.write(180);  // Move the servo to 180 degrees
  delay(1000);         // Wait for 1 second
}