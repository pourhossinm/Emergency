#include <SoftwareSerial.h>
SoftwareSerial sim800(3, 2); // RX, TX

void waitForResponse(unsigned long timeout = 2000);  // <-- اضافه شد

void setup() {
  Serial.begin(9600);
  sim800.begin(9600);

  Serial.println("SIM800L Voice Call Test");

  delay(1000);

  sim800.println("AT");
  waitForResponse();

  sim800.println("ATS0=1");
  waitForResponse();

  sim800.println("AT+CHFA=1");
  waitForResponse();

  sim800.println("AT+CLVL=100");
  waitForResponse();
}

void loop() {
  if (sim800.available()) {
    String response = sim800.readString();

    if (response.indexOf("RING") >= 0) {
      Serial.println("📞 تماس ورودی دریافت شد...");
    }

    Serial.print(response);
  }
}

// تابع بررسی پاسخ از ماژول
void waitForResponse(unsigned long timeout) {
  unsigned long start = millis();
  while (millis() - start < timeout) {
    while (sim800.available()) {
      Serial.write(sim800.read());
    }
  }
}
