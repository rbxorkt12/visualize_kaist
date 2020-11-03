# visualize_kaist

카이스트에 대해 보도된 각종 기사들을 크롤링하고, 그에 NLP 분석 기법들을 이용하여, 최종적으로 html파일 형식으로 직접 유저가 분석 결과를 직접 눌러보면서 확인할 수 있는 interactive graph를 만드는 프로젝트입니다. 워드클라우드와 토픽모델링은 visualize 폴더로 이동하여 확인하시면 됩니다.

- 파일 구조 설명
    1. english_crawling : 영어 기사를 크롤링한 코드와 데이터를 담은 폴더.
    2. journal_crawling : nature, science의 저널을 크롤링한 코드와 데이터를 담은 폴더.
    3. korean_crawling : 한국어 기사를 크롤링한 코드와 데이터를 담은 폴더.
    4. tokenizer : 토큰화 작업을 하는 코드와 사용자 사전 및 불용어 사전을 담은 폴더.
    5. visualize : 워드클라우드 및 토픽모델링을 시각화한 html 파일을 담은 폴더. 여기에서 시각화 결과를 확인할 수 있습니다.
    6. render.py : 분석 결과를 html 파일로 렌더링 해주는 코드.
    7. visualize.ipynb, visualize.py : 분석 결과를 시각화 해주는 코드.

- 사용된 분석 기법
  1. Countervectiorizer(각 문서에서 고 빈도로 등장한 단어 순으로 정렬)
  2. TF-IDF(문서당 단어의 가중치를 다르게 줌으로써, 그 가중치가 높은 순으로 단어를 정렬) 
  3. Word2vector( 단어를 window를 기반으로 embedding하여, 문장 내에서 비슷한 맥락을 가진 단어들을 가까운 위치에 등장시키는 기법) 
  4. CountCoccur( 단어를 기준으로 그 단어가 등장한 경우, window를 만들어서, 그 window내의 단어의 개수를 파악하여, 함께 어떠한 단어가 주로 등장하는지 파악하는 기법) 
  5. LDA (Topic modeling , NMF의 일종으로 주로 문장에서 어떠한 토픽이 등장하는지 분석하는 기법) 
 

- 개발 환경 설정
--> pip install requirements.txt
 