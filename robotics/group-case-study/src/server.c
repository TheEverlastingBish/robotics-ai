/* Author: Dionysus Mariyanayagam, Bish Sinha,
 * Ghanshyam Gondaliya, Faizal Umar, Christina,
 * Madu
 *
 * This is the Server Side Start this ESP32 first
 * Make sure there is dedicated power
 */

#include <Arduino>
#include <string>
#include <bits/stdc++.h> 
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
using namespace std; 


const char *ssid = "CyberneticHandServerGroup1";
const char *password = "Sw33tSurr3nd3r";

AsyncWebServer server(80); // Create an asynchronous web server on port

// Button Pins
const int ButtonPins[6] = { 34, 35, 32, 33, 25, 26 };

// Button States
int ButtonStates[6] = { };

// const String htmlHeader = "<DOCTYPE html>\\n<html>\\n<head>\\n<title>Cybernetic Arm</title>\\n</head>\\n<body>\\n<h1>\\n";
// const String htmlFooter = "</h1>\n</body>\n</html>";

String countTest()
{
    String count = String((millis() / 1000));
    Serial.println(count);
    return count;
}


String cipherEncrypt(String response_text)
{
    char xorKey = 'D';
    int len = strlen(response_text);

    for (int i; i < len; i++)
    {
        response_text[i] = response_text[i] ^ xorKey;
    }

    return response_text;
}


String buttonParse(String buttonName, int buttonState)
{
  String response;

    if (buttonState == HIGH)
    {
        response = String("ON") + buttonName;
    }
    else
    {
        response = String("OFF") + buttonName;
    }

    response = cipherEncrypt(response);

    Serial.println(response);
    return String(response);
}


void setup()
{
    Serial.begin(115200);        // Clock speed for ESP32 Processor
    WiFi.softAP(ssid, password); // Setting up the WiFi

    IPAddress IP = WiFi.softAPIP(); // Get the IP address of this device
    Serial.print("AP IP address: ");
    Serial.println(IP);

    server.begin(); // Starts the server

    int numButtons = sizeof(ButtonPins) / sizeof(int);

    // initialize the pushbutton pin as an input:
    for (int i = 0; i < numButtons; i++)
    {
      pinMode(ButtonPins[i], INPUT);
    }

    // All the different webpages
    server.on("/count", HTTP_GET, [](AsyncWebServerRequest *request)
          { request->send_P(200, "text/plain", countTest().c_str()); });

    for (int i=0; i < 6; i++)
    {
      String buttonContext = String("BT") + String(i);
      String buttonEndpoint = String("/button") + String(i + 1);
      // String htmlContent = htmlHeader + buttonParse(buttonContext, digitalRead(ButtonPins[i])) + htmlFooter;
      // htmlHeader + buttonContext + htmlFooter;

      server.on(buttonContext.c_str(), HTTP_GET, [htmlContent](AsyncWebServerRequest *request)
      { 
        request->send_P(200, "text/plain", buttonParse(buttonContext, digitalRead(ButtonPins[i])).c_str());
      });
    }
}


void loop()
{
    // countTest();

    for (int i = 0; i < 6; i++)
    {
      String buttonContext = String("BT") + String(i + 1);
      String buttonEndpoint = String("/button") + String(i + 1);

      buttonParse(buttonContext, digitalRead(ButtonPins[i]));
    }

    delay(500);
}
