from gtts import gTTS
from flask import Flask, send_file, make_response
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
import os, flask, flask_socketio 
import time
from chatterbot import ChatBot
from settings import TWITTER

#responses = ["hello", "hi", "Who did you vote for?", "TRUMP 2016", "Who did it?", "The russians!", "MAGA", "MAKE AMERICA GREAT AGAIN", "TRUMPs favroite chat", "Build that wall", "what is your name", "Jason", "Do you feel love?", "I'm a robot you idiot"]

#chatbot = ChatBot(
  # 'Ron Obvious',
   # trainer='chatterbot.trainers.ListTrainer'
#)

#Train based on the english corpus
#chatbot.train(responses)


chatbot = ChatBot("TwitterBot",
    logic_adapters=[
        "chatterbot.logic.BestMatch"
    ],
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter",
    database="./twitter-database.db",
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"],
    trainer="chatterbot.trainers.TwitterTrainer"
)

print("Starting the twitter training")
chatbot.train()
print("Finished training")

chatbot.logger.info('Trained database generated successfully!')

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

messageList = [];
music_dir = os.getcwd() + '/templates/media/'

@socketio.on('connect')
def on_connect():
 print 'Someone connected!'

@socketio.on("newMessage")
def handle_message(messageData):
    passedContents = messageData
    tts = gTTS(text=str(chatbot.get_response(passedContents)), lang='en')
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
    response = make_response(send_file(
         music_dir + filename, 
         mimetype="audio/mp3", 
         as_attachment=True, 
         attachment_filename="filename"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

    #return render_template('play.html',
                      #  title = filename,
                      #  music_file = filename)

socketio.run(
 app,
 host=os.getenv('IP', '0.0.0.0'),
 port=int(os.getenv('PORT', 8080)),
 debug=True
)