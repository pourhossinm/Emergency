#include <SoftwareSerial.h>

SoftwareSerial sim800(3, 2); // RX, TX
String inputString = "";

void setup() {
  Serial.begin(9600);     // ارتباط با پایتون
  sim800.begin(9600);     // ارتباط با SIM800
}

void loop() {
  // خواندن فرمان از پایتون
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      inputString.trim();  // حذف کاراکترهای اضافی
      processCommand(inputString);
      inputString = "";
    } else {
      inputString += c;
    }
  }
}

void processCommand(String command) {
  if (command == "ATA") {
    sim800.println("ATA");  // پاسخ به تماس
    Serial.println("CALL_ANSWERED");
  }
  else if (command == "ATH") {
    sim800.println("ATH");  // قطع تماس
    Serial.println("CALL_HUNG_UP");
  }
}
