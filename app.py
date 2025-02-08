from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room

# Next two lines are for the issue: https://github.com/miguelgrinberg/python-engineio/issues/142
from engineio.payload import Payload
import os
import uuid

Payload.max_decode_packets = 200

app = Flask(__name__)
app.config['SECRET_KEY'] = "thisismys3cr3tk3y"

socketio = SocketIO(app, cors_allowed_origins="*")


_users_in_room = {} # stores room wise user list
_room_of_sid = {} # stores room joined by an used
_name_of_sid = {} # stores display name of users


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        room_id = request.form['room_id']
        return redirect(url_for("entry_checkpoint", room_id=room_id))

    return render_template("home.html")


import uuid
from flask import jsonify

@app.route("/create-room/", methods=["GET"])
def create_room():
    room_id = str(uuid.uuid4())[:8]  # ایجاد یک شناسه یکتا برای اتاق (8 کاراکتری)
    user1_id = str(uuid.uuid4())[:8]  # ایجاد شناسه یکتا برای کاربر 1
    user2_id = str(uuid.uuid4())[:8]  # ایجاد شناسه یکتا برای کاربر 2

    base_url = request.host_url.replace("http", "http")  # تبدیل HTTP به HTTPS

    room_links = {
        "user1_link": f"{base_url}room/{room_id}/{user1_id}",
        "user2_link": f"{base_url}room/{room_id}/{user2_id}"
    }

    return jsonify(room_links)

# @app.route("/room/<string:room_id>/")
# def enter_room(room_id):
#     if room_id not in session:
#         return redirect(url_for("entry_checkpoint", room_id=room_id))
#     return render_template("chatroom.html", room_id=room_id, display_name=session[room_id]["name"], mute_audio=session[room_id]["mute_audio"], mute_video=session[room_id]["mute_video"])

@app.route("/room/<string:room_id>/<string:user_id>/")
def enter_room(room_id, user_id):
    return render_template("chatroom.html", room_id=room_id, user_id=user_id)

@app.route("/room/<string:room_id>/checkpoint/", methods=["GET", "POST"])
def entry_checkpoint(room_id):
    print(request.method)
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


# @socketio.on("join-room")
# def on_join_room(data):
#     print(43)
#     sid = request.sid
#     room_id = data["room_id"]
#     display_name = session[room_id]["name"]
#
#     # register sid to the room
#     join_room(room_id)
#     _room_of_sid[sid] = room_id
#     _name_of_sid[sid] = display_name
#
#     # broadcast to others in the room
#     print("[{}] New member joined: {}<{}>".format(room_id, display_name, sid))
#     emit("user-connect", {"sid": sid, "name": display_name}, broadcast=True, include_self=False, room=room_id)
#
#     # add to user list maintained on server
#     if room_id not in _users_in_room:
#         _users_in_room[room_id] = [sid]
#         emit("user-list", {"my_id": sid}) # send own id only
#     else:
#         usrlist = {u_id:_name_of_sid[u_id] for u_id in _users_in_room[room_id]}
#         emit("user-list", {"list": usrlist, "my_id": sid}) # send list of existing users to the new member
#         _users_in_room[room_id].append(sid) # add new member to user list maintained on server
#
#     print("\nusers: ", _users_in_room, "\n")


@socketio.on("join-room")
def on_join_room(data):
    room_id = data["room_id"]
    user_id = data["user_id"]
    sid = request.sid  # شناسه سوکت کاربر

    # اگر اتاق وجود نداشته باشد، ایجادش می‌کنیم
    if room_id not in _users_in_room:
        _users_in_room[room_id] = {}

    # اضافه کردن کاربر به اتاق
    join_room(room_id)
    _users_in_room[room_id][sid] = user_id
    _room_of_sid[sid] = room_id

    # ارسال لیست کاربران به اعضای اتاق
    emit("user-list", {"list": list(_users_in_room[room_id].values())}, room=room_id)

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

@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid

    # بررسی کنیم که آیا کاربر در اتاق‌ها ثبت شده یا نه
    if sid not in _room_of_sid:
        print(f"[Warning] SID {sid} not found in _room_of_sid. Ignoring disconnect.")
        return

    room_id = _room_of_sid.pop(sid, None)
    display_name = _name_of_sid.pop(sid, "Unknown")

    print(f"[{room_id}] Member left: {display_name} <{sid}>")
    emit("user-disconnect", {"sid": sid}, broadcast=True, include_self=False, room=room_id)

    # به جای `remove(sid)`, از `pop(sid, None)` برای حذف از دیکشنری استفاده می‌کنیم
    if room_id in _users_in_room:
        _users_in_room[room_id].pop(sid, None)  # ✅ حذف `sid` از دیکشنری

        # اگر اتاق خالی شد، آن را پاک کنیم
        if not _users_in_room[room_id]:
            del _users_in_room[room_id]

    print("\nusers: ", _users_in_room, "\n")


# @socketio.on("data")
# def on_data(data):
#     sender_sid = data['sender_id']
#     target_sid = data['target_id']
#     if sender_sid != request.sid:
#         print("[Not supposed to happen!] request.sid and sender_id don't match!!!")
#
#     if data["type"] != "new-ice-candidate":
#         print('{} message from {} to {}'.format(data["type"], sender_sid, target_sid))
#     socketio.emit('data', data, room=target_sid)

@socketio.on("data")
def on_data(data):
    if 'sender_id' not in data or 'target_id' not in data:
        print("Error: Missing sender_id or target_id in data:", data)
        return  # از ادامه‌ی پردازش جلوگیری کن

    sender_sid = data['sender_id']
    target_sid = data['target_id']

    if sender_sid != request.sid:
        print("[Error] sender_id doesn't match request.sid!")

    if data["type"] != "new-ice-candidate":
        print('{} message from {} to {}'.format(data["type"], sender_sid, target_sid))

    socketio.emit('data', data, room=target_sid)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # تنظیم پورت مناسب
    socketio.run(app, host='0.0.0.0', port=port)
    # socketio.run(app, debug=True)