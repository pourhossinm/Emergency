import serial
import time
import threading

# تبدیل متن به UCS2 HEX
def to_ucs2_hex(text):
    return ''.join(f"{ord(c):04X}" for c in text)

# تنظیمات سریال
ser = serial.Serial('COM3', 9600, timeout=1)  # پورت سریال را متناسب با سیستم تغییر دهید
time.sleep(2)  # زمان برای برقراری ارتباط

# تابع خواندن داده‌های سریال و نمایش در کنسول پایتون
def read_from_serial():
    while True:
        if ser.in_waiting > 0:
            serial_data = ser.readline().decode("utf-8").strip()
            print(f"📡 آردوینو → {serial_data}")  # نمایش پیام‌های دریافتی

# شروع خواندن سریال در یک ترد جداگانه (برای نمایش هم‌زمان پیام‌ها)
threading.Thread(target=read_from_serial, daemon=True).start()

while True:
    phone_number = input("📲 شماره گیرنده (+98XXXXXXXXXX): ")
    message_text = input("💬 متن پیامک: ")

    phone_ucs2 = to_ucs2_hex(phone_number)
    text_ucs2 = to_ucs2_hex(message_text)

    data_to_send = f"{phone_ucs2},{text_ucs2}\n"

    ser.write(data_to_send.encode())  # ارسال داده به آردوینو
    print("🚀 پیام به آردوینو ارسال شد!")
    time.sleep(3)  # تاخیر بین ارسال‌ها
