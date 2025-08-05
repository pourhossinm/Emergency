import serial
import time
import threading
import tkinter as tk
from tkinter import messagebox, ttk

import sqlite3
import webbrowser
import uuid

import threading
import serial.tools.list_ports
import chardet

# تنظیمات سریال
# try:
#     ser = serial.Serial('COM5', 4800, timeout=1)  # پورت سریال را متناسب با سیستم تغییر دهید
#     time.sleep(2)  # زمان برای برقراری ارتباط
# except:
#     print("خطا در پورت COM")

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


def on_row_double_click(event):
    selected_item = tree.focus()  # گرفتن آیتم انتخاب‌شده
    if not selected_item:
        return

    item_values = tree.item(selected_item, "values")  # گرفتن مقادیر هر ستون
    if len(item_values) >= 3:
        # caller_id.delete(0, tk.END)
        caller_id.config(text= item_values[0])

        entry_phone.delete(0, tk.END)
        entry_phone.insert(0, item_values[1])

        entry_url.delete(0, tk.END)
        entry_url.insert(0, item_values[2])


def fetch_data():
    """دریافت اطلاعات از دیتابیس و نمایش در جدول"""
    for row in tree.get_children():
        tree.delete(row)  # پاک کردن اطلاعات قبلی جدول

    cursor.execute("SELECT  id, Phone, Message FROM Emergency order by id DESC")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

# تابع برای گرفتن لیست پورت‌ها
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# تابع اتصال به پورت

def connect_serial():
    selected_port = port_combo.get()
    global ser

    if selected_port:
        try:
            # تبدیل COM10 به \\.\COM10 برای پورت‌های بالا
            if selected_port.startswith("COM") and int(selected_port[3:]) > 9:
                selected_port = f"\\\\.\\{selected_port}"

            ser = serial.Serial(selected_port, 4800, timeout=1)
            time.sleep(2)
            ser.write(b'ping\n')  # اگر آردوینو قراره جواب بده
            response = ser.readline().decode('utf-8').strip()

            if response:
                caller_label.config(text=" متصل است. ")
            else:
                caller_label.config(text="هیچ پاسخی  دریافت نشد.")
                ser.close()

        except serial.SerialException as e:
            messagebox.showerror("خطا", f"اتصال ناموفق: {e}")
    else:
        messagebox.showwarning("هشدار", "لطفاً یک پورت را انتخاب کنید.")



def send_sms(phone, message):
    try:
        data_to_send = f"SMS:{phone}:{message}\n"  # فرمت مورد انتظار آردوینو
        ser.write(data_to_send.encode("utf-8"))
        cursor.execute("INSERT INTO Emergency (Phone, Message) VALUES (?, ?)", (phone, message))
        conn.commit()
        fetch_data()  # به‌روز‌رسانی جدول
        # entry_phone.delete(0, tk.END)
        # entry_message.delete(0, tk.END)
        messagebox.showinfo("ثبت موفق", "اطلاعات با موفقیت ذخیره شد!")
        # time.sleep(3)  # تاخیر بین ارسال‌ها
    except Exception as e:
        print(tk.END, f"خطا در ارسال: {e}\n")


def submit():
    try:

        Phone = entry_phone.get()
        uuid_user1 = str(uuid.uuid4())[:4]
        uuid_user2 = str(uuid.uuid4())[:4]

        temp_link = f"https://emergency-7a6k.onrender.com/room/{Phone}/{uuid_user1}"
        entry_url.insert(0, temp_link)
        temp_message = f"https://emergency-7a6k.onrender.com/room/{Phone}/{uuid_user2}"
        Messgae = temp_message
        print(Messgae)

        if Phone and Messgae:
            send_sms(Phone, Messgae)
        else:
            messagebox.showwarning("خطا!", "اطلاعات ورودی صحیح نیست!")
    except Exception as e:

        print(tk.END, f"خطا در ارسال: {e}\n")


def open_url():
    """باز کردن آدرس داخل entry در مرورگر"""
    url = entry_url.get()
    if url:
        if not url.startswith("http"):
            url = "http://" + url  # در صورت نداشتن http:// آن را اضافه می‌کنیم
        webbrowser.open(url)
    else:
        messagebox.showwarning("خطا", "لطفاً یک آدرس وارد کنید!")


