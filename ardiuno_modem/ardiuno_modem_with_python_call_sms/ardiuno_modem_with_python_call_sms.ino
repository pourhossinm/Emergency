#include <SoftwareSerial.h>

SoftwareSerial sim800(3, 2); // RX, TX

String callerNumber = "";
String smsNumber = "";
String smsText = "";

void setup() {
  Serial.begin(4800);     
  sim800.begin(4800);  

  sim800.println("AT+CLIP=1"); // فعال‌سازی نمایش شماره تماس‌گیرنده
  delay(500);

  sim800.println("AT+CMGF=1"); // حالت پیامک به متن
  delay(500);

  Serial.println("SIM800 Ready. Send 'ATA' to answer call.");
}

void loop() {

  // دریافت دستور از پایتون از طریق Serial
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.equalsIgnoreCase("ATA")) {
      sim800.println("ATA");
      Serial.println(">> Sent 'ATA' to SIM800");
    }
    else if (command.equalsIgnoreCase("ATH")) {
      sim800.println("ATH");
      Serial.println(">> Sent 'ATH' to SIM800");
    }
    else if (command.startsWith("SMS:")) {

      parseSMSCommand(command); // تجزیه و ارسال پیامک
    }
  }

  // دریافت پاسخ از SIM800
  if (sim800.available()) {
    String response = sim800.readStringUntil('\n');
    response.trim();

    if (response.length() > 0) {
      Serial.println("SIM800: " + response);

      // اگر شماره تماس‌گیرنده دریافت شد
      if (response.startsWith("+CLIP:")) {
        int quote1 = response.indexOf('"');
        int quote2 = response.indexOf('"', quote1 + 1);
        if (quote1 != -1 && quote2 != -1) {
          callerNumber = response.substring(quote1 + 1, quote2);
          Serial.println("CALLER:" + callerNumber); // ارسال به پایتون
        }
      }
    }
  }
}

// تابع برای تجزیه دستور SMS و ارسال آن
void parseSMSCommand(String cmd) {
  // فرمت: SMS:شماره:متن
  int firstColon = cmd.indexOf(':');
  int secondColon = cmd.indexOf(':', firstColon + 1);

  if (firstColon != -1 && secondColon != -1) {
    smsNumber = cmd.substring(firstColon + 1, secondColon);
    smsText = cmd.substring(secondColon + 1);

    sendSMS(smsNumber, smsText);
  } else {
    Serial.println("⚠️ SMS format error. Use: SMS:number:text");
  }
}

// تابع ارسال پیامک
void sendSMS(String number, String text) {
  sim800.println("AT+CMGF=1"); // حالت متن
  delay(500);

  sim800.print("AT+CMGS=\"");
  sim800.print(number);
  sim800.println("\"");
  delay(500);

  sim800.print(text);
  delay(200);

  sim800.write(26); // CTRL+Z
  delay(3000);

  Serial.println("✅ SMS sent to " + number);
}
