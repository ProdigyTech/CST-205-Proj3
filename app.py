from gtts import gTTS
from flask import Flask, send_file, make_response
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
import os, flask, flask_socketio 
import time
from chatterbot import ChatBot
from settings import TWITTER
from chatterbot.trainers import ListTrainer
import twitterPost
from listReader import generateTrainingLists

chatbot = ChatBot(
   'CST Bot',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.50,
            'default_response': 'I dont know, I dumb. :('
        }
    ],
    trainer='chatterbot.trainers.ListTrainer',
    read_only=True,
)
chatbot.train("chatterbot.corpus.english.conversations")
chatbot.train("chatterbot.corpus.english.greetings")

chatbot.set_trainer(ListTrainer)

# Training from a file
for li in generateTrainingLists("exTraining.txt"):
    chatbot.train(li)


def initMessage():
   tts = gTTS(text=str("Hello, I am pie-Bot! Talk to me, make me smater. I can send tweets to twitter, to start type the word tweet and then what you want me to say"), lang='en')
   tts.save("templates/media/sentMessage.mp3")
   mediaLink  = "/media/sentMessage.mp3"
   messageList.append({
       'message' :"I can send tweets to twitter, to start type the word tweet and then what you want me to say",
       'socket'  : 0000,
       'mediaLink' : mediaLink
       })
   socketio.emit('passedMessageList', messageList )


app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

messageList = [];
music_dir = os.getcwd() + '/templates/media/'
# initMessage()
@socketio.on('connect')
def on_connect():
 print 'Someone connected!'

@socketio.on("newMessage")
def handle_message(messageData):
    passedContents = messageData
    if ('tweet' in passedContents):
        tweetToSend =  passedContents[6:]
        tts = gTTS(text=str("Tweet sent to twitter, check it out"), lang='en')
        respMsg = str(chatbot.get_response(passedContents[5:]))
        tweetToSend = "Q:" + passedContents[5:] + "\nR:" + respMsg
        tts = gTTS(text=str(respMsg), lang='en')
        tts.save("templates/media/sentMessage.mp3")
        mediaLink  = "/media/sentMessage.mp3"
        
        twitterPost.sendTweet(tweetToSend)
        messageList.append({
            'message' :passedContents,
            'socket'  : request.sid,
            'mediaLink' : mediaLink,
            'twitterLink': twitterPost.getRecentTweetLink()
            })
        socketio.emit('passedMessageList', messageList )
        print "TEST"
        print messageList
    else:
     tts = gTTS(text=str(chatbot.get_response(passedContents)), lang='en')
     tts.save("templates/media/sentMessage.mp3")
     mediaLink  = "/media/sentMessage.mp3"
     messageList.append({
         'message' :passedContents,
         'socket'  : request.sid,
         'mediaLink' : mediaLink,
         'twitterLink': ''
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

socketio.run(
 app,
 host=os.getenv('IP', '0.0.0.0'),
 port=int(os.getenv('PORT', 8080)),
 debug=True
)