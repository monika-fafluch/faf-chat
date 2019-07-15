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
rooms = []

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def home():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        # save user's name into session
        session["name"] = request.form.get("name")
        # ensure the channel's name isn't taken
        channel = request.form.get("create-channel")
        if channel in rooms:
            return render_template("index-error.html")
        # save the channel into rooms list in flask memory
        rooms.append(channel)
        # create the list for the channel in messages dict
        messages[channel] = []

        return redirect(url_for('channels'))


@app.route('/channels')
def channels():
    return render_template("channels.html", channels=rooms)


@app.route('/chat/<channel>')
def chat(channel):
        
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