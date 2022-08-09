
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
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import numpy as np
import urllib.request

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
# tweets_text = []
# # tweets_dict = defaultdict(list)
# tweets_dict = defaultdict(set)


def tweets_analysis(user, no_of_tweets):
    data = []
    tweets_text = []


#   tweets_dict = defaultdict(list)
    tweets_dict = defaultdict(set)

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
        topic_words_this_tweet = set()
        common_words = Topic_Recognition.find_common_words(info.full_text)
        # tweets_text.append(info.full_text)
        arr = []
        for i in common_words:
            text = i

            # returns a document of object
            doc = nlp(text)

            # checking if it is a noun or not
            if (doc[0].tag_ == 'NNP'):
                if not (text == 'http'):
                    common_words_tracker.append(text)
                    topic_words_this_tweet.add(text)
                    arr.append(text)

        for topic_word in topic_words_this_tweet:
            # tweets_dict[topic_word].append(info.full_text)
            tweets_dict[topic_word].add(info.full_text)

    lemmatizer = WordNetLemmatizer()
    # print(common_words_tracker)
    common_words_list = Counter([lemmatizer.lemmatize(t)
                                for t in common_words_tracker])
    x_coord = ['topics']
    y_coord = ['mentions']
    for i in common_words_list.most_common(6):
        x_coord.append(i[0])
        y_coord.append(i[1])

    # Profile pic stuff start

    # Profile pic stuff end

    return x_coord, y_coord, tweets_dict

    # df = pandas.DataFrame(data, columns=columns)
    # df.to_csv('tweets.csv', encoding='utf-8-sig')


# tweets_analysis()
def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha='center',
                 bbox=dict(facecolor='red', alpha=.8))


def download_image(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)
    return full_path


def get_profile_info(user):
    try:
        user_info_dict = {}
        user_info = api.get_user(screen_name=user)
        user_info_dict['followers_count'] = user_info.followers_count
        user_info_dict['name'] = user_info.name
        user_info_dict['screen_name'] = user_info.screen_name
        user_info_dict['statuses_count'] = user_info.statuses_count
        user_info_dict['following_count'] = user_info.friends_count
        profile_img_small_url = user_info.profile_image_url
        user_info_dict['profile_img_url'] = profile_img_small_url.replace(
            'normal', '400x400')

    except:
        return None

    # print(name)
    # print(screen_name)
    # print(followers_count)
    # print(following_count)
    # print(user_info.profile_image_url)
    # print(profile_img_url)
    # print(statuses_count)
    # print(user_info)
    # download_image(profile_img_url, 'static/img/', screen_name)
    return user_info_dict


print("***************************************************************************************************************************************")
print(get_profile_info('ackermanhisashi'))

# plot_graph('cr7raprhymes', 200)
