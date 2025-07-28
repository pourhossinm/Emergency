#include <SoftwareSerial.h>

SoftwareSerial sim800(3, 2); // RX, TX برای SIM800

String callerNumber = "";

void setup() {
  Serial.begin(4800);     
  sim800.begin(4800);  

  sim800.println("AT+CLIP=1"); // فعال کردن نمایش Caller ID   

  Serial.println("SIM800 Ready. Send 'ATA' to answer call.");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.equalsIgnoreCase("ATA")) {
      sim800.println("ATA");
      Serial.println(">> Sent 'ATA' to SIM800");
    }
    else if 
    (command.equalsIgnoreCase("ATH")) {
      sim800.println("ATH");
      Serial.println(">> Sent 'ATH' to SIM800");
    }
  }

  if (sim800.available()) {
    String response = sim800.readStringUntil('\n');
    response.trim();
    if (response.length() > 0) {
      Serial.println("SIM800: " + response);
      if (response.startsWith("+CLIP:")) {
        int quote1 = response.indexOf('"');
        int quote2 = response.indexOf('"', quote1 + 1);
        if (quote1 != -1 && quote2 != -1) {
          callerNumber = response.substring(quote1 + 1, quote2);
          Serial.println("CALLER:" + callerNumber); // ارسال برای پایتون
        }
      }
    

    }
  }
}


  // // دریافت پاسخ از SIM800
  // if (sim800.available()) {
  //   String response = sim800.readStringUntil('\n');
  //   response.trim();

  //   if (response.length() > 0) {
  //     Serial.println("SIM800: " + response);

  //     // اگر شماره تماس‌گیرنده دریافت شد
  //     if (response.startsWith("+CLIP:")) {
  //       int quote1 = response.indexOf('"');
  //       int quote2 = response.indexOf('"', quote1 + 1);
  //       if (quote1 != -1 && quote2 != -1) {
  //         callerNumber = response.substring(quote1 + 1, quote2);
  //         Serial.println("CALLER:" + callerNumber); // ارسال برای پایتون
  //       }
  //     }
