import tweepy

###### TWITTER API #############################################

def sendTweet(tweetData):
    
    consumer_key= "EuvpBtbfkdpycmVxR14gH7mph" 
    consumer_secret= "jr8t52Xof1bliEQIFD5MUe1qK2eYEnBOrG7T5QReanW125KgAs" 
    access_token = "862722342501232640-E1p1EwoAOxZlgbRGWCUELKmgkrQpvLx" 
    access_token_secret = "LrvxY0HLqsxsYNvpUUi8kyEk0xMkjPgQz6lrO0TEz5AMC" 
    #Logging into twitter using the tweetpy wrapper
    auth = tweepy.OAuthHandler(consumer_key,  consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(tweetData)
