import eventlet
eventlet.monkey_patch()

from database import create_tables, add_closed_room, is_room_closed
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room

# Next two lines are for the issue: https://github.com/miguelgrinberg/python-engineio/issues/142
from engineio.payload import Payload
import os
import uuid



Payload.max_decode_packets = 200

app = Flask(__name__)
app.config['SECRET_KEY'] = "thisismys3cr3tk3y"

# socketio = SocketIO(app, cors_allowed_origins="*")
socketio = SocketIO(app, async_mode='eventlet')


_users_in_room = {} # stores room wise user list
_room_of_sid = {} # stores room joined by an used
_name_of_sid = {} # stores display name of users

_room_owner = {}  # ذخیره user1_id برای هر اتاق
user_room_mapping = {}  # نگاشت SID به Room برای ارسال موقعیت

create_tables()
@app.route("/create-room/", methods=["GET"])
def create_room():
    room_id = str(uuid.uuid4())[:8]  # ایجاد یک شناسه یکتا برای اتاق (8 کاراکتری)
    user1_id = str(uuid.uuid4())[:8]  # ایجاد شناسه یکتا برای کاربر 1
    user2_id = str(uuid.uuid4())[:8]  # ایجاد شناسه یکتا برای کاربر 2

    base_url = request.host_url.replace("http", "http")  # تبدیل HTTP به HTTPS

    # ذخیره مالک اتاق (کاربر 1)
    _room_owner[room_id] = user1_id

    room_links = {
        "user1_link": f"{base_url}room/{room_id}/{user1_id}",
        "user2_link": f"{base_url}room/{room_id}/{user2_id}"
    }

    return jsonify(room_links)



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        room_id = request.form['room_id']
        return redirect(url_for("entry_checkpoint", room_id=room_id))

    return render_template("home.html")

# @app.route("/room/<string:room_id>/<string:user_id>/")
# def enter_room(room_id, user_id):
#     session[room_id] = {"name": user_id, "mute_audio":0, "mute_video":0}
#     return render_template("chatroom.html", room_id=room_id, user_id=user_id)


@app.route("/room/<string:room_id>/<string:user_id>/")
def enter_room(room_id, user_id):
    if is_room_closed(room_id):  # بررسی بسته بودن اتاق
        return "این اتاق بسته شده است و دیگر قابل دسترسی نیست.", 403  # پاسخ مناسب

    # اگر این اولین کاربری است که وارد اتاق می‌شود، آن را مالک اتاق در نظر بگیریم
    if room_id not in _room_owner:
        _room_owner[room_id] = user_id  # اولین کاربر را به عنوان user1 ذخیره کنیم

    session[room_id] = {"name": user_id, "mute_audio": 0, "mute_video": 0}
    return render_template("chatroom.html", room_id=room_id, user_id=user_id)


@app.route("/room/<string:room_id>/checkpoint/", methods=["GET", "POST"])
def entry_checkpoint(room_id):
    if request.method == "POST":
        display_name = request.form['display_name']
        mute_audio = request.form['mute_audio']
        mute_video = request.form['mute_video']
        session[room_id] = {"name": display_name, "mute_audio":mute_audio, "mute_video":mute_video}
        print(session[room_id])
        return redirect(url_for("enter_room", room_id=room_id))

    print(f"chatroom_checkpoint.html   {room_id}")
    return render_template("chatroom_checkpoint.html", room_id=room_id)



@socketio.on("connect")
def on_connect():
    sid = request.sid
    print("New socket connected ", sid)


