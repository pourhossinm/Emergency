import sqlite3

DB_NAME = "chat_rooms.db"


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ایجاد جدول برای ذخیره نام اتاق‌های بسته‌شده
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS closed_rooms (
        room_id TEXT PRIMARY KEY
    )
    """)

    conn.commit()
    conn.close()


def add_closed_room(room_id):
    """ ذخیره نام اتاق بسته‌شده در دیتابیس """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO closed_rooms (room_id) VALUES (?)", (room_id,))
    conn.commit()
    conn.close()


def is_room_closed(room_id):
    """ بررسی اینکه آیا این اتاق در دیتابیس بسته‌شده است یا خیر """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM closed_rooms WHERE room_id = ?", (room_id,))
    result = cursor.fetchone()

    conn.close()
    return result is not None  # اگر مقدار پیدا شد یعنی اتاق بسته است


def remove_closed_room(room_id):
    """ حذف یک اتاق بسته‌شده از دیتابیس (در صورت نیاز) """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM closed_rooms WHERE room_id = ?", (room_id,))
    conn.commit()
    conn.close()
