from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

users = []  # لیست کاربران متصل

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("join")
def handle_join():
    sid = request.sid
    users.append(sid)

    print(f"User {sid} joined. Total users: {len(users)}")

    if len(users) == 2:  # اگر دو نفر وصل شدند، ارتباط را شروع کن
        emit("start_call", {"peer": users[1]}, room=users[0])
        emit("start_call", {"peer": users[0]}, room=users[1])

@socketio.on("offer")
def handle_offer(data):
    emit("offer", data, broadcast=True)

@socketio.on("answer")
def handle_answer(data):
    emit("answer", data, broadcast=True)

@socketio.on("candidate")
def handle_candidate(data):
    emit("candidate", data, broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    if sid in users:
        users.remove(sid)
    print(f"User {sid} disconnected. Remaining users: {len(users)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    socketio.run(app, host="0.0.0.0", port=port)