def answer_call():
    try:
        ser.write(b'ATA\n')  # ارسال فرمان پاسخ
        line = ser.readline()
        result = chardet.detect(line)
        encoding = result['encoding']
        print("Detected encoding:", encoding)
        print("Decoded:", line.decode(encoding))

    except Exception as e:

        print(tk.END, f"خطا در ارسال: {e}\n")

def hangup_call():
    try:
        ser.write(b'ATH\n')  # ارسال فرمان پاسخ
        print(ser.readline().decode('utf-8').strip())

    except Exception as e:
        print(tk.END, f"خطا در ارسال: {e}\n")

def del_room():
    try:
        print(caller_id.cget("text"))
        cursor.execute("INSERT INTO chatrooms (room_id) VALUES (?)", (caller_id.cget("text")))
        conn.commit()
    except:
        pass



def read_serial():
    try:
        while True:
            if ser.in_waiting:
                line = ser.readline().decode(errors='ignore').strip()
                if line:
                    print("From Arduino:", line)
                    if line.startswith("CALLER:"):
                        number = line.replace("CALLER:", "")
                        caller_label.config(text=f"شماره تماس گیرنده:\n{number}")
                        print(tk.END, f"تماس از: {number}\n")
                    else:
                        print(tk.END, f"{line}\n")
    except:
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("فرم دریافت اطلاعات")
    root.geometry("800x600")

    # پیکربندی ستون‌ها برای چینش بهتر
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    # لیبل و کمبوباکس پورت
    tk.Label(root, text="انتخاب پورت COM:").grid(row=0, column=1, pady=10, sticky="e")
    ports = list_serial_ports()
    port_combo = ttk.Combobox(root, values=ports, state="readonly", justify="right")
    port_combo.grid(row=0, column=0, pady=10, sticky="w")

    # دکمه اتصال
    connect_button = tk.Button(root, text="اتصال", command=connect_serial)
    connect_button.grid(row=1, column=0, columnspan=2, pady=10)

    # لیبل وضعیت تماس
    caller_label = tk.Label(root, text="در انتظار اتصال ...", font=('Arial', 14))
    caller_label.grid(row=2, column=0, columnspan=2, pady=10)

    # لیبل و ورودی شماره تماس
    tk.Label(root, text="شماره تماس:").grid(row=3, column=1, sticky="e")
    entry_phone = tk.Entry(root, justify="right")
    entry_phone.grid(row=3, column=0, pady=5, sticky="w")

    # لیبل کد تماس‌گیرنده
    caller_id = tk.Label(root, text="کد", font=('Arial', 8), justify="right")
    caller_id.grid(row=4, column=0, columnspan=2, pady=5)

    # لیبل و ورودی آدرس وب
    tk.Label(root, text="آدرس وب:").grid(row=5, column=1, sticky="e")
    entry_url = tk.Entry(root, width=60, justify="right")
    entry_url.grid(row=5, column=0, pady=5, sticky="w")

    # دکمه‌ها
    btn_open_url = tk.Button(root, text="باز کردن لینک", command=open_url)
    btn_open_url.grid(row=6, column=0, columnspan=2, pady=5)

    btn_submit = tk.Button(root, text="ارسال پیام", command=submit)
    btn_submit.grid(row=6, column=1, columnspan=2, pady=5)

    btn_response = tk.Button(root, text="پاسخ تماس", command=answer_call)
    btn_response.grid(row=7, column=0, columnspan=2, pady=5)

    btn_hangup = tk.Button(root, text="قطع تماس", command=hangup_call)
    btn_hangup.grid(row=7, column=1, columnspan=2, pady=5)


    # جدول نمایش اطلاعات
    columns = ("کد", "شماره تماس", "پیام")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("کد", text="کد")
    tree.heading("شماره تماس", text="شماره تماس")
    tree.heading("پیام", text="پیام")
    tree.grid(row=8, column=0, columnspan=2, pady=10, sticky="nsew")

    # اتصال دوبار کلیک به جدول
    tree.bind("<Double-1>", on_row_double_click)

    fetch_data()

    try:
        serial_thread = threading.Thread(target=read_serial, daemon=True)
        serial_thread.start()
    except:
        pass

    root.mainloop()
    conn.close()
    try:
        ser.close()
    except:
        print("exit")





