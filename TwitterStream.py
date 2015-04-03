import tweepy
from TwitterConnection import TwitterAuthentication
from tweepy import Stream
from tweepy.streaming import StreamListener

class TweetListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

ckey = "HM6VFab52fMzCqkxwKoF8cqRt"
csecret = "JaxQ7zkNRLf0qQjisEamW6lj1O7wc5Nv8k8rmdEnmBLA5E26m2"
atoken = "242248419-E8aEN7i8UB7BvTZxtdCxwzgSLzfO3aOKppeKCVlP"
asecret = "AtaUjKrNschURDr7b6L8YsWioCZo3bB4tt8V4LnBk4DiO"

auth = TwitterAuthentication(ckey, csecret, atoken, asecret)
auth = auth.getAuthHandler()

twitterStream = Stream(auth, TweetListener())
twitterStream.filter(track=["car"])
