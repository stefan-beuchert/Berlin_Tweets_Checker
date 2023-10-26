import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# nltk.download('vader_lexicon')


def get_sentiments(data):
    sentiment_scores = []

    for tweet in data['Pre_Processed']:
        score = SentimentIntensityAnalyzer().polarity_scores(tweet)
        neg = score['neg']
        pos = score['pos']

        if pos > neg:
            sentiment_score = 1
        elif pos < neg:
            sentiment_score = -1
        else:
            sentiment_score = 0

        sentiment_scores.append(sentiment_score)

    data['Sentiment Score'] = sentiment_scores

    return data


def aggregate_sentiments_for_visualization(data):
    # ensure that datetime data is in datetime format
    data['Datetime'] = pd.to_datetime(data['Datetime'])

    # group by year, month and district
    data['Year'] = data['Datetime'].dt.year
    data['Month'] = data['Datetime'].dt.month
    data['Week'] = data['Datetime'].dt.isocalendar().week

    df_for_vis_month = data.groupby([data['Year'], data['Month'], data['District']]).mean()
    df_for_vis_month = df_for_vis_month.reset_index()

    df_for_vis_week = data.groupby([data['Year'], data['Week'], data['District']]).mean()
    df_for_vis_week = df_for_vis_week.reset_index()

    total_sentiment_over_time = get_total_sentiment_over_time(data)

    return df_for_vis_month, df_for_vis_week, total_sentiment_over_time


def get_total_sentiment_over_time(data):
    df_for_vis_total_sentiment_per_week = data.groupby([data['Year'], data['Week']]).mean()
    df_for_vis_total_sentiment_per_week = df_for_vis_total_sentiment_per_week.reset_index()

    return df_for_vis_total_sentiment_per_week

