#include <Arduino.h>
#include <ESP32Servo.h>

// Adapted from https://github.com/madhephaestus/ESP32Servo/blob/master/examples/Multiple-Servo-Example-Arduino/Multiple-Servo-Example-Arduino.ino

// Create two servo objects
Servo servo1;
Servo servo2;

// Define min and max positions for the servos
const int SERVO1_MIN = 75; // Minimum position for servo1
const int SERVO1_MAX = 115; // Maximum position for servo1
const int SERVO2_MIN = 75; // Minimum position for servo2
const int SERVO2_MAX = 115; // Maximum position for servo2

int pos = 90; // Initial position for both servos (middle)

void setup() {
  // Attach servos to digital pins on the Arduino
  servo1.attach(9); // Servo 1 on pin 9
  servo2.attach(6); // Servo 2 on pin 6

  // Initialize serial communication at 115200 bits per second:
  Serial.begin(115200);
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    char input = Serial.read(); // Read the incoming byte

    if (input == 'o') { // If 'i' is pressed, move inward
      pos = max(pos - 1, SERVO1_MIN); // Decrease position but not less than SERVO1_MIN
    } else if (input == 'i') { // If 'o' is pressed, move outward
      pos = min(pos + 1, SERVO1_MAX); // Increase position but not more than SERVO1_MAX
    }

    // Move servos to new position within defined limits
    servo1.write(pos);
    servo2.write(map(pos-90, SERVO1_MIN, SERVO1_MAX, SERVO2_MAX, SERVO2_MIN)); // Map and inverse position for the second servo
  }
}
