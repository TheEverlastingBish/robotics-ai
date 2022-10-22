int LED_Pin = 13;  // For Arduino Nano, the in-built LED Pin is set to 13.

void setup()
{
  pinMode(LED_Pin, OUTPUT);
}

void loop()
{
  // Turn it on
  digitalWrite(LED_Pin, HIGH);
  delay(300); // On wait time in millisecond(s)

  // Turn it off
  digitalWrite(LED_Pin, LOW);
  delay(700); // Off wait time in millisecond(s)
}
