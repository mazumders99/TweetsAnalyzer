import tweepy
from tweepy.auth import OAuthHandler
import configparser
import pandas
import Topic_Recognition
import nltk
import spacy
from nltk.tokenize import word_tokenize
from collections import Counter
import plotly.express as px

from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import numpy as np

# nltk.download('averaged_perceptron_tagger')
nlp = spacy.load("en_core_web_sm")

# read configs
config = configparser.ConfigParser()
config.read('config.ini')

# api_key = config['twitter']['api_key']
# api_key_secret = config['twitter']['api_key_secret']

# access_token = config['twitter']['access_token']
# access_token_secret = config['twitter']['access_token_secret']

api_key = 'Y3yzEbnsMden7DyTqf0Bj2E5y'
api_key_secret = 'wZco61qaKLdswPQhnCpUCcU8IdybEtu3M2mx84ANpRxmer4VQg'

access_token = '1461974155570475014-HpoRPOlZfxBsaHSoTm4MctNOndI2f5'
access_token_secret = 'qcqgdLdyiG0r4AOR3IlPBHgfBjK1ymE3JHWSqBrBTF4Kw'

# authentication
auth = OAuthHandler(api_key, api_key_secret)
# auth = tweepy.OAuth1UserHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

columns = ['Retweets', 'Likes', 'Tweet']


def tweets_analysis(user, no_of_tweets):
    data = []

    tweets = api.user_timeline(screen_name=user,
                               # 200 is the maximum allowed count
                               count=no_of_tweets,
                               include_rts=False,
                               exclude_replies=True,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               tweet_mode='extended'
                               )
    common_words_tracker = []

    for info in tweets:
        #data.append([info.retweet_count, info.favorite_count, info.full_text])
        # print(info.retweet_count)
        # print(info.favorite_count)
        # print(info.created_at)
        # print(info.full_text)
        # print("\n")

        common_words = Topic_Recognition.find_common_words(info.full_text)
        for i in common_words:
            text = i

            # returns a document of object
            doc = nlp(text)

            # checking if it is a noun or not
            if (doc[0].tag_ == 'NNP'):
                if not (text == 'http'):
                    common_words_tracker.append(text)
        # print(common_words)

    # print(common_words_tracker)

    lemmatizer = WordNetLemmatizer()

    common_words_list = Counter([lemmatizer.lemmatize(t)
                                for t in common_words_tracker])
    print(common_words_list.most_common(6))
    return common_words_list

    # df = pandas.DataFrame(data, columns=columns)
    # df.to_csv('tweets.csv', encoding='utf-8-sig')


# tweets_analysis()
def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha='center',
                 bbox=dict(facecolor='red', alpha=.8))


def plot_graph(user, no_of_tweets):
    x_coord = ['topics']
    y_coord = ['mentions']
    for i in tweets_analysis(user, no_of_tweets).most_common(6):
        x_coord.append(i[0])
        y_coord.append(i[1])

    # plt.figure(figsize=(10, 5))
    # #plt.plot(x_coord, y_coord)
    # plt.bar(x_coord, y_coord)
    # addlabels(x_coord, y_coord)
    # plt.title(f'Most frequently tweeted words of user {user}')
    # plt.xlabel('Tweet topic')
    # plt.ylabel('No of times tweeted')
    # plt.xticks(rotation=-90)
    # plt.show()

    # fig = px.bar(x=x_coord,
    #              y=y_coord, color_discrete_sequence=['white'])
    # fig.write_html('graph.html')

    # plt.savefig('data.jpeg')
    print(f'x_coord: {x_coord}, y_coord: {y_coord}')
    return x_coord, y_coord


# plot_graph('brfootball', 20)
