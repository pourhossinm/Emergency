import serial
import time
import threading
import tkinter as tk
from tkinter import messagebox, ttk

import sqlite3
import webbrowser
import uuid

# تنظیمات سریال
try:
    ser = serial.Serial('COM3', 9600, timeout=1)  # پورت سریال را متناسب با سیستم تغییر دهید
    time.sleep(2)  # زمان برای برقراری ارتباط
except:
    print("خطا در پورت COM")

#تنظیم database
conn = sqlite3.connect("Emergency.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Emergency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Phone TEXT NOT NULL,
    Message TEXT NOT NULL
)
""")
conn.commit()


def fetch_data():
    """دریافت اطلاعات از دیتابیس و نمایش در جدول"""
    for row in tree.get_children():
        tree.delete(row)  # پاک کردن اطلاعات قبلی جدول

    cursor.execute("SELECT  Phone, Message FROM Emergency")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)


# تبدیل متن به UCS2 HEX
def to_ucs2_hex(text):
    return ''.join(f"{ord(c):04X}" for c in text)

# تابع خواندن داده‌های سریال و نمایش در کنسول پایتون
# def read_from_serial():
#     while True:
#         if ser.in_waiting > 0:
#             serial_data = ser.readline().decode("utf-8").strip()
#             messagebox.showinfo("آردینو",f"📡 آردوینو → {serial_data}")  # نمایش پیام‌های دریافتی

def send_sms(phone, message):
    # شروع خواندن سریال در یک ترد جداگانه (برای نمایش هم‌زمان پیام‌ها)
    # threading.Thread(target=read_from_serial, daemon=True).start()

    phone_ucs2 = to_ucs2_hex(phone)
    text_ucs2 = to_ucs2_hex(message)

    data_to_send = f"{phone_ucs2},{text_ucs2}\n"

    ser.write(data_to_send.encode())  # ارسال داده به آردوینو
    messagebox.showinfo("ارسال پیام","🚀 پیام به آردوینو ارسال شد!")
    cursor.execute("INSERT INTO Emergency (Phone, Message) VALUES (?, ?)", (phone, message))
    conn.commit()
    fetch_data()  # به‌روز‌رسانی جدول
    entry_phone.delete(0, tk.END)
    # entry_message.delete(0, tk.END)
    messagebox.showinfo("ثبت موفق", "اطلاعات با موفقیت ذخیره شد!")
    time.sleep(3)  # تاخیر بین ارسال‌ها


def open_url():
    """باز کردن آدرس داخل entry در مرورگر"""
    url = entry_url.get()
    if url:
        if not url.startswith("http"):
            url = "http://" + url  # در صورت نداشتن http:// آن را اضافه می‌کنیم
        webbrowser.open(url)
    else:
        messagebox.showwarning("خطا", "لطفاً یک آدرس وارد کنید!")
def submit():
    Phone = entry_phone.get()
    uuid_user1 = str(uuid.uuid4())[:4]
    uuid_user2 = str(uuid.uuid4())[:4]

    farsi_message = "کلیک کنید."
    temp_link = f"http://emergency-7a6k.onrender.com/room/{Phone}/{uuid_user1}"
    entry_url.insert(0, temp_link)
    temp_message = f"{farsi_message} http://emergency-7a6k.onrender.com/room/{Phone}/{uuid_user2}"
    Messgae = temp_message

    if Phone and Messgae:
        send_sms(Phone, Messgae)
    else:
        messagebox.showwarning("خطا!", "اطلاعات ورودی صحیح نیست!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("فرم دریافت اطلاعات")
    root.geometry("600x400")

    tk.Label(root, text="شماره تماس:").pack(pady=5)
    entry_phone = tk.Entry(root)
    entry_phone.pack(pady=5)

    # tk.Label(root, text="پیام:").pack(pady=5)
    # entry_message = tk.Entry(root)
    # entry_message.pack(pady=5)

    # لیبل و ورودی آدرس وب
    tk.Label(root, text="آدرس وب:").pack(pady=5)
    entry_url = tk.Entry(root)
    entry_url.pack(pady=5)

    # دکمه باز کردن لینک در مرورگر
    btn_open_url = tk.Button(root, text="باز کردن لینک", command=open_url)
    btn_open_url.pack(pady=10)

    btn_submit = tk.Button(root, text="ارسال پیام", command=submit)
    btn_submit.pack(pady=5)

    # نمایش جدول (Treeview)
    columns = ( "شماره تماس", "پیام")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("شماره تماس", text="شماره تماس")
    tree.heading("پیام", text="پیام")

    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    fetch_data()

    root.mainloop()

    conn.close()





