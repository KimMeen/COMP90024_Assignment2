from twython import Twython
import twitter_config as config
from Server import Db
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from tweepy import Stream
import LocationService
from textblob import TextBlob

twitter = Twython(config.APP_KEY, config.APP_SECRET)
auth = twitter.get_authentication_tokens()
twitter = Twython(config.APP_KEY, config.APP_SECRET,
                  config.OAUTH_TOKEN, config.OAUTH_TOKEN_SECRET)
consumer_key = 'RAzA2C6n5DAEaAtoHOJqNcmZh'
consumer_secret = 'gvJopH2esd7WOcHtelQ9QwnHXAaVOyTMonh6zObEbIUrOeB8UK'
access_token = '1104975269633253377-TvFZL6UAJLYtRJdQaK4enQVFTuEOvS'
access_secret = 'simP9EhMSDuJ7G7d6FMttgqZKvwb47axZ6cmtlsuFYp6a'

db = Db("comp90024")
from twython import TwythonStreamer
import MapRegion
class listener(StreamListener):

    def on_data(self, streamData):
        global count
        data = json.loads(streamData)
        processed = {}
        processed['created_at'] = data['created_at']
        processed['text'] = data['text']
        processed['location'] = data['user']['location']
        processed['coordinates'] = LocationService.addressToCoordinate(processed['location'])
        processed['label'] = 0
        processed['region'] = MapRegion.getCoordinateRegion(processed['coordinates'])
        t = TextBlob(data['text'])
        processed['sentiment'] = t.sentiment.polarity
        print(processed)
        db.writeDoc2DB(processed)

    def on_error(self, status):
        print(status)

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data and 'coordinates' in data and 'user' in data and 'created_at' in data:
            if not data['coordinates'] is None:
                print(data['coordinates'])
    def on_error(self, status_code, data):
        print(status_code)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(locations=[112.921114, -43.740482, 159.109219, -9.142176])