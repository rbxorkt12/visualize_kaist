# 사전에 docker에 gtp7473/gtp7473/nori_tokenize_es:latest 가 돌고 있어야함.

import pandas as pd
import json
import re
from ckonlpy.tag import Twitter
from ckonlpy.utils import load_wordset


def call_userword():
    with open('./tokenizer/korean_userword.txt', 'r', encoding='utf-8-sig') as f:
        return list(map(lambda x: x.rstrip('\n'), f.readlines()))


def text_tokenize(text,okt,stopwords):
    tokens = []
    for t in okt.pos(text, stem=True) :
        if t[1] in ['Noun', 'Verb', 'Adjective'] : 
            if len(t[0]) != 1 and t[0] not in stopwords:
                tokens.append(t[0])
        elif t[1] in ['Alpha']:
            tokens.append(t[0].lower())
    return list(map(lambda x: x.replace("카이스트","kaist"),tokens))

def tokenize_okt(df):
    okt = Twitter()
    okt.add_dictionary(call_userword(), 'Noun')
    stopwords = load_wordset('./tokenizer/korean_stopword.txt')
    stopwords = stopwords | load_wordset('./tokenizer/korean_screen.txt')
    stopwords = list(stopwords)
    df['content_token'] = df.progress_apply(lambda x: text_tokenize(x['content'],okt,stopwords), axis=1)
    df['title_token'] = df.progress_apply(lambda x: text_tokenize(x['title'],okt,stopwords), axis=1)
    return df

def tokenize_okt_noscreen(df):
    okt = Twitter()
    okt.add_dictionary(call_userword(), 'Noun')
    stopwords = load_wordset('./tokenizer/korean_stopword.txt')
    #stopwords = stopwords | load_wordset('./tokenizer/korean_screen.txt')
    stopwords = list(stopwords)
    df['content_token'] = df.progress_apply(lambda x: text_tokenize(x['content'],okt,stopwords), axis=1)
    df['title_token'] = df.progress_apply(lambda x: text_tokenize(x['title'],okt,stopwords), axis=1)
    return df
