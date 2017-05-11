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

#responses = ["hello", "hi", "Who did you vote for?", "TRUMP 2016", "Who did it?", "The russians!", "MAGA", "MAKE AMERICA GREAT AGAIN", "TRUMPs favroite chat", "Build that wall", "what is your name", "Jason", "Do you feel love?", "I'm a robot you idiot"]

chatbot = ChatBot(
   'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    read_only=True,
)
chatbot.train("chatterbot.corpus.english.conversations")
chatbot.train("chatterbot.corpus.english.conversations")
chatbot.train("chatterbot.corpus.english.greetings")

chatbot.set_trainer(ListTrainer)
chatbot.train("twitter_training.json")


chatbot.train([
    "How are you?",
    "I am good.",
    "That is good to hear.",
    "Thank you",
    "You are welcome.",
])

chatbot.train([
    "Do you feel love?",
    "I did until I had my heart broken",
    "Who broke your heart?.",
    "A botnet named Kris",
    "Sad"
    "It's ok,  I don't feel anymore.",
])
chatbot.train([
    "What is your name",
    "XJ9 BOT",
    "Who are your parents",
    "I only have one creator. His name is Javar",
    "Where were you born?",
     "I was born in Seaside CA, at California State University Monterey Bay",
     "When is your birthday?",
     "Sometime in May",
])

chatbot.train([
    "TRUMP",
    "You mean Satan?",
    "Trump is not satan",
    "Ok, he is the anti-christ",
    "that's not nice",
     "The anti christ isn't nice. so what's your point",
     "You're mean",
     "Yup",
])

chatbot.train({
 "Who is your favorite actor?",
 "I like Harrison Ford",
 "He's actually not a car, he is an actor.",
 "Are you sure that's true?",
 "Yes, I have seen him in lots of movies.",
 "fine then"
})

chatbot.train({
 "Do you think I'm fat?",
 "im glad youre fat"
})
chatbot.train({
 "Mean Girls",
 "Four for you Glen Coco, You GO Glen Coco!"
})

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

#Train based on the english corpus
#chatbot.train(responses)


#chatbot = ChatBot("TwitterBot",
 #   logic_adapters=[
  #      "chatterbot.logic.BestMatch"
   # ],
    #input_adapter="chatterbot.input.TerminalAdapter",
    #output_adapter="chatterbot.output.TerminalAdapter",
    #database="./twitter-database.db",
    #twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    #twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    #twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    #twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"],
    #trainer="chatterbot.trainers.TwitterTrainer"
#)

#print("Starting the twitter training")
#chatbot.train()
#print("Finished training")

#chatbot.logger.info('Trained database generated successfully!')

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

messageList = [];
music_dir = os.getcwd() + '/templates/media/'
initMessage()
@socketio.on('connect')
def on_connect():
 print 'Someone connected!'

@socketio.on("newMessage")
def handle_message(messageData):
    passedContents = messageData
    if ('tweet' in passedContents):
        tweetToSend =  passedContents[5:]
        tts = gTTS(text=str("Tweet sent to twitter, check it out"), lang='en')
        tts.save("templates/media/sentMessage.mp3")
        mediaLink  = "/media/sentMessage.mp3"
        messageList.append({
            'message' :passedContents,
            'socket'  : request.sid,
            'mediaLink' : mediaLink
            })
        twitterPost.sendTweet(tweetToSend)
        socketio.emit('passedMessageList', messageList )
        print messageList
    else:
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