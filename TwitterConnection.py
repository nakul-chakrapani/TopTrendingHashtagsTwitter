from tweepy import OAuthHandler

class TwitterAuthentication:
    consumerKey = ''
    consumerSecret = ''
    authToken = ''
    authSecret = ''

    def __init__(self, ckey, csecret, atoken, asecret):
        self.consumerKey = ckey
        self.consumerSecret = csecret
        self.authToken = atoken
        self.authSecret = asecret

    def getAuthHandler(self):
        auth = OAuthHandler(self.consumerKey, self.consumerSecret)
        auth.set_access_token(self.authToken, self.authSecret)
        return auth
