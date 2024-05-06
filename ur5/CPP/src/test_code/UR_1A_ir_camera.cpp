#include <Adafruit_MLX90640.h>
#include <Adafruit_GFX.h>
#include <Adafruit_HX8357.h>
#include <Wire.h>

/*
  This file can be used to run the MLX90640 sensor with an Adafruit HX8357D display.
  We did not use this file in the actual competition, but we did use it to tune the
  ```ir_threshold.cpp``` file which we did use.
*/

#define TFT_CS 4
#define TFT_DC 5
#define TFT_RST -1  // RST can be set to -1 if you tie it to Arduino's reset
Adafruit_HX8357 tft = Adafruit_HX8357(TFT_CS, TFT_DC, TFT_RST);

Adafruit_MLX90640 mlx;
float frame[32*24]; // buffer for full frame of temperatures

void setup()
{
  Serial.begin(115200);
  while (!Serial) delay(10); // wait for serial port to connect
  Serial.println("Adafruit MLX90640 Simple Test");

  if (! mlx.begin(MLX90640_I2CADDR_DEFAULT, &Wire))
  {
    Serial.println("MLX90640 not found!");
    while (1) delay(10); // halt forever
  }

  mlx.setMode(MLX90640_CHESS);
  mlx.setResolution(MLX90640_ADC_18BIT);
  mlx.setRefreshRate(MLX90640_2_HZ);

  tft.begin();
  tft.setRotation(1);
}

uint16_t temperatureToColor(float temperature)
{
  // Map temperature readings to a color gradient (blue to red). These are the color mappings
  // discussed in ```ir_threshold.cpp```
  if (temperature < 20) return tft.color565(0, 0, 255); // Blue
  else if (temperature < 23) return tft.color565(0, 128, 255); // Light blue
  else if (temperature < 25) return tft.color565(0, 255, 255); // Cyan
  else if (temperature < 27) return tft.color565(0, 255, 128); // Greenish
  else if (temperature < 29) return tft.color565(128, 255, 0); // Light green
  else if (temperature < 31) return tft.color565(255, 255, 0); // Yellow
  else if (temperature < 33) return tft.color565(255, 128, 0); // Orange
  else if (temperature < 35) return tft.color565(255, 0, 0); // Red
  else return tft.color565(128, 0, 0); // Dark red
}

void loop()
{
  if (mlx.getFrame(frame) != 0)
  {
    Serial.println("Failed to read frame");
    return;
  }

  tft.fillScreen(HX8357_BLACK);
  uint8_t cellWidth = tft.width() / 32;
  uint8_t cellHeight = tft.height() / 24;
  
  // Map the IR readings to colors to show on the display
  for (uint8_t h = 0; h < 24; h++)
  {
    for (uint8_t w = 0; w < 32; w++)
    {
      float temperature = frame[h * 32 + w];
      uint16_t color = temperatureToColor(temperature);
      tft.fillRect(w * cellWidth, h * cellHeight, cellWidth, cellHeight, color);
    }
  }
  delay(500); // Refresh rate of the display
}