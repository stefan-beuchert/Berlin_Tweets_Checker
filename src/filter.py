import nltk
from nltk.tokenize import word_tokenize

# nltk.download('punkt')


def filter(data):
    return data[data.apply(row_filter, axis=1)]


def row_filter(row):
    filter_words = ["vladimir", "lenin", "marx", "murder", "kleiner", "russia", "rudolf", "hess", "gregor", "pinke",
                    "murder", "kleiner", "russia", "russian", "court", "holocaust"]
    row_words = word_tokenize(row.Pre_Processed)
    for word in row_words:
        if word in filter_words:
            return False
    return True
