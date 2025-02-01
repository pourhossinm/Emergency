#include <SoftwareSerial.h>

SoftwareSerial sim800(3, 2); // RX, TX

void sendSMS_UCS2(const char* phoneNumber, const char* textUCS2) {
    sim800.println("AT+CMGF=1");  // حالت متنی
    delay(500);

    sim800.println("AT+CSCS=\"UCS2\"");  // استفاده از UCS2
    delay(500);

    sim800.println("AT+CSMP=17,167,0,8");  // تنظیمات مناسب UCS2
    delay(500);

    sim800.print("AT+CMGS=\"");
    sim800.print(phoneNumber);  // شماره گیرنده (قبلاً UCS2 شده)
    sim800.println("\"");
    delay(1000);

    sim800.print(textUCS2);  // متن پیامک در قالب UCS2 HEX
    delay(500);

    sim800.write(26);  // ارسال Ctrl+Z
    delay(3000);

    Serial.println("✅ پیامک ارسال شد!");
}

void setup() {
    Serial.begin(9600);
    sim800.begin(9600);

    Serial.println("Initializing SIM800L...");
    delay(1000);

    // شماره گیرنده (به UCS2 تبدیل شده)
    const char* phoneUCS2 = "002B003900380039003100380038003100330038003300350036";

    // متن پیامک فارسی (به UCS2 تبدیل شده)
    const char* textUCS2 = "06330644062706450020062706CC06460020062A0633062A002006330627064506270646064700200627064806310698062706460633002006270633062A002E062706CC0646062A06310646062A0020062E0648062F002006310627002006410639062706440020064800200628064700200631064806CC0020064406CC064606A90020063206CC063100200636063106280647002006280632064606CC062F0020007700770077002E006900720061006E002E00690072";

    // ارسال پیامک
    sendSMS_UCS2(phoneUCS2, textUCS2);

    // بازگشت به ASCII برای ارسال‌های بعدی
    sim800.println("AT+CSCS=\"GSM\"");
    delay(500);
}

void loop() {}
