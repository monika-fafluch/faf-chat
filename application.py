import os
import json

from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_session import Session
import datetime
#from datetime import datetime


app = Flask(__name__)
app.secret_key = '\xd9\xcb\x91\x81$ho\x9fi\xaf[H\xb0\x7f\x0b\x88\xbc\xb8r0\x1e\x08@1'
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

messages = {"general": [], "banhart": [], "the zombies": [], "new order": [], "donovan": [], "ariel pink": []}
rooms = ["general", "banhart", "the zombies", "new order", "donovan", "ariel pink"]



@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'GET':
        # check if user has visisted a channel before
        if "last_channel" in session:
            last_channel = session["last_channel"]
            if last_channel in rooms:
                print(last_channel)
                return redirect(url_for('chat', channel=last_channel))

        return render_template("index.html")  
    
    else:
        # save user's name into session
        session["name"] = request.form.get("name")
        # ensure the channel's name isn't taken
        channel = request.form.get("create-channel")
        if channel:
            if channel in rooms:
                return render_template("index-error.html")
            # save the channel into rooms list in flask memory
            rooms.append(channel)
            # create the list for the channel in messages dict
            messages[channel] = []
        print(rooms)
        return redirect(url_for('channels'))


@app.route('/channels')
def channels():
    number = len(rooms)
    if "name" in session:
        name = session["name"]
        return render_template("channels.html", channels=rooms, name=name, number=number)
    return render_template("channels.html", channels=rooms, number=number)


@app.route('/drop_session')
def drop_session():
    if "last_channel" in session:
        session.pop("last_channel")
    return redirect('/')

@app.route('/chat/<channel>')
def chat(channel):
    # save the channel to get the user back to that channel after closing the browser window
    session["last_channel"] = channel
    # check if there are no more than 100 messages in dict
    if len(messages[channel]) > 100:
        end = len(messages[channel]) - 100
        del messages[channel][0:end]

    return render_template("chat.html", messages_channel=messages[channel], channel=channel)

@socketio.on('join_channel')
def join_channel(join_channel):
    join_room(join_channel)

@socketio.on('send message')
def send_message(data):
    room = data["room"]
    join_room(room)
    name = data["name"]
    date = data["date"]
    message = data["message"]
    whole_message = date + ' ' + name + ': ' + message
    # save a message into messages dict in flask memory
    messages[room].append(whole_message)
    
    emit('display', whole_message, room=room)

@socketio.on('leave_channel')
def leave_channel(channel):
    # remove the last channel from session
    session.pop("last_channel")
    leave_room(channel)
    print(f"leaved channel: {channel}")


if __name__ == '__main__':
    socketio.run(app, debug=True)