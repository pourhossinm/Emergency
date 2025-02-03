from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}  # ذخیره کاربران در اتاق‌های جداگانه

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("join")
def handle_join(data):
    room = data["room"]
    sid = request.sid

    if room not in rooms:
        rooms[room] = []

    rooms[room].append(sid)
    join_room(room)

    print(f"User {sid} joined room {room}")

    if len(rooms[room]) == 2:  # اگر دو کاربر در اتاق باشند
        emit("start_call", room=room)  # به هر دو کاربر بگو که تماس شروع شود

@socketio.on("offer")
def handle_offer(data):
    room = data["room"]
    emit("offer", data, room=room, include_self=False)

@socketio.on("answer")
def handle_answer(data):
    room = data["room"]
    emit("answer", data, room=room, include_self=False)

@socketio.on("candidate")
def handle_candidate(data):
    room = data["room"]
    emit("candidate", data, room=room, include_self=False)

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    for room in rooms:
        if sid in rooms[room]:
            rooms[room].remove(sid)
            leave_room(room)
            if len(rooms[room]) == 0:
                del rooms[room]
            break

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    socketio.run(app, host="0.0.0.0", port=port)
