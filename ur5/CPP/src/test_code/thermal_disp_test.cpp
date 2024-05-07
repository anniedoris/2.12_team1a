#include <Adafruit_MLX90640.h>
#include <Adafruit_GFX.h>
#include <Adafruit_HX8357.h>
#include <Wire.h>
#include <iostream>
#include <vector>

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

  // tft.begin();
  // tft.setRotation(1);
}

// uint16_t temperatureToColor(float temperature) {
//   // Map temperatures to a color gradient (blue to red)
//   if (temperature < 20) return tft.color565(0, 0, 255); // Blue
//   else if (temperature < 23) return tft.color565(0, 128, 255); // Light blue
//   else if (temperature < 25) return tft.color565(0, 255, 255); // Cyan
//   else if (temperature < 27) return tft.color565(0, 255, 128); // Greenish
//   else if (temperature < 29) return tft.color565(128, 255, 0); // Light green
//   else if (temperature < 31) return tft.color565(255, 255, 0); // Yellow
//   else if (temperature < 33) return tft.color565(255, 128, 0); // Orange
//   else if (temperature < 35) return tft.color565(255, 0, 0); // Red
//   else return tft.color565(128, 0, 0); // Dark red
// }

void loop() {
  if (mlx.getFrame(frame) != 0) {
    Serial.println("Failed to read frame");
    return;
  }

  // tft.fillScreen(HX8357_BLACK);
  // uint8_t cellWidth = tft.width() / 32;
  // uint8_t cellHeight = tft.height() / 24;
  
  // Create an array of items that have at least orange value
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


      // uint16_t color = temperatureToColor(temperature);
      // tft.fillRect(w * cellWidth, h * cellHeight, cellWidth, cellHeight, color);
    }
  }

  int count = std::count_if(num_values.begin(), num_values.end(), [](int x) { return x != 0; });

  if (count <= 50)
  {
    Serial.println("No signal");
    Serial.println(count);
  }

  else
  {
    Serial.println("TIM LOCATED!");
    Serial.println(count);
  }


  delay(500); // Refresh rate of the display
}
