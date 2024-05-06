#include <Adafruit_MLX90640.h>
#include <Adafruit_GFX.h>
#include <Adafruit_HX8357.h>
#include <Wire.h>
#include <iostream>
#include <vector>

/*
  This is code for running the IR sensor on the end effector. It will print out to the serial monitor
  the number of pixels in the IR window that are above a certain threshold. We first set up the IR sensor
  with a Adafruit display and we tested putting the IR camera above the IR sensors in TIM's house. We had
  a mapping from sensor reading values to colors for display. We noticed that when the sensor was above TIM's
  heating pads, there were yellow colors and hotter colors (orange, red, etc.) on the display. The yellow color 
  corresponded with pixel readings of greater than 29, so we set the threshold to 29. We then tally all the
  pixels in the field of view that are above this threshold, and report that number through the display port.
  More than 50 pixels with a threshold of greater than 29 meant that TIM was located.
*/

// Set up the pins
#define TFT_CS 4
#define TFT_DC 5
#define TFT_RST -1  // RST can be set to -1 if you tie it to Arduino's reset
Adafruit_HX8357 tft = Adafruit_HX8357(TFT_CS, TFT_DC, TFT_RST);

Adafruit_MLX90640 mlx;
float frame[32*24]; // buffer for full frame of temperatures

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10); // wait for serial port to connect
  Serial.println("Adafruit MLX90640 Simple Test");

  if (! mlx.begin(MLX90640_I2CADDR_DEFAULT, &Wire)) {
    Serial.println("MLX90640 not found!");
    while (1) delay(10); // halt forever
  }

  mlx.setMode(MLX90640_CHESS);
  mlx.setResolution(MLX90640_ADC_18BIT);
  mlx.setRefreshRate(MLX90640_2_HZ);
}

void loop() {

  // Try to get the frame
  if (mlx.getFrame(frame) != 0) {
    Serial.println("Failed to read frame");
    return;
  }

  // List to store the number of pixels that have a IR reading greater than the
  // `yellow' threshold of 29.
  std::vector<int> num_values;

  for (uint8_t h = 0; h < 24; h++) {
    for (uint8_t w = 0; w < 32; w++) {
      float temperature = frame[h * 32 + w];

      if (temperature > 29) // filters for yellow or above
      {
        num_values.push_back(1); // add 1 to the vector
      }

      else
      {
        num_values.push_back(0); // Add 0 to the vector
      }
    }
  }

  // Return the number of pixels that meet the threshold
  int count = std::count_if(num_values.begin(), num_values.end(), [](int x) { return x != 0; });

  // If the number of pixels that meet the threshold is less than 50, TIM has not been located
  if (count <= 50)
  {
    Serial.println("No signal");
    Serial.println(count);
  }

  // If the number of pixels that meet the threshold is greater than 50, TIM has been located
  else
  {
    Serial.println("TIM LOCATED!"); // print this info to the user
    Serial.println(count);
  }

  delay(500); // Refresh rate of the display
}
