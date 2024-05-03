#include <Arduino.h>
#include <ESP32Servo.h>

// Adapted from https://github.com/madhephaestus/ESP32Servo/blob/master/examples/Multiple-Servo-Example-Arduino/Multiple-Servo-Example-Arduino.ino
// Updated on 5/1/24 - works 

// Create two servo objects
Servo servo1;
Servo servo2;

int pos; // Initial position for servos
int pos2;
int position2;
int GRASP_DELTA = 70;
int OUT_POS_RIGHT = 0;
int IN_POS_RIGHT = OUT_POS_RIGHT + GRASP_DELTA;
bool move_in = true;
int IN_POS_LEFT = 0;
int OUT_POS_LEFT = IN_POS_LEFT + GRASP_DELTA;

int micro_sec;
int read_val;

void setup() {
  // Attach servos to digital pins on the Arduino
  ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	servo1.setPeriodHertz(50);    // standard 50 hz servo
	servo1.attach(9, 500, 2500); // attaches the servo on pin 18 to the servo object
  servo2.setPeriodHertz(50);
  servo2.attach(6, 500, 2500);
  // servo1.attach(9); // Servo 1 on pin 9
  // servo2.attach(6); // Servo 2 on pin 6

  // Initialize serial communication at 115200 bits per second:
  Serial.begin(115200);
  servo1.write(OUT_POS_RIGHT);
  servo2.write(OUT_POS_LEFT);
  
}

void loop() {

  // GOOD CODE
  if (Serial.available() > 0) 
  {
    char input = Serial.read(); // Read the incoming byte

    if (input == 'o') 
    { // If 'i' is pressed, move inward
      // pos = OUT_POS_RIGHT; // Decrease position but not less than SERVO1_MIN
      //Serial.println(pos);
      servo1.write(OUT_POS_RIGHT);
      servo2.write(OUT_POS_LEFT);
    } 
    
    else if (input == 'i') 
    { // If 'o' is pressed, move outward
      // pos = IN_POS_RIGHT; // Increase position but not more than SERVO1_MAX
      //Serial.println(pos);
      servo1.write(IN_POS_RIGHT);
      servo2.write(IN_POS_LEFT);
      
    }
  }

  