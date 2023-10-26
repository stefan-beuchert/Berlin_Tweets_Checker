import requests
import json
import pandas as pd

bearer_token = "AAAAAAAAAAAAAAAAAAAAAPGyVwEAAAAAl47lZfgL%2Bb9oVYqaPlYeHAuOmPk%3DMwaa2nidrHcPOwW1X1dkzE6Cx1BPhkCbxv1saoryaFZIiW3Pq7"
search_url = "https://api.twitter.com/2/tweets/search/recent"


def get_district_names(source):
    with open(source, 'r') as district_file:
        district_names = district_file.read()
        return json.loads(district_names)


def create_query(district_name, token=None, max_results=10):
    query_params = {'query': f'({district_name} and berlin) '
                             # f'entity:berlin '
                             f'lang:en '
                             # f'-is:retweet '
                             f'-has:links '
                             f'-has:media',  # place:berlin only available with academic access
                            # 'start_time': start_date,
                            # 'end_time': end_date,
                            'max_results': max_results,
                            'expansions': 'geo.place_id',
                            'tweet.fields': 'id,text,geo,created_at,lang,public_metrics',
                            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                            'next_token': {token}}

    return query_params


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


if __name__ == "__main__":

    id_list = []
    text_list = []
    created_at_list = []
    lang_list = []
    city_district_list = []
    geo_list = []

    max_number_of_tweets_per_district = 1000
    number_of_tweets_per_request = 10

    list_of_districts = get_district_names('data/berlin_districts_transformed.json')

    for district in list_of_districts.keys():
        district_variations = list_of_districts[district]

        for district_variation in district_variations:
            token = None
            number_of_returned_tweets = 0

            keep_fetching = True

            while keep_fetching:

                # make requests
                query = create_query(district_variation, token, number_of_tweets_per_request)
                json_response = connect_to_endpoint(search_url, query)

                # check json response and define if more request are needed
                # no tweets returned
                if json_response['meta']['result_count'] == 0:
                    keep_fetching = False
                    print("no results")
                    continue

                # tweets returned but no token for next request
                if 'next_token' not in json_response['meta']:
                    keep_fetching = False
                    print("no new token " + str(json_response['meta']['result_count']))
                else:
                    token = json_response['meta']['next_token']

                # number of tweets is bigger than threshold
                number_of_returned_tweets += json_response['meta']['result_count']
                if number_of_returned_tweets >= max_number_of_tweets_per_district:
                    keep_fetching = False
                    print("max number of tweets reached")

                # store results
                returned_data_df = pd.DataFrame(json_response['data'])

                for index, row in returned_data_df.iterrows():
                    id_list.append(row['id'])
                    text_list.append(row['text'])
                    created_at_list.append(row['created_at'])
                    lang_list.append(row['lang'])
                    city_district_list.append(district)

                print(str(number_of_returned_tweets) + " " + district_variation)

    final_data_df = pd.DataFrame(
        {'id': id_list,
         'text': text_list,
         'created_at': created_at_list,
         'lang': lang_list,
         #'geo': geo_list,
         'city_district': city_district_list}
    )

    final_data_df.to_csv('data/data.csv', encoding='utf-8')
