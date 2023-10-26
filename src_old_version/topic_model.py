import os
import gensim
import gensim.corpora as corpora
#import pyLDAvis.gensim
import pickle
import pyLDAvis

from src.helper import load_data
from preprocessing import pre_process_tweets

data = load_data('../data/data_backup.csv')
data['processed'], _ = pre_process_tweets(data['text'], True)

# Create Dictionary
id2word = corpora.Dictionary(data['processed'])
# Create Corpus
#texts = data_words
# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in data['processed']]
# View
num_topics = 10
# Build LDA model
lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                       id2word=id2word,
                                       num_topics=num_topics)

# Visualize the topics
pyLDAvis.enable_notebook()
LDAvis_data_filepath = os.path.join('../data/ldavis_prepared'+str(num_topics))
# # this is a bit time consuming - make the if statement True
# # if you want to execute visualization prep yourself
if 1 == 1:
    LDAvis_prepared = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    with open(LDAvis_data_filepath, 'wb') as f:
        pickle.dump(LDAvis_prepared, f)
# load the pre-prepared pyLDAvis data from disk
with open(LDAvis_data_filepath, 'rb') as f:
    LDAvis_prepared = pickle.load(f)
pyLDAvis.save_html(LDAvis_prepared, '../visualizations/lda_model'+ str(num_topics) +'.html')
#LDAvis_prepared
