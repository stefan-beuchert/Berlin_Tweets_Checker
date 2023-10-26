import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')


def pre_process_tweets(tweets, with_removal = False):
    res_tweets = []
    hashtags_per_tweet = []

    for tweet in tweets:
        # get hashtags
        hashtags = lambda x: re.findall(r"#(\w+)", tweet)

        # text to lower
        tweet = tweet.lower()

        # remove users
        tweet = re.sub('@[^\s]+', '', tweet)

        # remove numbers
        tweet = re.sub(r'\d+', '', tweet)

        if with_removal:
            # remove special characters and turn text to tokens
            tokenizer = nltk.RegexpTokenizer(r"\w+")
            tweet = tokenizer.tokenize(tweet)

            # remove words < 2
            tweet = [token for token in tweet if 2 <= len(token)]

            # remove stopwords
            stop_words = stopwords.words('english')
            stop_words.extend(['rt', 'berlin', 'charlottenburg', 'friedrichshain',
                               'hellersdorf', 'hohenschönhausen', 'kreuzberg', 'kreutzberg', 'Xberg',
                               'köpenick', 'lichtenberg', 'marzahn', 'mitte', 'neukölln', 'pankow', 'prenzlauer Berg',
                               'reinickendorf', 'schöneberg', 'spandau', 'steglitz', 'steglits', 'tempelhof', 'tiergarten',
                               'treptow', 'trepto', 'wedding', 'weißensee', 'weisensee', 'wilmersdorf', 'zehlendorf'])
            stop_words = set(stop_words)
            tweet = [token for token in tweet if token not in stop_words]

        res_tweets.append(tweet)
        hashtags_per_tweet.append(hashtags)

    return res_tweets, hashtags_per_tweet


test_tweets = [
    "@ciabaudo @jed_mercurio @BenMacintyre1 @FinancialTimes I don't know Kreuzberg that well, just for an article. I "
    "did go to Berlin 3 times in the 80's [when I lived in Munich-Innsbruck], modelling, but was too busy to poke "
    "around and my life was different, it was show biz, I was totally naive."]

a, _ = pre_process_tweets(test_tweets)

print(a)