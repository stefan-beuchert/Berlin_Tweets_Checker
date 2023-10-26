import nltk
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

from src.helper import load_data
from preprocessing import pre_process_tweets

nltk.download('vader_lexicon')

def get_sentiment_scores(tweets):
    sentiment_scores = []

    for tweet in tweets:
        analysis = TextBlob(tweet)
        score = SentimentIntensityAnalyzer().polarity_scores(tweet)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        polarity = analysis.sentiment.polarity

        sentiment_score = None

        if pos > neg:
            sentiment_score = 1
        elif pos < neg:
            sentiment_score = -1
        else:
            sentiment_score = 0

        # print("neg " + str(neg))
        # print("neu " + str(neu))
        # print("pos " + str(pos))
        # print("comp " + str(comp))
        # print("pol " + str(polarity))

        sentiment_scores.append(sentiment_score)

    return sentiment_scores


# get data
data = load_data('../data/data_backup.csv')

# preprocess data
tweet_preprocessed, hashtags = pre_process_tweets(data['text'])
data['processed'] = tweet_preprocessed
data['hashtags'] = hashtags

# get sentiments
data['sentiments'] = get_sentiment_scores(data['text'])

a = data[['city_district', 'sentiments']].groupby('city_district').mean()
print(a)

plt.xticks(rotation='vertical')
plt.bar(a.index, height=a.sentiments)
plt.title('distribution of districts')

plt.tight_layout()
plt.savefig('../visualizations/sentiment_per_district.png')
print(a.head(30))

print("jim")
