/* Author: Dionysus Mariyanayagam, Bish Sinha,
 * Ghanshyam Gondaliya, Faizal Umar, Christina,
 * Madu
 *
 * This is the Server Side Start this ESP32 first
 * Make sure there is dedicated power
 */

#include <WiFi.h>
#include <ESPAsyncWebServer.h>

const char *ssid = "CyberneticHandServerGroup1";
const char *password = "Sw33tSurr3nd3r";

AsyncWebServer server(80); // Create an asynchronous web server on port

// Button Pins
const int buttonPin1 = 34;
const int buttonPin2 = 35;
const int buttonPin3 = 32;
const int buttonPin4 = 33;
const int buttonPin5 = 25;
const int buttonPin6 = 26;

// Button States
int buttonState1 = 0;
int buttonState2 = 0;
int buttonState3 = 0;
int buttonState4 = 0;
int buttonState5 = 0;
int buttonState6 = 0;

String countTest()
{
    String count = String((millis() / 1000));
    Serial.println(count);
    return count;
}

String buttonOne()
{
    buttonState1 = digitalRead(buttonPin1);
    if (buttonState1 == HIGH)

    {
        String confirm = "ON1";
        Serial.println(confirm);
        return String(confirm);
    }
    else
    {
        String decline = "OFF1";
        Serial.println(decline);
        return String(decline);
    }
}

String buttonTwo()
{
    buttonState2 = digitalRead(buttonPin2);
    if (buttonState2 == HIGH)
    {
        String confirm = "ON2";
        Serial.println(confirm);
        return String(confirm);
    }
    else
    {
        String decline = "OFF2";
        Serial.println(decline);
        return String(decline);
    }
}

String buttonThree()
{
    buttonState3 = digitalRead(buttonPin3);
    if (buttonState3 == HIGH)

    {
        String confirm = "ON3";
        Serial.println(confirm);
        return String(confirm);
    }
    else
    {
        String decline = "OFF3";
        Serial.println(decline);
        return String(decline);
    }
}

String buttonFour()
{
    buttonState4 = digitalRead(buttonPin4);
    if (buttonState4 == HIGH)

    {
        String confirm = "ON4";
        Serial.println(confirm);
        return String(confirm);
    }
    else
    {
        String decline = "OFF4";
        Serial.println(decline);
        return String(decline);
    }
}

String buttonFive()
{
    buttonState5 = digitalRead(buttonPin5);
    if (buttonState5 == HIGH)

    {
        String confirm = "ON5";
        Serial.println(confirm);
        return String(confirm);
    }
    else
    {
        String decline = "OFF5";
        Serial.println(decline);
        return String(decline);
    }
}

String buttonSix()
{
    buttonState6 = digitalRead(buttonPin6);
    if (buttonState6 == HIGH)

    {
        String confirm = "ON6";
        Serial.println(confirm);
        return String(confirm);
    }
    else
    {
        String decline = "OFF6";
        Serial.println(decline);
        return String(decline);
    }
}

void setup()
{
    Serial.begin(115200);        // Clock speed for ESP32 Processor
    WiFi.softAP(ssid, password); // Setting up the WiFi

    IPAddress IP = WiFi.softAPIP(); // Get the IP address of this device
    Serial.print("AP IP address: ");
    Serial.println(IP);

    server.begin(); // Starts the server

    // initialize the pushbutton pin as an input:
    pinMode(buttonPin1, INPUT);
    pinMode(buttonPin2, INPUT);
    pinMode(buttonPin3, INPUT);
    pinMode(buttonPin4, INPUT);
    pinMode(buttonPin5, INPUT);
    pinMode(buttonPin6, INPUT);

    // All the different webpages
    server.on("/count", HTTP_GET, [](AsyncWebServerRequest *request)
              { request->send_P(200, "text/plain", countTest().c_str()); });

    server.on("/buttonOne", HTTP_GET, [](AsyncWebServerRequest *request)
              { request->send_P(200, "text/plain", buttonOne().c_str()); });

    server.on("/buttonTwo", HTTP_GET, [](AsyncWebServerRequest *request)
              { request->send_P(200, "text/plain", buttonTwo().c_str()); });

    server.on("/buttonThree", HTTP_GET, [](AsyncWebServerRequest *request)
              { request->send_P(200, "text/plain", buttonThree().c_str()); });

    server.on("/buttonFour", HTTP_GET, [](AsyncWebServerRequest *request)
              { request->send_P(200, "text/plain", buttonFour().c_str()); });

    server.on("/buttonFive", HTTP_GET, [](AsyncWebServerRequest *request)
              { request->send_P(200, "text/plain", buttonFive().c_str()); });

    server.on("/buttonSix", HTTP_GET, [](AsyncWebServerRequest *request)
              { request->send_P(200, "text/plain", buttonSix().c_str()); });
}

void loop()
{
    countTest();
    // buttonOne();
    // buttonTwo();
    // buttonThree();
    // buttonFour();
    // buttonFive();
    // buttonSix();
    // delay(500);
}
