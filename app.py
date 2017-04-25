
from gtts import gTTS
from flask import Flask, send_file
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
import os, flask, flask_socketio 
import time
import random


app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

#messageList = []
music_dir = '/home/ubuntu/workspace/CST-205-Project3/templates/media/'
global mediaLink

@socketio.on('connect')
def on_connect():
 print 'Someone connected!'

@socketio.on("newMessage")
def handle_message(messageData):
    passedContents = messageData
    messageList = []
    filename = random.randint(1,101)
    tts = gTTS(text=passedContents, lang='en')
    tts.save("templates/media/"+str(filename)+".mp3")
    mediaLink  = "/media/"+str(filename)+".mp3"
    messageList.append({
        'message' :passedContents,
        'socket'  : request.sid,
        'mediaLink' : mediaLink
        })
    socketio.emit('passedMessageList', messageList )
    print messageList
    song(filename+".mp3")
    def song(files):
        name = files
        print name
        return send_file(
            music_dir+"/"+name, 
            mimetype="audio/mp3", 
            as_attachment=True, 
            attachment_filename=name)

 

@app.route("/")
def index():
   music_files = [f for f in os.listdir(music_dir) if f.endswith('mp3')]
   music_files_number = len(music_files)
   return render_template("index.html")
@app.route('/media/<filename>')
def song(filename):
    name = filename
    print name
    return send_file(
         music_dir+"/"+name, 
         mimetype="audio/mp3", 
         as_attachment=True, 
         attachment_filename=name)

    #return render_template('play.html',
                      #  title = filename,
                      #  music_file = filename)

socketio.run(
 app,
 host=os.getenv('IP', '0.0.0.0'),
 port=int(os.getenv('PORT', 8080)),
 debug=True
)
