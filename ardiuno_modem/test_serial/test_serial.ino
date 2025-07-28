#include <SoftwareSerial.h>

#define SIM800_TX 10
#define SIM800_RX 11

SoftwareSerial sim800(3, 2);

long baudRates[] = {4800, 9600, 19200, 38400, 57600, 115200};
int index = 0;
bool found = false;

void setup() {
  Serial.begin(4800);
  delay(1000);
  Serial.println("Testing SIM800 baud rates...");
}

void loop() {
  if (found || index >= sizeof(baudRates)/sizeof(baudRates[0])) return;

  long baud = baudRates[index];
  sim800.end();
  delay(200);
  sim800.begin(baud);

  Serial.print("Trying baud: ");
  Serial.println(baud);

  sim800.println("AT");
  delay(1000);

  while (sim800.available()) {
    char c = sim800.read();
    Serial.write(c);
    if (c == 'K') found = true; // OK
  }

  index++;
  delay(2000);
}
