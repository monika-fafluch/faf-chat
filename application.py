import os
import json

from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, send, join_room
from flask_session import Session
from datetime import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

messages = {}
channels_list = []

"""@app.route('/')
def index():
    return render_template("index-test.html")

@app.route('/channel1')
def channel1():
    return render_template("channel1.html")

@app.route('/channel2')
def channel2():
    return render_template("channel2.html")

@socketio.on('join')
def on_join(room):
    print(f"joined room is: {room}")
    join_room(room)
    send(' username has entered the room.', room=room)

@socketio.on('message')
def handleMessage(msg):
    print(f"message is: {msg}")
    emit('message', msg, broadcast=True)"""





def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        """if "last_channel" not in session:
            return render_template("index.html")
        else:
            print(session["last_channel"])
            channel = session["last_channel"]
            return redirect(url_for('channel', channel=channel))"""
        return render_template("index.html")
    else:
        name = request.form.get("name")
        session["username"] = name
        return redirect('/create_channel')

@app.route('/create_channel', methods=["GET", "POST"])
def create_channel():
    if request.method == "GET":
        return render_template("create_channel.html")
    else:
        # get a user input/channel's name
        channel = request.form.get("create-channel")
        # check if exists
        if channel in channels_list:
            return render_template("create_channel_error.html")
        # save the channel as last channel in user's session
        session["last_channel"] = channel
        # append channel to exisiting channels list
        channels_list.append(channel)

        # create a list for this channel in 'messages' dict
        messages[channel] = []

        return redirect('/channels')

@app.route('/channels')
def channels():

    return render_template("channels.html", channels_list=channels_list)

@app.route('/channels/<channel>', methods=["GET", "POST"])
def channel(channel):
    messages_channel = []
    session["saved"] = channel
    # read messages from 'messages' dict in the channel's list
    """if "channel" in messages:
        end = len(messages[channel]) - 100
        if len(messages[channel]) > 100:
            del messages[channel][0:end]
        # save the channel as the last channel in user's session
        session["last_channel"] = channel"""
        # CHECK LATER IF NECCESSARY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    for msg in messages[channel]:
        messages_channel.append(msg)

       
    return render_template("channel.html", channel=channel, messages_channel=messages_channel)


"""@socketio.on('join')
def on_join(room):
    print(f"joined channel is: {room}")
    username = session.get("name")
    join_room(room)
    data = {"username": username, "room": room}
    emit('join', data)"""


@socketio.on('send message')
def handleMessage(data):
    # get user's name and sent message
    print(f"sent data is: {data}")
    message = data["message"]
    name = data["name"]
    date = data["date"]
    room = session.get("saved")
    join_room(room)
    print(f"room is: {room}")
    # save data into messages dict   
    """if room not in messages:
        messages[room] = []"""
    messages[room].append(message)
    

    emit("announce message", {"message": message, "date": date, "name": name}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)