#include <SoftwareSerial.h>

SoftwareSerial sim800(3, 2); // RX, TX
String inputString = "";

void setup() {
  Serial.begin(4800);      // ارتباط با پایتون
  sim800.begin(4800);      // ارتباط با SIM800
  delay(2000);

  Serial.println("Ready");
  String command = Serial.readStringUntil('\n');
  Serial.println(command);
}

void loop() {

  // خواندن فرمان از پایتون
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "ATA") {
      sim800.println("ATA");
    }
  }

  if (sim800.available()) {
    String response = sim800.readStringUntil('\n');
    Serial.println(response);
  }
  

  // بازتاب پاسخ ماژول SIM800
  // if (sim800.available()) {
  //   String response = sim800.readStringUntil('\n');
  //   response.trim();
  //   if (response.length() > 0)
  //     Serial.println(response);
  // }
}

void processCommand(String cmd) {
  // مثال: SMS:09123456789:سلام
  int sep = cmd.indexOf(':', 4);
  if (sep != -1) {
    String number = cmd.substring(4, sep);
    String message = cmd.substring(sep + 1);
    sendSMS(number, message);
  }
}

void sendSMS(String number, String message) {
  sim800.println("AT+CMGF=1"); delay(500);
  sim800.print("AT+CMGS=\""); sim800.print(number); sim800.println("\"");
  delay(500);
  sim800.print(message);
  delay(500);
  sim800.write(26);  // Ctrl+Z
  delay(2000);
  Serial.println("SMS Sent.");
}
