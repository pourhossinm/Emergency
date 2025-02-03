from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

app = Flask(__name__)
socketio = SocketIO(app)

clients = {}  # ذخیره کلاینت‌ها بر اساس اتاق

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    clients[username] = room  # ذخیره نام کاربر به همراه اتاقی که در آن حضور دارد
    join_room(room)
    emit('message', {'message': f'{username} has entered the room.'}, room=room)

@socketio.on('offer')
def handle_offer(data):
    room = data['room']
    emit('offer', data, room=room)  # ارسال پیشنهاد به اتاق مورد نظر

@socketio.on('answer')
def handle_answer(data):
    room = data['room']
    emit('answer', data, room=room)  # ارسال پاسخ به اتاق مورد نظر

@socketio.on('candidate')
def handle_candidate(data):
    room = data['room']
    emit('candidate', data, room=room)  # ارسال candidate به اتاق مورد نظر

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # تنظیم پورت مناسب
    socketio.run(app, host='0.0.0.0', port=port)
