import plotly
from bertopic import BERTopic
import umap
import json
import pandas as pd
import gensim.corpora as corpora
from gensim.models.coherencemodel import CoherenceModel

import src.helper as helper


def get_topics_per_district(data):

    result = {}

    # for each district
    for district in data['District'].unique():
        district_tweets = data[data['District'] == district]


        # for all tweets with positive sentiments
        positive_tweets = district_tweets[district_tweets['Sentiment Score'] > 0]
        top_positive_topics, coherence_pos = get_top_topics(positive_tweets['Pre_Processed'].tolist())

        # for all the tweets with negative sentiments
        negative_tweets = district_tweets[district_tweets['Sentiment Score'] < 0]
        top_negative_topics, coherence_neg = get_top_topics(negative_tweets['Pre_Processed'].tolist())

        # add topics to result
        topics = {'positive topics': top_positive_topics, 'coherence pos': coherence_pos,
                  'negative topics': top_negative_topics, 'coherence neg': coherence_neg}

        result[district] = topics

    result = json.dumps(result)
    helper.save_data_to_json('data/topics.json', result)

    return result


def get_top_topics(tweets):

    if len(tweets) == 0:
        return [],''

    try:
        model = BERTopic(embedding_model='xlm-r-bert-base-nli-stsb-mean-tokens', nr_topics="auto", n_gram_range = (1,3))
        topics, probabilities = model.fit_transform(tweets)

        # Preprocess Documents
        documents = pd.DataFrame({"Document": tweets,
                                  "ID": range(len(tweets)),
                                  "Topic": topics})
        documents_per_topic = documents.groupby(['Topic'], as_index=False).agg({'Document': ' '.join})
        cleaned_docs = model._preprocess_text(documents_per_topic.Document.values)

        # Extract vectorizer and analyzer from BERTopic
        vectorizer = model.vectorizer_model
        analyzer = vectorizer.build_analyzer()

        # Extract features for Topic Coherence evaluation
        words = vectorizer.get_feature_names()
        tokens = [analyzer(doc) for doc in cleaned_docs]
        dictionary = corpora.Dictionary(tokens)
        corpus = [dictionary.doc2bow(token) for token in tokens]
        topic_words = [[words for words, _ in model.get_topic(topic)]
                       for topic in range(len(set(topics)) - 1)]

        # Evaluate
        coherence_model = CoherenceModel(topics=topic_words,
                                         texts=tokens,
                                         corpus=corpus,
                                         dictionary=dictionary,
                                         coherence='c_v')
        coherence = coherence_model.get_coherence()

    except:
        return [], ''

    result = []

    n_topics = len(set(topics))
    if n_topics >= 4:
        n_topics = 4

    for i in range(n_topics - 1):
        topic = model.get_topic(i)
        key_words = [key_word[0] for key_word in topic[:5]]
        result.append(','.join(key_words))

    return result, coherence


def get_topics(data, nr_of_topics):
    umap_model = umap.UMAP(init='random')
    model = BERTopic(embedding_model='xlm-r-bert-base-nli-stsb-mean-tokens',
                     nr_topics=nr_of_topics,
                     n_gram_range=(1, 3),
                     umap_model=umap_model)

    topics, probabilities = model.fit_transform(data)

    vis = model.visualize_topics()

    plotly.offline.plot(vis, filename=f'resources for präsi/topic_model_overview_{nr_of_topics}.html')

