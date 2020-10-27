# visualize_kaist

카이스트에 대해 보도된 각종 기사들을 크롤링하고, 그에 nlp 분석 기법들을 이용하여, 최종적으로 html파일 형식으로 직접 유저가 분석 결과를 직접 눌러보면서 확인할 수 있는 interactive graph를 만드는 프로젝트임. 

1. Korean crawling 폴더에는 한국의 보도국 당 크롤링을 하는 주피터 노트북 파일이 들어있으며  -> 이후 py 파일로 묶어서, 외부에서 함수 호출 가능한 형태로 변환할 예정
2. English crawling 폴더에는 영어 보도국 당 크롤링을 하는 주피터 노트북 파일이 들어가 있음. -> 이후 py 파일로 묶어서, 외부에서 함수 호출 가능한 형태로 변환할 예정

작성된 파일들은 폴더 밖의 korean_analize 주피터 노트북에서, nori-tokenizer(ES search)를 통해 토크나이징 되어, sklearn 및 gensim의 각종 라이브러리를 통해 원하는 형태로 분석이 가능함. 
현재 구현되어 있는 분석 기법의 경우 다음과 같음. 
  1. Countervectiorizer(각 문서에서 고 빈도로 등장한 단어 순으로 정렬)
  2. TF-IDF(문서당 단어의 가중치를 다르게 줌으로써, 그 가중치가 높은 순으로 단어를 정렬) 
  3. Word2vector( 단어를 window를 기반으로 embedding하여, 문장 내에서 비슷한 맥락을 가진 단어들을 가까운 위치에 등장시키는 기법) 
  4. CountCoccur( 단어를 기준으로 그 단어가 등장한 경우, window를 만들어서, 그 window내의 단어의 개수를 파악하여, 함께 어떠한 단어가 주로 등장하는지 파악하는 기법) 
  5. LDA (Topic modeling , NMF의 일종으로 주로 문장에서 어떠한 토픽이 등장하는지 분석하는 기법) 
 
 이후 이러한 분석 결과를 visualization 내부의 json파일로 보내고, 이 json파일을 html이 읽어서 interactive graph를 만들 예정.(by d3-cloud) -> 현재는 서버형태로 띄우지 않으면 작동 불가능함. 
 서버로 띄우고 싶다면 인터넷에서 nodejs를 다운받고, 그 nodejs를 기반으로 index.html을 실행시킬 것. 
 또한 토픽 모델링의 경우 현재 폴더안의 topic_modeling.html의 경우 완성된 파일로써 topic modeling용 visulization graph임. 
 
 
