import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import pandas as pd
import re

# Data Preprocessing


def tokenize(text):
    try:
        text =str(text)
        # tokenize into words
        text = re.sub('[^A-Za-z ]', '', text)
        tokens = [word for sent in nltk.sent_tokenize(text)
                for word in nltk.word_tokenize(sent)]
        # remove stopwords
        stop = stopwords.words('english')
        tokens = [token for token in tokens if token not in stop +
                call_stopwords() + ['this']]
        # remove words less than three letters
        tokens = [word for word in tokens if len(word) >= 3]
        # lower capitalization
        tokens = [word.lower() for word in tokens]
        # lemmatization
        lmtzr = WordNetLemmatizer()
        tokens = [lmtzr.lemmatize(word) for word in tokens]
        tokens = [lmtzr.lemmatize(word, 'v') for word in tokens]
        # stemming
        return tokens
    except:
        return ['']
def call_stopwords():
    with open('./tokenizer/stopwords.txt', 'r') as f:
        stopwords = f.readlines()
        stopwords = list(map((lambda x: x.rstrip('\n')), stopwords))
    return stopwords


def tokenize_nltk(df):
    df['content_token']= df.progress_apply(lambda x : tokenize(x['content']),axis=1)
    df['title_token'] = df.progress_apply(lambda x : tokenize(x['title']),axis=1)
    return df
