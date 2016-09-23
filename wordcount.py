import json

import tweepy
from matplotlib import animation
from nltk.tokenize import TweetTokenizer

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

hashtable = {}


class TweetListener(tweepy.StreamListener):
    def __init__(self):
        super(TweetListener, self).__init__()
        self.tokenizer = TweetTokenizer()
        # self.hashtable = {}

    def on_connect(self):
        print('Successfully connected to the twitter stream !')

    def on_disconnect(self, notice):
        print('Disconnected from current twitter stream !')

    def on_data(self, raw_data):
        try:
            tweet = json.loads(raw_data)
            text = tweet["text"].lower()
            text_tkn = self.tokenizer.tokenize(text)
            for word in text_tkn:
                if word in hashtable:
                    hashtable[word] += 1
                else:
                    hashtable[word] = 1
                    # plt.bar(hashtable.keys(), hashtable.values(), 5, color='g')
                    # plt.show()
        except KeyError:
            print(KeyError.message)

    def on_status(self, status):
        print(status)

    def on_error(self, status_code):
        print('Error: %s', status_code)


auth = tweepy.OAuthHandler('key',
                           'secret')
auth.set_access_token('token',
                      'token-secret')

myTwitterListener = TweetListener()
myTwitterStream = tweepy.Stream(auth=auth, listener=myTwitterListener)

myTwitterStream.sample(async=True)


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                '%d' % int(height),
                ha='center', va='bottom')


def animate(frameno):
    words, frequency = zip(*hashtable)

    ind = np.arange(len(hashtable))  # the x locations for the groups
    width = 0.35  # the width of the bars

    rects1 = ax.bar(ind, frequency, width, color='r')

    ax.set_ylabel('Count')
    ax.set_xticks(ind + width / 2.)
    ax.set_xticklabels(words)

    autolabel(rects1)


fig, ax = plt.subplots()


ani = animation.FuncAnimation(fig, animate, blit=False, interval=100,
                              repeat=True)
plt.show()
