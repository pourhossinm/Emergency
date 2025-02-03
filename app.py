from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# ذخیره کاربران در یک اتاق مشترک
users = {}

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("join")
def handle_join():
    sid = request.sid  # دریافت ID کاربر
    users[sid] = sid  # ثبت کاربر
    print(f"User {sid} joined")

    if len(users) == 2:  # اگر دو کاربر متصل شده‌اند
        user_list = list(users.keys())
        emit("start_call", {"peer": user_list[1]}, room=user_list[0])  # به کاربر اول اعلام کن
        emit("start_call", {"peer": user_list[0]}, room=user_list[1])  # به کاربر دوم اعلام کن

@socketio.on("offer")
def handle_offer(data):
    emit("offer", data, broadcast=True)

@socketio.on("answer")
def handle_answer(data):
    emit("answer", data, broadcast=True)

@socketio.on("candidate")
def handle_candidate(data):
    emit("candidate", data, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    socketio.run(app, host="0.0.0.0", port=port)
