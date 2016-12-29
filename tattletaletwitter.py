# See https://apps.twitter.com/app/13163627 for registered app

import twitter

import configparser
config = configparser.ConfigParser()
config.read('tattletale.conf')

twitterConsumerKey = config.get('twitter', 'consumerKey')
twitterConsumerSecret = config.get('twitter', 'consumerSecret')
twitterAccessToken = config.get('twitter', 'accessToken')
twitterAccessTokenSecret = config.get('twitter', 'accessTokenSecret')

# login to twitter
api = twitter.Api(consumer_key=twitterConsumerKey,
                  consumer_secret=twitterConsumerSecret,
                  access_token_key=twitterAccessToken,
                  access_token_secret=twitterAccessTokenSecret)

def tweet(msg: str):
    api.PostUpdate(msg)

#tweet('testing')
