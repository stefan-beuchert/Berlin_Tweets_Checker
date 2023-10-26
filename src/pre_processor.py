import re
import nltk

import src.helper as helper


def process(data):
    tweets = data['Text']
    stop_words = helper.get_stopwords()

    pre_processed_tweets = []

    for tweet in tweets:
        pre_processed_tweet = clean_tweet(tweet, stop_words)
        pre_processed_tweets.append(pre_processed_tweet)

    data['Pre_Processed'] = pre_processed_tweets

    return data


def clean_tweet(tweet, stop_words):
    # text to lower
    tweet = tweet.lower()

    # remove users
    tweet = re.sub('@[^\s]+', '', tweet)

    # remove links
    tweet = re.sub(r'https?://[A-Za-z0-9./]+', '', tweet)

    # remove numbers
    tweet = re.sub(r'\d+', '', tweet)

    tweet = tokenize_tweet(tweet)

    # remove words < 2
    tweet = [token for token in tweet if 2 <= len(token)]

    # remove stopwords
    tweet = [token for token in tweet if token not in stop_words]

    tweet = ' '.join(tweet)

    return tweet


def tokenize_tweet(tweet):
    # remove special characters and turn text to tokens
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    return tokenizer.tokenize(tweet)


def tokenize_tweets(tweets):
    res = []
    for tweet in tweets:
        tokenized_tweet = tokenize_tweet(tweet)
        res.append(tokenized_tweet)

    return res
