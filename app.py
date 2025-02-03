from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
import eventlet

app = Flask(__name__)

# فعال کردن CORS برای سایت شما
socketio = SocketIO(app, cors_allowed_origins=["https://yourdomain.com"])

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('offer')
def handle_offer(data):
    emit('offer', data, broadcast=True)

@socketio.on('answer')
def handle_answer(data):
    emit('answer', data, broadcast=True)

@socketio.on('candidate')
def handle_candidate(data):
    emit('candidate', data, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Render به طور خودکار PORT را تنظیم می‌کند
    socketio.run(app, host="0.0.0.0", port=port)  # بدون debug=True
