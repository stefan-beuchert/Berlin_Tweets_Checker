from wordcloud import WordCloud
import matplotlib.pyplot as plt
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
import spacy

import src.pre_processor as preprocessor


def explore_data(data):
    # make a wordcloud
    create_wordcloud(data)


def basic_tweet_per_district_distribution(data):
    data_aggregated = data[['city_district']].groupby('city_district').size().reset_index(name='counts')

    plt.xticks(rotation='vertical')
    plt.bar(data_aggregated.city_district, height=data_aggregated.counts)
    plt.title('distribution of districts')

    plt.tight_layout()
    plt.savefig('../visualizations/distribution_of_districts.png')


def create_wordcloud(data):
    all_tweets = ' '.join(data['Pre_Processed'])

    wordcloud = WordCloud(width=1600, height=800, background_color="white", max_words=5000, contour_width=3,
                          contour_color='steelblue')
    wordcloud.generate(all_tweets)
    plt.figure(figsize=(160, 90))

    path = 'resources for präsi/word_cloud.png'
    wordcloud.to_file(path)
    print(f"wordcloud saved as f{path}")


#https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/
def topic_model(data):
    print("1")
    data_words = preprocessor.tokenize_tweets(data['Pre_Processed'])

    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)  # higher threshold fewer phrases.

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)

    data_words_bigrams = [bigram_mod[doc] for doc in data_words]

    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    print("2")
    data_lemmatized = lemmatization(data_words_bigrams, nlp, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)

    # Create Corpus
    texts = data_lemmatized

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    print("3")
    coherence_per_number_of_topics = {}

    for number_of_topics in range(5, 51, 5):
    #{5: 0.5060531630034373, 10: 0.43077922116130346, 15: 0.395309099971014, 20: 0.4393223979749954, 25: 0.44120308799427327, 30: 0.4520656275733501, 35: 0.5310623458376399, 40: 0.4362516197499013, 45: 0.4416682006913991, 50: 0.4223327804047966}
        # Build LDA model
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                    id2word=id2word,
                                                    num_topics=number_of_topics,
                                                    random_state=100,
                                                    update_every=1,
                                                    chunksize=100,
                                                    passes=10,
                                                    alpha='auto',
                                                    per_word_topics=True)
        print("4")
        coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
        print("5")
        coherence_score = coherence_model_lda.get_coherence()
        print(coherence_score)
        coherence_per_number_of_topics[number_of_topics] = coherence_score
        print("6")

    print(coherence_per_number_of_topics)


def lemmatization(texts, nlp, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']): # mybe only nouns?
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

