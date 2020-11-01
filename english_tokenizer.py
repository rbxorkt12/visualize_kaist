import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import pandas as pd
import re

# Data Preprocessing


def preprocess(text):
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


def call_stopwords():
    with open('stopwords.txt', 'r') as f:
        stopwords = f.readlines()
        stopwords = list(map((lambda x: x.rstrip('\n')), stopwords))
    return stopwords


def english_tokenize(df):
    titles_token = []
    contents_token = []
    for i, row in enumerate(df.itertuples()):
        title_token = []
        content_token = []
        title = getattr(row, 'title')
        content = getattr(row, 'content')
        title_token = preprocess(title)
        content_token = preprocess(content)
        titles_token.append(title_token)
        contents_token.append(content_token)
        if i % 10 == 0:
            print(i)
    df['title_token'] = titles_token
    df['content_token'] = contents_token
    return df
