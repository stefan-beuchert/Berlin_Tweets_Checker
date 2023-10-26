import pandas as pd
import geopandas as gpd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from descartes.patch import PolygonPatch

from preprocessing import pre_process_tweets


def basic_tweet_per_district_distribution(data):
    data_aggregated = data[['city_district']].groupby('city_district').size().reset_index(name='counts')

    plt.xticks(rotation='vertical')
    plt.bar(data_aggregated.city_district, height=data_aggregated.counts)
    plt.title('distribution of districts')

    plt.tight_layout()
    plt.savefig('../visualizations/distribution_of_districts.png')


def create_wordcloud(data):
    all_tweets = " ".join(data['processed'])

    wordcloud = WordCloud(width=1600, height=800, background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
    wordcloud.generate(all_tweets)
    plt.figure(figsize=(160, 90))

    wordcloud.to_file('../visualizations/word_cloud.png')


def berlin_districts():
    plt.style.use('seaborn')

    plz_shape_df = gpd.read_file('../data/geo/plz-gebiete.shp', dtype={'plz': str})

    plz_region_df = pd.read_csv(
        '../data/geo/zuordnung_plz_ort.csv',
        sep=',',
        dtype={'plz': str}
    )

    plz_region_df.drop('osm_id', axis=1, inplace=True)

    germany_df = pd.merge(
        left=plz_shape_df,
        right=plz_region_df,
        on='plz',
        how='inner'
    )

    germany_df.drop(['note'], axis=1, inplace=True)

    berlin_df = germany_df.query('ort == "Berlin"')

    berlin_neighbourhoods_df = gpd.read_file('../data/geo/neighbourhoods.geojson')

    berlin_neighbourhoods_df = berlin_neighbourhoods_df \
        [~ berlin_neighbourhoods_df['neighbourhood_group'].isnull()]

    print(berlin_neighbourhoods_df.head())
    print(berlin_neighbourhoods_df['neighbourhood_group'].head())

    fig, ax = plt.subplots()

    berlin_df.plot(
        ax=ax,
        alpha=0.2
    )

    berlin_neighbourhoods_df.plot(
        ax=ax,
        column='neighbourhood_group',
        categorical=True,
        legend=True,
        legend_kwds={'title': 'Districts', 'loc': 'upper right'},
        cmap='tab20',
        edgecolor='black'
    )

    ax.set(
        title='Berlin Districts',
        aspect=1.3
    )

    plt.savefig('../visualizations/berlin_districts.png')


def load_data(path):
    df = pd.read_csv(path)
    return df


# get data
data = load_data('../data/data_backup.csv')
data['processed'], _ = pre_process_tweets(data['text'], False)

# basic_tweet_per_district_distribution(data)
create_wordcloud(data)
berlin_districts()
