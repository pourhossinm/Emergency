import serial
import tkinter as tk
import threading

# تنظیمات پورت سریال: پورت را بر اساس سیستم خود تنظیم کن (مثلاً COM3 یا /dev/ttyUSB0)
ser = serial.Serial('COM5', 4800, timeout=1)

def answer_call():
    try:
        ser.write(b'ATA\n')  # ارسال فرمان پاسخ
        log_text.insert(tk.END, "فرمان ATA ارسال شد\n")
    except Exception as e:
        log_text.insert(tk.END, f"خطا در ارسال: {e}\n")

def hangup_call():
    try:
        ser.write(b'ATH\n')  # ارسال فرمان پاسخ
        log_text.insert(tk.END, "فرمان ATH ارسال شد\n")
    except Exception as e:
        log_text.insert(tk.END, f"خطا در ارسال: {e}\n")

def read_serial():
    while True:
        if ser.in_waiting:
            line = ser.readline().decode(errors='ignore').strip()
            if line:
                print("From Arduino:", line)
                if line.startswith("CALLER:"):
                    number = line.replace("CALLER:", "")
                    caller_label.config(text=f"شماره تماس گیرنده:\n{number}")
                    log_text.insert(tk.END, f"تماس از: {number}\n")
                else:
                    log_text.insert(tk.END, f"{line}\n")

# رابط گرافیکی ساده
root = tk.Tk()
root.title("پاسخ تماس با SIM800")

caller_label = tk.Label(root, text="در انتظار تماس...", font=('Arial', 14))
caller_label.pack(pady=10)


btn = tk.Button(root, text="پاسخ به تماس", command=answer_call, font=('Arial', 14), bg='lightgreen')
btn.pack(pady=10)

btn = tk.Button(root, text="قطع تماس تماس", command=hangup_call, font=('Arial', 14), bg='lightgreen')
btn.pack(pady=10)

log_text = tk.Text(root, height=10, width=40, font=('Arial', 12))
log_text.pack()

serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()


root.mainloop()
