// #include <SoftwareSerial.h>

// SoftwareSerial sim800(3, 2); // RX, TX
// String phoneUCS2, textUCS2;

// void sendSMS(String phoneNumber, String textMessage) {
//     sim800.println("AT+CMGF=1");  
//     delay(500);
    
//     sim800.println("AT+CSCS=\"UCS2\"");  
//     delay(500);
    
//     sim800.println("AT+CSMP=17,167,0,8");  
//     delay(500);

//     sim800.print("AT+CMGS=\"");
//     sim800.print(phoneNumber);
//     sim800.println("\"");
//     delay(1000);

//     sim800.print(textMessage);
//     delay(500);

//     sim800.write(26);  
//     delay(3000);

//     Serial.println("✅ پیامک ارسال شد!");
//     sim800.println("AT+CSCS=\"GSM\"");  
//     delay(500);
// }

// void setup() {
//     Serial.begin(9600);
//     sim800.begin(9600);
//     Serial.println("✅ آماده دریافت پیام از پایتون...");
// }

// void loop() {
//     if (Serial.available()) {
//         String data = Serial.readStringUntil('\n');  // دریافت داده از پایتون
//         int commaIndex = data.indexOf(',');
        
//         if (commaIndex > 0) {
//             phoneUCS2 = data.substring(0, commaIndex);
//             textUCS2 = data.substring(commaIndex + 1);
//             sendSMS(phoneUCS2, textUCS2);
//         }
//     }
// }
#include <SoftwareSerial.h>

SoftwareSerial sim800(3, 2); // RX, TX
String phoneUCS2, textUCS2;

void sendSMS(String phoneNumber, String textMessage) {
    Serial.println("📡 در حال ارسال پیامک...");
    sim800.println("AT+CMGF=1");  
    delay(500);
    
    sim800.println("AT+CSCS=\"UCS2\"");  
    delay(500);
    
    sim800.println("AT+CSMP=17,167,0,8");  
    delay(500);

    sim800.print("AT+CMGS=\"");
    sim800.print(phoneNumber);
    sim800.println("\"");
    delay(1000);

    sim800.print(textMessage);
    delay(500);

    sim800.write(26);  
    delay(3000);

    Serial.println("✅ پیامک ارسال شد!");
    sim800.println("AT+CSCS=\"GSM\"");  
    delay(500);
}

void setup() {
    Serial.begin(9600);
    sim800.begin(9600);
    Serial.println("✅ آماده دریافت پیام از پایتون...");
}

void loop() {
    if (Serial.available()) {
        String data = Serial.readStringUntil('\n');  // دریافت داده از پایتون
        int commaIndex = data.indexOf(',');
        
        if (commaIndex > 0) {
            phoneUCS2 = data.substring(0, commaIndex);
            textUCS2 = data.substring(commaIndex + 1);
            Serial.println("📨 دریافت شماره و پیامک از پایتون...");
            Serial.println("📲 شماره: " + phoneUCS2);
            Serial.println("💬 متن: " + textUCS2);
            sendSMS(phoneUCS2, textUCS2);
        }
    }
}
