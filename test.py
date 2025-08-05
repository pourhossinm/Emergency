import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports

# تابع برای گرفتن لیست پورت‌ها
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


def connect_serial():
    selected_port = port_combo.get()

    if selected_port:
        try:
            # تبدیل COM10 به \\.\COM10 برای پورت‌های بالا
            if selected_port.startswith("COM") and int(selected_port[3:]) > 9:
                selected_port = f"\\\\.\\{selected_port}"

            ser = serial.Serial(selected_port, 4800, timeout=1)
            messagebox.showinfo("اتصال موفق", f"اتصال به {selected_port} با baudrate 4800 برقرار شد.")
            ser.close()
        except serial.SerialException as e:
            messagebox.showerror("خطا", f"اتصال ناموفق: {e}")
    else:
        messagebox.showwarning("هشدار", "لطفاً یک پورت را انتخاب کنید.")

# رابط گرافیکی
root = tk.Tk()
root.title("اتصال به پورت سریال")
root.geometry("300x150")

tk.Label(root, text="انتخاب پورت COM:").pack(pady=10)

# کمبوباکس پورت‌ها
ports = list_serial_ports()
port_combo = ttk.Combobox(root, values=ports, state="readonly")
port_combo.pack()

# دکمه اتصال
connect_button = tk.Button(root, text="اتصال", command=connect_serial)
connect_button.pack(pady=20)

root.mainloop()
