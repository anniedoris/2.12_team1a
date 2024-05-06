#include <Arduino.h>
#include <esp_now.h>
#include <WiFi.h>
#include "wireless.h"

#include <Adafruit_MLX90640.h>
#include <Adafruit_GFX.h>
#include <Adafruit_HX8357.h>
#include <Wire.h>

#define TFT_CS 4
#define TFT_DC 5
#define TFT_RST -1  // RST can be set to -1 if you tie it to Arduino's reset
Adafruit_HX8357 tft = Adafruit_HX8357(TFT_CS, TFT_DC, TFT_RST);

Adafruit_MLX90640 mlx;

bool freshWirelessData = false;

void onDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
    memcpy(&tft, incomingData, sizeof(tft));
    freshWirelessData = true;
    
}

void setupWireless(){
    // Set device as a Wi-Fi Station
    WiFi.mode(WIFI_STA);

    // Init ESP-NOW
    if (esp_now_init() != ESP_OK) {
        Serial.println("Error initializing ESP-NOW");
        return;
    }

    //Tell the microcontroller which functions to call when
    //data is sent or received
    esp_now_register_recv_cb(onDataRecv);
    
    // ESP-NOW Setup Complete

}