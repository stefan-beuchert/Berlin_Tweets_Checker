import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import src.helper as helper


def create_interactive_map():
    # get topics
    topics = helper.load_data_from_json('data/topics.json')


    # first load resources
    plz_shape_df = gpd.read_file('./data/geo/plz-gebiete.shp', dtype={'plz': str})
    plz_region_df = pd.read_csv(
        './data/geo/zuordnung_plz_ort.csv',
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

    berlin_neighbourhoods_df = gpd.read_file('./data/geo/neighbourhoods.geojson')

    berlin_neighbourhoods_df = berlin_neighbourhoods_df \
        [~ berlin_neighbourhoods_df['neighbourhood_group'].isnull()]

    berlin_neighbourhoods_df = berlin_neighbourhoods_df[['neighbourhood_group', 'geometry']]

    berlin_neighbourhoods_df = berlin_neighbourhoods_df.dissolve(by='neighbourhood_group')

    berlin_neighbourhoods_df['+t1'] = ''
    berlin_neighbourhoods_df['+t2'] = ''
    berlin_neighbourhoods_df['+t3'] = ''
    berlin_neighbourhoods_df['+coherence'] = ''

    berlin_neighbourhoods_df['-t1'] = ''
    berlin_neighbourhoods_df['-t2'] = ''
    berlin_neighbourhoods_df['-t3'] = ''
    berlin_neighbourhoods_df['-coherence'] = ''

    berlin_neighbourhoods_df = berlin_neighbourhoods_df.reset_index()

    for district in topics:
        if len(topics[district]['positive topics']) > 0:
            berlin_neighbourhoods_df.loc[berlin_neighbourhoods_df['neighbourhood_group'] == district, '+coherence'] \
                = topics[district]['coherence pos']
            berlin_neighbourhoods_df.loc[berlin_neighbourhoods_df['neighbourhood_group'] == district, '+t1'] \
                = topics[district]['positive topics'][0]
            if len(topics[district]['positive topics']) > 1:
                berlin_neighbourhoods_df.loc[berlin_neighbourhoods_df['neighbourhood_group'] == district, '+t2'] \
                    = topics[district]['positive topics'][1]
                if len(topics[district]['positive topics']) > 2:
                    berlin_neighbourhoods_df.loc[berlin_neighbourhoods_df['neighbourhood_group'] == district, '+t3'] \
                        = topics[district]['positive topics'][2]

        if len(topics[district]['negative topics']) > 0:
            berlin_neighbourhoods_df.loc[berlin_neighbourhoods_df['neighbourhood_group'] == district, '-coherence'] \
                = topics[district]['coherence neg']
            berlin_neighbourhoods_df.loc[berlin_neighbourhoods_df['neighbourhood_group'] == district, '-t1'] \
                = topics[district]['negative topics'][0]
            if len(topics[district]['negative topics']) > 1:
                berlin_neighbourhoods_df.loc[berlin_neighbourhoods_df['neighbourhood_group'] == district, '-t2'] \
                    = topics[district]['negative topics'][1]
                if len(topics[district]['negative topics']) > 2:
                    berlin_neighbourhoods_df.loc[berlin_neighbourhoods_df['neighbourhood_group'] == district, '-t3'] \
                        = topics[district]['negative topics'][2]

    print(berlin_neighbourhoods_df.head())

    m = berlin_neighbourhoods_df.explore(cmap='Paired',
                                         legend=True)

    m.save('resources for präsi/interactive_topic_map.html')

    print("saved")


def visualize_total_sentiment_per_week(data):
    ax = plt.gca()
    plot = data.plot(kind='line', x='Week', y='Sentiment Score', ax=ax)
    plot.axhline(y=0, color='gray', linestyle='--')
    fig = plot.get_figure()

    fig.savefig(f'./resources for präsi/overview.png')
    plt.close(fig)


def visualize_sentiment_maps_month(data):
    # first load resources
    plz_shape_df = gpd.read_file('./data/geo/plz-gebiete.shp', dtype={'plz': str})
    plz_region_df = pd.read_csv(
        './data/geo/zuordnung_plz_ort.csv',
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

    berlin_neighbourhoods_df = gpd.read_file('./data/geo/neighbourhoods.geojson')

    berlin_neighbourhoods_df = berlin_neighbourhoods_df \
        [~ berlin_neighbourhoods_df['neighbourhood_group'].isnull()]

    # for each frame of final image/gif
    for year in data['Year'].unique():
        for month in data['Month'].unique():
            df_for_year_and_month = data[(data['Year'] == year) & (data['Month'] == month)]
            df_for_year_and_month = df_for_year_and_month[['District', 'Sentiment Score']]

            create_and_safe_plot_month(df_for_year_and_month, year, month, berlin_df, berlin_neighbourhoods_df)


def create_and_safe_plot_month(df_for_year_and_month, year, month, berlin_df, berlin_neighbourhoods_df):
    # prepare canvas
    plt.style.use('seaborn')

    fig, ax = plt.subplots()

    berlin_df.plot(
        ax=ax,
        alpha=0.2
    )

    berlin_neighbourhoods_df_with_colors = berlin_neighbourhoods_df.merge(
        df_for_year_and_month,
        left_on='neighbourhood_group',
        right_on='District')

    berlin_neighbourhoods_df_with_colors.plot(
        ax=ax,
        column='Sentiment Score',
        categorical=True,
        legend=False,
        #legend_kwds={'title': 'Districts', 'loc': 'upper right'},
        cmap=LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256),
        edgecolor='black',
        # color='red'
    )

    ax.set(
        title=f"Berlin Sentiment {month}-{year}",
        aspect=1.3
    )

    plt.savefig(f'./visualizations/sentiment_maps/per_month/{year}_{month}.png')
    plt.close(fig)


def visualize_sentiment_maps_week(data):
    # first load resources
    plz_shape_df = gpd.read_file('./data/geo/plz-gebiete.shp', dtype={'plz': str})
    plz_region_df = pd.read_csv(
        './data/geo/zuordnung_plz_ort.csv',
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

    berlin_neighbourhoods_df = gpd.read_file('./data/geo/neighbourhoods.geojson')

    berlin_neighbourhoods_df = berlin_neighbourhoods_df \
        [~ berlin_neighbourhoods_df['neighbourhood_group'].isnull()]

    # for each frame of final image/gif
    for year in data['Year'].unique():
        for week in data['Week'].unique():
            df_for_year_and_week = data[(data['Year'] == year) & (data['Week'] == week)]
            df_for_year_and_week = df_for_year_and_week[['District', 'Sentiment Score']]

            create_and_safe_plot_week(df_for_year_and_week, year, week, berlin_df, berlin_neighbourhoods_df)


def create_and_safe_plot_week(df_for_year_and_month, year, week, berlin_df, berlin_neighbourhoods_df):
    # prepare canvas
    plt.style.use('seaborn')

    fig, ax = plt.subplots()

    berlin_df.plot(
        ax=ax,
        alpha=0.2
    )

    berlin_neighbourhoods_df_with_colors = berlin_neighbourhoods_df.merge(
        df_for_year_and_month,
        left_on='neighbourhood_group',
        right_on='District')

    berlin_neighbourhoods_df_with_colors.plot(
        ax=ax,
        column='Sentiment Score',
        categorical=True,
        legend=False,
        #legend_kwds={'title': 'Districts', 'loc': 'upper right'},
        cmap=LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256),
        edgecolor='black',
        # color='red'
    )

    ax.set(
        title=f"Berlin Sentiment {week}-{year}",
        aspect=1.3
    )

    plt.savefig(f'./visualizations/sentiment_maps/per_week/{year}_{week}.png')
    plt.close(fig)
