import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import TextBlob
# nltk.download('stopwords')    #download if using this module for the first time


def find_common_words(tweet_text):

    text1 = TextBlob(tweet_text).noun_phrases

    tokens = word_tokenize(tweet_text)
    #tokens= text1
    lowercase_tokens = [t.lower() for t in tokens]
    # print(lowercase_tokens)

    # bagofwords_1 = Counter(lowercase_tokens)
    # print(bagofwords_1.most_common(10))

    alphabets = [t for t in lowercase_tokens if t.isalpha()]

    words = stopwords.words("english")
    stopwords_removed = [t for t in alphabets if t not in words]

    # print(stopwords_removed)

    lemmatizer = WordNetLemmatizer()

    lem_tokens = [lemmatizer.lemmatize(t) for t in stopwords_removed]

    bag_words = Counter(lem_tokens)
    # print(bag_words.most_common(6))

    common_words = []
    common_words_count = []

    for i in bag_words.most_common(6):
        common_words.append(i[0])
        common_words_count.append(i[1])
    #print(common_words, common_words_count)
    # if('madrid' in tweet_text.lower()):
    #     print(tweet_text)
    #     print("***************")
    return common_words
    # print(bag_words['salah'])
