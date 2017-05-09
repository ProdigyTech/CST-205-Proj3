import tweepy

###### TWITTER API #############################################
consumer_key= "7EadEmQhNj4j6RY82f2HxhI2n" 
consumer_secret= "1eZhg5WNEO8Jt09E9dWy9Mo6f9Mriz83utvx8tb5lXJMwserkC" 
access_token = "1518510956-gU73yOwXZf20D2whzQ7CVIuGxObIQkEhSa6yD5j" 
access_token_secret = "WyvCoPFt0HwYLjqiUkvBHz4RA67vmyOKBbwI0vhD11LsJ" 

#Logging into twitter using the tweetpy wrapper
auth = tweepy.OAuthHandler(consumer_key,  consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweet = "Another test using a string"

# api.update_status(tweet)
