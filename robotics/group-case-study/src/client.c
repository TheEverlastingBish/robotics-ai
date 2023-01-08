/* Author: Dionysus Mariyanayagam
 * This is the Client side start after the server
*/
/* Connection for PCA9685
  GND - GND
  OE - NC
  SCL - D22
  SDA - D21
  VCC - 3.3V
  V+ - NC
*/

#include <WiFi.h>
#include <HTTPClient.h>

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();


const char *ssid = "CyberneticHandServerGroup1";
const char *password = "Sw33tSurr3nd3r";


/*
  MIN pulse length count (out of 4096)
  MAX pulse length count (out of 4096)
  defined per servo
*/

#define SERVOMIN  150 //this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  400 //this is the 'maximum' pulse length count (out of 4096)

#define Index_Thumb_Min 100    //synced
#define Index_Thumb_Max 450    //synced

#define Middle_Min 150         //synced
#define Middle_Max 580         //synced

#define Ring_Min 200           //synced
#define Ring_Max 600           //synced

#define Pinky_Min 200          //synced
#define Pinky_Max 600          //synced

#define Thumb_Rotate_Min 100   //synced
#define Thumb_Rotate_Max 500   //synced

#define Forearm_Rotate_Min 300 //synced
#define Forearm_Rotate_Max 550 //synced

/*  All servos being used  */

uint8_t servonum = 5; // Max number of servos for cycling, starting count from 0

static int Servo_Index_Thumb = 0;     //Index and Thumb
static int Servo_Middle = 1;          //Middle finger
static int Servo_Ring = 2;            //Ring finger
static int Servo_Pinky = 3;           //Pinky finger
static int Servo_Thumb_Rotate = 4;    //Thumb rotate
static int Servo_Forearm_Rotate = 5;  //Forearm rotate

const char* serverCounts  = "http://192.168.4.1/count";
const char* serverButton1 = "http://192.168.4.1/button1";
const char* serverButton2 = "http://192.168.4.1/button2";
const char* serverButton3 = "http://192.168.4.1/button3";
const char* serverButton4 = "http://192.168.4.1/button4";
const char* serverButton5 = "http://192.168.4.1/button5";
const char* serverButton6 = "http://192.168.4.1/button6";


// To store the http responses
String count;       // From the /count Server side
String button1;     // From the /button1 Server side
String button2;
String button3;
String button4;
String button5;
String button6;

//Connection LEDs
const int connectedLED = 15;
const int disconnectedLED = 2;

unsigned long previousMillis = 0;
const long interval = 5000;



void setup()
{
  Serial.begin(115200);
  
  pwm.begin();
  pwm.setPWMFreq(60);   // Analog servos run at ~60 Hz updates
  
  WiFi.begin(ssid, password);
  Serial.println("Connecting ...");
  
  pinMode(connectedLED, OUTPUT);
  pinMode(disconnectedLED, OUTPUT);
  
    while (WiFi.status() != WL_CONNECTED) 
    {
        delay(500);
        Serial.print(".");
    }
  
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}



void SerialRead()
{
    button1 = httpGETRequest(serverButton1);
    Serial.println(buttonOne);

    button2 = httpGETRequest(serverButton2);
    Serial.println(buttonTwo);

    button3 = httpGETRequest(serverButton3);
    Serial.println(buttonThree);

    button4 = httpGETRequest(serverButton4);
    Serial.println(buttonFour);

    button5 = httpGETRequest(serverButton5);
    Serial.println(buttonFive);

    button6 = httpGETRequest(serverButton6);
    Serial.println(buttonSix);
}



void countTest()
{
    count = httpGETRequest(serverCounts);
    Serial.println(count);
}



void Flex_Index_Thumb()
{
  if(button1 == "ON1")
  {
    pwm.setPWM(Servo_Index_Thumb, 0, Index_Thumb_Max);
    Serial.println("INTB_1");
    } else {
    pwm.setPWM(Servo_Index_Thumb, 0, Index_Thumb_Min);
    Serial.println("INTB_0");
  }
}


void Flex_Middle()
{
  if(button2 == "ON2")
  {
    pwm.setPWM(Servo_Middle, 0, Middle_Max);
    Serial.println("MI_1");
    } else {
    pwm.setPWM(Servo_Middle, 0, Middle_Min);
    Serial.println("MI_0");
  }
}


void Flex_Ring()
{
  if(button3 == "ON3")
  {
    pwm.setPWM(Servo_Ring, 0, Ring_Max);
    Serial.println("RI_1");
    } else {
    pwm.setPWM(Servo_Ring, 0, Ring_Min);
    Serial.println("RI_0");
  }
}


void Flex_Pinky()
{
  if(button4 == "ON4")
  {
    pwm.setPWM(Servo_Pinky, 0, Pinky_Max);
    Serial.println("PI_1");
    } else {
    pwm.setPWM(Servo_Pinky, 0, Pinky_Min);
    Serial.println("PI_0");
  }
}


void Flex_Thumb_Rotate()
{
  if(button5 == "ON5")
  {
    pwm.setPWM(Servo_Thumb_Rotate, 0, Thumb_Rotate_Max);
    Serial.println("THRO_1");
    } else {
    pwm.setPWM(Servo_Thumb_Rotate, 0, Thumb_Rotate_Min);
    Serial.println("THRO_0");
  }
}


void Flex_Forearm_Rotate()
{
  if(button6 == "ON6")
  {
    pwm.setPWM(Servo_Forearm_Rotate, 0, Forearm_Rotate_Max);
    Serial.println("FORO_1");
    } else {
    pwm.setPWM(Servo_Forearm_Rotate, 0, Forearm_Rotate_Min);
    Serial.println("FORO_0");
  }
}



void loop() 
{
    unsigned long currentMillis = millis();

    if (currentMillis - previousMillis >= interval) 
    {
        // Check WiFi connection status
        if (WiFi.status() == WL_CONNECTED ) 
        {
            SerialRead();
            //countTest();
            Flex_Index_Thumb();
            Flex_Middle();
            Flex_Ring();
            Flex_Pinky();
            Flex_Thumb_Rotate();
            Flex_Forearm_Rotate();

            digitalWrite(connectedLED, HIGH);
            digitalWrite(disconnectedLED, LOW);

        } else 
        {
            Serial.println("WiFi Disconnected");
            digitalWrite(connectedLED, LOW);
            digitalWrite(disconnectedLED, HIGH);
        }
    }
}



String httpGETRequest(const char* serverName) 
{
  HTTPClient http;
  
  // Your IP address with path or Domain name with URL path
  http.begin(serverName);
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload;
  
  if (httpResponseCode > 0)
  {
    payload = http.getString();
    //Serial.println(httpResponseCode);
    Serial.println(payload);
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();
  return payload;
}
