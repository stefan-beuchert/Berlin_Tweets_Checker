import snscrape.modules.twitter as sntwitter
import pandas as pd

import src.helper as helper


def fetch(data_points_per_district=1000):
    districts = helper.load_data_from_json('./data/12_districts_berlin.json')

    # for each district
    for district_label in districts:

        # get data
        tweets_per_district = get_tweets_for_district(district_label, districts[district_label], data_points_per_district)

        # save data
        helper.save_data_to_csv(tweets_per_district, f'./data/tweets_per_district/{district_label}.csv')


def get_tweets_for_district(district, list_of_sub_districts, data_points_per_district):
    number_of_sub_districts = len(list_of_sub_districts)
    number_of_data_points_per_district = int(data_points_per_district / number_of_sub_districts)

    tweets = []
    for sub_district in list_of_sub_districts:
        tweets_per_sub_district = get_tweets_for_sub_district(district, sub_district, number_of_data_points_per_district)
        tweets.extend(tweets_per_sub_district)

    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(tweets, columns=['Datetime',
                                              'Tweet Id',
                                              'Text',
                                              'Username',
                                              'Language',
                                              'District',
                                              'Sub District',
                                              'Up Votes'])

    return tweets_df


def get_tweets_for_sub_district(district_name, sub_district_name, number_of_data_points):
    # Creating list to append tweet data to
    tweets = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(f'{sub_district_name} and Berlin '
                                           'since:2021-01-01 until:2021-12-31 '
                                           'lang:en').get_items()):
        if len(tweets) >= number_of_data_points:
            break

        if (tweet.retweetedTweet is None
                and tweet.quotedTweet is None
                and tweet.outlinks is None
        ):
            tweets.append([tweet.date,
                           tweet.id,
                           tweet.content,
                           tweet.user.username,
                           tweet.lang,
                           district_name,
                           sub_district_name,
                           tweet.likeCount])

    return tweets


def aggregate():
    districts = helper.load_data_from_json('./data/12_districts_berlin.json')

    data = None

    for district_label in districts:
        district_data = helper.load_data_from_csv(f'./data/tweets_per_district/{district_label}.csv')

        district_data['District'] = helper.translate_district(district_label)

        if data is None:
            data = district_data
        else:
            data = data.append(district_data)

    return data


