//Modified by Joo Won to allow change in Robot speed from 10 - 20 with a button press
#include <Bounce2.h>
#include "wireless.h"
#include "util.h"
#include "joystick.h"
#include "dpad.h"
#include "display.h"
#include "controller_pinout.h"
#include <Arduino.h>

// Add a variable to track the button state
bool buttonState = false;

// Constants for button pin
#define BUTTON_PIN BUTTON_L_PIN

ControllerMessage prevControllerMessage;

Joystick joystick1(JOYSTICK1_X_PIN, JOYSTICK1_Y_PIN);
//Joystick joystick2(JOYSTICK2_X_PIN, JOYSTICK2_Y_PIN);

void setup() {
    Serial.begin(115200);

    setupWireless();

    joystick1.setup();

    Serial.println("Setup complete.");
    
    pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
        // Read the button state
    bool newButtonState = digitalRead(BUTTON_PIN);

    // Check if the button state has changed
    if (newButtonState != buttonState) {
        // Send a command to the robot when the button is pressed
        if (newButtonState == LOW) {
            // Button is pressed, send command to increase speed
            sendSpeedCommand(20); // Change speed to 20
        } else {
            // Button is released, send command to revert to default speed
            sendSpeedCommand(10); // Change speed to 10
        }
        // Update the button state
        buttonState = newButtonState;
    }
    
    // Read and send controller sensors
    EVERY_N_MILLIS(50) 
    {
        controllerMessage.millis = millis();
        controllerMessage.joystick1 = joystick1.read();
                
        if (!(prevControllerMessage == controllerMessage)) 
        {
            sendControllerData();         
            prevControllerMessage = controllerMessage;
        }
    }
}