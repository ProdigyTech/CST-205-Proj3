
from gtts import gTTS
from flask import Flask, send_file
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
import os, flask, flask_socketio 
import time


app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

messageList = [];
music_dir = '/home/ubuntu/workspace/CST-205-Project3/templates/media/'


@socketio.on('connect')
def on_connect():
 print 'Someone connected!'

@socketio.on("newMessage")
def handle_message(messageData):
    passedContents = messageData
    tts = gTTS(text=passedContents, lang='en')
    tts.save("templates/media/sentMessage.mp3")
    mediaLink  = "/media/sentMessage.mp3"
    messageList.append({
        'message' :passedContents,
        'socket'  : request.sid,
        'mediaLink' : mediaLink
        })
    socketio.emit('passedMessageList', messageList )
    print messageList
 

@app.route("/")
def index():
   music_files = [f for f in os.listdir(music_dir) if f.endswith('mp3')]
   music_files_number = len(music_files)
   return render_template("index.html",
                        title = 'Home',
                        music_files_number = music_files_number,
                        music_files = music_files)
@app.route('/media/<filename>')
def song(filename):
    name = filename
    return send_file(
         music_dir, 
         mimetype="audio/mp3", 
         as_attachment=True, 
         attachment_filename="filename")

    #return render_template('play.html',
                      #  title = filename,
                      #  music_file = filename)

socketio.run(
 app,
 host=os.getenv('IP', '0.0.0.0'),
 port=int(os.getenv('PORT', 8080)),
 debug=True
)
