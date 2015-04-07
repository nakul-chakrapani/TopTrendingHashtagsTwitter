import tweepy
from TwitterConnection import TwitterAuthentication
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy.utils import import_simplejson
import operator
import sys
json = import_simplejson()

tweetCount = 0
hashTagsMapList = []
hashTagsMap = {}
trendingHashTags = {}
windowSize = 3              #Default window size
K = 10                      #Default K
numberOfTweets = 100

class TweetListener(StreamListener):

    def on_data(self, data):
        global tweetCount, hashTagsMapList, hashTagsMap
        data = json.loads(data)
        if 'entities' in data:
            if len(data['entities']['hashtags']) > 0:
                tweetCount += 1
                self.getHashtags(data)
                if tweetCount == numberOfTweets:
                    tweetCount = 0
                    hashTagsMapList.append(hashTagsMap)
                    self.getTrendingHashtags()
                    hashTagsMap = {}
        return True

    def on_error(self, status):
        print status

    def getHashtags(self, data):
        global hashTagsMap
        hashtagArray = []
        hashtags = data['entities']['hashtags']
        for hashtag in hashtags:
            hashtagText = hashtag['text']
            if hashtagText is None:
                continue
            if hashtagText in hashTagsMap:
                hashTagsMap[hashtagText] = hashTagsMap[hashtagText] + 1
            else:
                hashTagsMap[hashtagText] = 1

    def getTrendingHashtags(self):
        global trendingHashTags, hashTagsMapList
        if len(hashTagsMapList) > windowSize:
            mapToBeRemoved = hashTagsMapList[0]
            for key in mapToBeRemoved:
                if key in trendingHashTags:
                    value = trendingHashTags[key]
                    value = value - mapToBeRemoved[key]
                    if value == 0:
                        trendingHashTags.pop(key, None)
                    else:
                        trendingHashTags[key] = value

        recentlyAddedMap = hashTagsMapList[-1]
        for key in recentlyAddedMap:
            if key in trendingHashTags:
                trendingHashTags[key] = trendingHashTags[key] + recentlyAddedMap[key]
            else:
                trendingHashTags[key] = recentlyAddedMap[key]

        sorted_hashmap = sorted(trendingHashTags.items(), key=operator.itemgetter(1))
        for i in xrange(len(sorted_hashmap)-1, len(sorted_hashmap)-K-1,-1):
            print sorted_hashmap[i][0].encode('utf-8') + "\t&emsp;\t" + str(sorted_hashmap[i][1])


if __name__ == '__main__':
    ckey = sys.argv[1]
    csecret = sys.argv[2]
    atoken = sys.argv[3]
    asecret = sys.argv[4]
    windowSize = int(sys.argv[5])
    numberOfTweets = int(sys.argv[6])
    K = int(sys.argv[7])

    auth = TwitterAuthentication(ckey, csecret, atoken, asecret)
    auth = auth.getAuthHandler()
    twitterStream = Stream(auth, TweetListener())
    twitterStream.sample()
