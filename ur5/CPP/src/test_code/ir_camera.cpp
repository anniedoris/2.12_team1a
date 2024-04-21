// Code to control the IR camera on the end effector 
// Adafruit MLX90640

// This code is an example file from  https://learn.adafruit.com/adafruit-mlx90640-ir-thermal-camera/arduino-thermal-camera

#include <Adafruit_MLX90640.h>
#include "Adafruit_Arcada.h"
Adafruit_MLX90640 mlx;
Adafruit_Arcada arcada;

#if !defined(USE_TINYUSB)
  #warning "Compile with TinyUSB selected!"
#endif

File myFile;

float mlx90640To[768];   // Here we receive the float vals acquired from MLX90640

#define DE_BOUNCE 200
  // Wait this many msec between button clicks
#define MENU_LEN 12
  // Number of total available menu choices
#define MENU_ROWS 9
  // Number of menu lines that can fit on screen
#define MENU_VPOS 6
#define GRAY_33 0x528A
#define BOTTOM_DIR "MLX90640"
#define DIR_FORMAT "/dir%05d"
#define BMP_FORMAT "/frm%05d.bmp"
#define CFG_FLNAME "/config.ini"
#define MAX_SERIAL 999

// BMP File Header, little end first, Photoshop ver.
const PROGMEM uint8_t BmpPSPHead[14] = {
 0x42, 0x4D,             // "BM" in hex
 0x38, 0x09, 0x00, 0x00, // File size, 2360
 0x00, 0x00,             // reserved for app data 1
 0x00, 0x00,             // reserved for app data 2
 0x36, 0x00, 0x00, 0x00  // Offset of first pixel, 54
};

// BMP 24-bit DIB Header, little end first, Photoshop ver.
const PROGMEM uint8_t DIBHeadPSP1[40] = {
 0x28, 0x00, 0x00, 0x00,  // Header size, 40
 0x20, 0x00, 0x00, 0x00,  // pixel width, 32
 0x18, 0x00, 0x00, 0x00,  // pixel height, 24
 0x01, 0x00,              // color planes, 1
 0x18, 0x00,              // bits per pixel, 24
 0x00, 0x00, 0x00, 0x00,  // Compression method, 0==none
 0x00, 0x00, 0x00, 0x00,  // Raw bitmap data size, dummy 0
 0x12, 0x0B, 0x00, 0x00,  // Pixels per meter H, 2834
 0x12, 0x0B, 0x00, 0x00,  // Pixels per meter V, 2834
 0x00, 0x00, 0x00, 0x00,  // Colors in palette, 0==default 2^n
 0x00, 0x00, 0x00, 0x00   // Number of important colors, 0
};

// BMP file data, 2 byte padding
const PROGMEM uint8_t PSPpad[2] = {0x00, 0x00};

//Byte arrays of bitmapped icons, 16 x 12 px:
const PROGMEM uint8_t battIcon[] = {
0x0f, 0x00, 0x3f, 0xc0, 0x20, 0x40, 0x20, 0x40, 0x20, 0x40, 0x20, 0x40, 
0x20, 0x40, 0x20, 0x40, 0x20, 0x40, 0x20, 0x40, 0x20, 0x40, 0x3f, 0xc0};

const PROGMEM uint8_t camIcon[] = {
0x01, 0xe0, 0x61, 0x20, 0xff, 0xf0, 0x80, 0x10, 0x86, 0x10, 0x89, 0x10, 
0x90, 0x90, 0x90, 0x90, 0x89, 0x10, 0x86, 0x10, 0x80, 0x10, 0xff, 0xf0};

const PROGMEM uint8_t SDicon[] = {
0x0f, 0xe0, 0x1f, 0xe0, 0x3c, 0x60, 0x78, 0x60, 0x70, 0x60, 0x60, 0x60, 
0x60, 0x60, 0x60, 0x60, 0x6f, 0x60, 0x60, 0x60, 0x7f, 0xe0, 0x7f, 0xe0};

const PROGMEM uint8_t snowIcon[] = {
0x15, 0x00, 0x4E, 0x40, 0xC4, 0x60, 0x75, 0xC0, 0x9F, 0x20, 0x0E, 0x00,
0x0E, 0x00, 0x9F, 0x20, 0x75, 0xC0, 0xC4, 0x60, 0x4E, 0x40, 0x15, 0x00};

uint8_t pixelArray[2304];   // BMP image body, 32 pixels * 24 rows * 3 bytes

// Some global values that several functions will use, including
// 5 floats to append to the BMP pixel data:
// coldest pixel, coldest color, center temp, hottest color, hottest pixel
float sneakFloats[5] = {3.1415926, 0.0, -11.7, 98.6, -12.34};      // Test values that get overwritten
uint16_t highAddr = 0, lowAddr = 0;                                // Append the pixel addresses, too

uint16_t backColor, lowPixel, highPixel, buttonRfunc = 1,
         emissivity = 95, frameRate = 4,
         thermRange = 0, paletteNum = 1, colorPal[256],            // Array for color palettes
         nextDirIndex = 0, nextBMPindex = 0, nextBMPsequence = 1;  // These keep count of SD files and dirs, 0==error
uint32_t deBounce = 0, buttonBits = 0;
boolean mirrorFlag = false, celsiusFlag = false, markersOn = true,
        screenDim = false, smoothing = false, showLastCap = false,
        save1frame = false, recordingInProg = false, buttonActive = false;
float battAverage = 0.0, colorLow = 0.0, colorHigh = 100.0;        // Values for managing color range
volatile boolean clickFlagMenu = false, clickFlagSelect = false;   // Volatiles for timer callback handling