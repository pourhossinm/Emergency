#include <SoftwareSerial.h>

SoftwareSerial sim800(3, 2); // RX, TX
String inputString = "";

void setup() {
  Serial.begin(9600);      // ارتباط با پایتون
  sim800.begin(9600);      // ارتباط با SIM800
  delay(2000);

  // تنظیم عدم پاسخ خودکار تماس (چون می‌خواهیم دستی انجام دهیم)
  sim800.println("ATS0=0");
  delay(1000);

  Serial.println("Ready");
}

void loop() {
  // خواندن فرمان از پایتون
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      inputString.trim();
      processCommand(inputString);
      inputString = "";
    } else {
      inputString += c;
    }
  }

  // بررسی تماس ورودی (نمایشی یا تستی)
  if (sim800.available()) {
    String response = sim800.readString();
    if (response.indexOf("RING") != -1) {
      Serial.println("Incoming Call...");
    }
  }
}

void processCommand(String cmd) {
  if (cmd == "ATA") {
    sim800.println("ATA"); // پاسخ تماس
    Serial.println("Answered");
  }
  else if (cmd == "ATH") {
    sim800.println("ATH"); // قطع تماس
    Serial.println("Hung up");
  }
  else if (cmd.startsWith("SMS:")) {
    int firstColon = cmd.indexOf(':', 4);
    if (firstColon != -1) {
      String number = cmd.substring(4, firstColon);
      String message = cmd.substring(firstColon + 1);
      sendSMS(number, message);
    }
  }
}

void sendSMS(String number, String message) {
  sim800.println("AT+CMGF=1");
  delay(500);
  sim800.print("AT+CMGS=\"");
  sim800.print(number);
  sim800.println("\"");
  delay(500);
  sim800.print(message);
  delay(500);
  sim800.write(26); // Ctrl+Z
  delay(2000);
  Serial.println("SMS Sent.");
}
