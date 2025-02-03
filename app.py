from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

app = Flask(__name__)
socketio = SocketIO(app)

clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    clients[username] = room
    join_room(room)
    emit('message', {'message': f'{username} has entered the room.'}, room=room)

@socketio.on('offer')
def handle_offer(data):
    emit('offer', data, room=data['room'])

@socketio.on('answer')
def handle_answer(data):
    emit('answer', data, room=data['room'])

@socketio.on('candidate')
def handle_candidate(data):
    emit('candidate', data, room=data['room'])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # تغییر به پورت 10000
    socketio.run(app, host='0.0.0.0', port=port)
