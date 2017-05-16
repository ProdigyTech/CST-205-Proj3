#Written by Maria L. File that allows us to send tweets to twitter from the chatbot. 

import tweepy

###### TWITTER API #############################################

consumer_key= "EuvpBtbfkdpycmVxR14gH7mph" 
consumer_secret= "jr8t52Xof1bliEQIFD5MUe1qK2eYEnBOrG7T5QReanW125KgAs" 
access_token = "862722342501232640-E1p1EwoAOxZlgbRGWCUELKmgkrQpvLx" 
access_token_secret = "LrvxY0HLqsxsYNvpUUi8kyEk0xMkjPgQz6lrO0TEz5AMC" 
#Logging into twitter using the tweetpy wrapper
auth = tweepy.OAuthHandler(consumer_key,  consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def sendTweet(tweetData):
    api.update_status(tweetData)
    
    
def getRecentTweetLink():
    me = api.me()
    # print me.screen_name
    # print me.screenname
    # print me.id
    
    tweet = api.user_timeline(id=me.id, count = 1)[0]
    # print tweet
    # print tweet.id
    # print str(tweet.id)
    url = "https://twitter.com/" + me.screen_name + "/status/" + str(tweet.id)
    # print url
    return url
    
    # https://twitter.com/CST_205_BOT/status/862739416686743553