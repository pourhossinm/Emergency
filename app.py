from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)


socketio = SocketIO(app, cors_allowed_origins="*")

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
    port = int(os.environ.get("PORT", 5000))  # مقدار پیش‌فرض 5000 است، اگر PORT موجود نباشد
    socketio.run(app, debug=True, port=port, allow_unsafe_werkzeug=True)
    # app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)

