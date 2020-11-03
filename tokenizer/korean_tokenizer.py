# 사전에 docker에 gtp7473/gtp7473/nori_tokenize_es:latest 가 돌고 있어야함.

import pandas as pd
import requests
import json
import time
import re
from ckonlpy.tag import Twitter
from ckonlpy.utils import load_wordset


tokenizer_url = 'http://localhost:9200/mix_tokenizer'


def call_userword():
    with open('./tokenizer/korean_userword.txt', 'r', encoding='utf-8-sig') as f:
        return f.readlines()


def nori_reset(url):
    """
    nori 토크나이저의 단어사전이 바뀔 경우 토크나이저를 껐다 켜야하는데, 그걸 자동으로 실행해주는 함수
    """
    close_url = url + '/_close'
    res = requests.post(close_url)
    res.raise_for_status()
    open_url = url + '/_open'
    res = requests.post(open_url)
    res.raise_for_status()


def str_tokenize(text, analyzer_url):
    """
    text 하나를 입력하면, nori에서 토큰화 하고, 이후 후처리까지 해주는 과정
    후처리 : 토큰중 원하는 pos만 뽑고, 어근은 '+하다' 동사,형용사는 '+다'로 복구
    """
    global response
    url = analyzer_url + '/_analyze'
    headers = {
        'content-type': "application/json",
        'Connection': "close",
    }
    compound = []
    tokens_1 = []
    tokens = []
    one_word = ['겔', '결', '굿', '귤', '깡', '꽃', '꿀',
                '꿈', '꿩', '낮', '넋', '늪', '덫', '등', '똥',
                '뜸', '말', '맘', '맛', '멋', '멍', '밖', '밥',
                '방', '뱀', '벌', '벨', '볏', '불', '붐', '붓', '빗',
                '빚', '빛', '뺨', '뽕', '살', '색', '샘', '셀', '솔',
                '솜', '술', '숲', '숯', '쏙', '쑥', '옷', '옻', '욕',
                '윷', '즙', '춤', '칡', '침', '칼', '퀄', '킵', '템',
                '펄', '펜', '향', '헐', '헬', '짱', "웜", "톤"]
    requset = {"analyzer": "nori_analyzer", "text": text, "explain": 'true',
               "attributes": ["leftPos", "posType", "morphemes"]}
    payload = json.dumps(requset)
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        response.raise_for_status()
    except Exception:
        print(payload)
        print(response.text)
    response_json = json.loads(response.text)

    for token in response_json['detail']['tokenfilters'][0]['tokens']:
        if token['posType'] == 'INFLECT':
            continue
        elif token['posType'] == 'COMPOUND':
            tokens.append(token['token'])
            if token['morphemes'] is None:
                continue
            for morpheme in token['morphemes'].split('+'):
                compound.append(morpheme.split('/')[0])
            continue
        if token['leftPOS'] == 'VA(Adjective)' or token['leftPOS'] == 'VV(Verb)':
            tokens.append(token['token'] + '다')
        elif token['leftPOS'] == 'XR(Root)':
            tokens.append(token['token'] + '하다')
        else:
            if token['token'] in compound:
                compound.remove(token['token'])
                continue
            else:
                tokens.append(token['token'])

    return tokens


def tokenize_nori(df, analyzer_url='http://localhost:9200/mix_tokenizer'):
    """
    자료가 reviews라는 db collection으로 부터 왔다고 가정하고
    그 df에 토큰화 및 후처리한 내용을 담아서 다시 돌려주는 과정
    """
    df['content_token'] = df.progress_apply(
        lambda x: str_tokenize(x['content']), axis=1)
    df['title_token'] = df.progress_apply(
        lambda x: str_tokenize(x['title']), axis=1)
    return df


def tokenize_okt(df):
    okt = Twitter()
    okt.add_dictionary(call_userword(), 'Noun')
    stopwords = load_wordset('./tokenizer/korean_stopword.txt')
    stopwords = stopwords | load_wordset('./tokenizer/korean_screen.txt')
    stopwords = list(stopwords)
    df['content_token'] = df.progress_apply(lambda x: [t[0] for t in okt.pos(
        x['content'], stem=True) if t[1] in ['Noun', 'Verb', 'Adjective'] and t[0] not in stopwords], axis=1)
    df['title_token'] = df.progress_apply(lambda x: [t[0] for t in okt.pos(
        x['title'], stem=True) if t[1] in ['Noun', 'Verb', 'Adjective'] and t[0] not in stopwords], axis=1)
    return df


def tokenize_okt_noscreen(df):
    okt = Twitter()
    okt.add_dictionary(call_userword(), 'Noun')
    stopwords = load_wordset('./tokenizer/korean_stopword.txt')
    stopwords = stopwords | load_wordset('./tokenizer/korean_screen.txt')
    stopwords = list(stopwords)
    df['content_token'] = df.progress_apply(lambda x: [t[0] for t in okt.pos(
        x['content'], stem=True) if t[1] in ['Noun', 'Verb', 'Adjective'] and t[0] not in stopwords], axis=1)
    df['title_token'] = df.progress_apply(lambda x: [t[0] for t in okt.pos(
        x['title'], stem=True) if t[1] in ['Noun', 'Verb', 'Adjective'] and t[0] not in stopwords], axis=1)
    return df