@socketio.on("join-room")
def on_join_room(data):
    sid = request.sid
    room_id = data["room_id"]
    display_name = session[room_id]["name"]

    # register sid to the room
    join_room(room_id)
    _room_of_sid[sid] = room_id
    user_room_mapping[sid] = room_id
    _name_of_sid[sid] = display_name

    # broadcast to others in the room
    print("[{}] New member joined: {}<{}>".format(room_id, display_name, sid))
    emit("user-connect", {"sid": sid, "name": display_name}, broadcast=True, include_self=False, room=room_id)

    # add to user list maintained on server
    if room_id not in _users_in_room:
        _users_in_room[room_id] = [sid]
        emit("user-list", {"my_id": sid}) # send own id only
    else:
        usrlist = {u_id:_name_of_sid[u_id] for u_id in _users_in_room[room_id]}
        emit("user-list", {"list": usrlist, "my_id": sid}) # send list of existing users to the new member
        _users_in_room[room_id].append(sid) # add new member to user list maintained on server

    print("\nusers: ", _users_in_room, "\n")


# @socketio.on("disconnect")
# def on_disconnect():
#     sid = request.sid
#     room_id = _room_of_sid[sid]
#     display_name = _name_of_sid[sid]
#
#     print("[{}] Member left: {}<{}>".format(room_id, display_name, sid))
#     emit("user-disconnect", {"sid": sid}, broadcast=True, include_self=False, room=room_id)
#
#     _users_in_room[room_id].remove(sid)
#     if len(_users_in_room[room_id]) == 0:
#         _users_in_room.pop(room_id)
#
#     _room_of_sid.pop(sid)
#     _name_of_sid.pop(sid)
#
#     print("\nusers: ", _users_in_room, "\n")

_closed_rooms = set()  # لیست اتاق‌های بسته‌شده

@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    room_id = _room_of_sid.get(sid)

    if not room_id:
        return

    display_name = _name_of_sid[sid]

    print("[{}] Member left: {}<{}>".format(room_id, display_name, sid))
    emit("user-disconnect", {"sid": sid}, broadcast=True, include_self=False, room=room_id)

    _users_in_room[room_id].remove(sid)

    # اگر کاربری که خارج شده، همان user1_id باشد، اتاق را در دیتابیس ثبت کنیم
    if _room_owner.get(room_id) == display_name:
        print(f"Closing room {room_id} because user1_id left.")
        _users_in_room.pop(room_id, None)
        add_closed_room(room_id)  # ثبت اتاق در دیتابیس
        _room_owner.pop(room_id, None)  # حذف مالک اتاق

    _room_of_sid.pop(sid, None)
    _name_of_sid.pop(sid, None)
    user_room_mapping.pop(sid, None)

    print("\nActive rooms: ", _users_in_room, "\n")

@socketio.on("data")
def on_data(data):
    print(data)
    sender_sid = data['sender_id']
    target_sid = data['target_id']

    # بررسی معتبر بودن ارتباط فرستنده
    if sender_sid != request.sid:
        print("[WARNING] sender_id and actual request.sid don't match!")
        return

    # بررسی وجود target در لیست کاربران فعلی
    if target_sid not in _room_of_sid:
        print(f"[ERROR] target_sid {target_sid} not connected. Dropping message.")
        return

    # بررسی اینکه target در همان اتاق است
    sender_room = _room_of_sid.get(sender_sid)
    target_room = _room_of_sid.get(target_sid)

    if sender_room != target_room:
        print(f"[WARNING] sender and target not in same room: {sender_room} ≠ {target_room}")
        return

    # ارسال پیام به target
    socketio.emit('data', data, room=target_sid)

@socketio.on('bttn_location')
def handle_send_location(data):
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    room = data.get('room')

    if latitude is None or longitude is None:
        emit('location_debug', {'message': '⚠️ مختصات ناقص دریافت شد.'}, to=request.sid)
        return

    msg = f"📍 لوکیشن دریافت شد: lat={latitude}, lon={longitude}, room={room}"
    emit('location_debug', {'message': msg}, to=request.sid)

    # ارسال لوکیشن به دیگران
    emit('receive_location', data, room=room, include_self=False)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # تنظیم پورت مناسب
    socketio.run(app, host='0.0.0.0', port=port)
    # socketio.run(app, debug=True)

    # port = int(os.environ.get("PORT", 5000))
    # socketio.run(app, host='127.0.0.1', port=port, debug=True)