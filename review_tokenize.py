# 사전에 docker에 gtp7473/gtp7473/nori_tokenize_es:latest 가 돌고 있어야함.

import pandas as pd
import requests
import json
import time
import re

tokenizer_url = 'http://localhost:9200/mix_tokenizer'



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


def df_tokenize(raw_data, analyzer_url='http://localhost:9200/mix_tokenizer'):
    """
    자료가 reviews라는 db collection으로 부터 왔다고 가정하고
    그 df에 토큰화 및 후처리한 내용을 담아서 다시 돌려주는 과정
    """
    review_list = raw_data['content'].tolist()
    title_list = raw_data['title'].tolist()
    title_tokens = []
    content_tokens = []
    for i, review in enumerate(review_list):
        nonstop = str_tokenize(review, analyzer_url)
        content_tokens.append(nonstop)
        if i%100 == 0:
            print('{} step finish'.format(i))
    for i, title in enumerate(title_list):
        nonstop = str_tokenize(title, analyzer_url)
        title_tokens.append(nonstop)
        if i%100 == 0:
            print('{} step finish'.format(i))
    print('Tokenize End')
    raw_data['title_token'] = title_tokens
    raw_data['content_token'] = content_tokens
    return raw_data

