- 프로젝트 설명

카이스트에 대해 보도된 각종 기사들을 크롤링하고, 그에 NLP 분석 기법들을 이용하여, 최종적으로 html파일 형식으로 직접 유저가 분석 결과를 직접 눌러보면서 확인할 수 있는 
인터랙티브 워드클라우드 및 단어 네트워크를 만드는 프로젝트입니다. visualize 폴더의 english, korean, journal 폴더에 각 신문사마다 폴더가 나뉘어져있고 각 폴더에는 html 파일이 존재합니다.
html 파일을 클릭해서 browser 창에서 띄우게 되면 인터랙티브 워드클라우드 및 단어 네트워크를 확인하실 수 있습니다. 
워드클라우드의 단어를 클릭하면 아래 Similar Detail과 Coocurrence Detail에 해당 단어를 중심으로 한 네트워크를 확인하실 수 있습니다.
visualize 폴더의 non_interactive_wordcloud 폴더에는 원형 모양의 워드클라우드와 'KAIST' 글자 모양의 워드클라우드 png 파일이 저장되어있습니다. 
인터랙티브 워드클라우드는 직접 눌러보시면서 다양한 인사이트를 얻을 때 사용하고, 게시물에 첨부할 사진으로는 png 파일로 저장된 워드클라우드를 이용한다면 이 프로젝트를 더 잘 활용할 수 있습니다. 
  
- 파일 구조 설명
    1. english_crawling : 영어 기사를 크롤링한 코드와 데이터를 담은 폴더.
    2. journal_crawling : nature, science의 저널을 크롤링한 코드와 데이터를 담은 폴더.
    3. korean_crawling : 한국어 기사를 크롤링한 코드와 데이터를 담은 폴더.
    4. tokenizer : 토큰화 작업을 하는 코드와 사용자 사전 및 불용어 사전을 담은 폴더.
    5. visualize : 워드클라우드 및 토픽모델링을 시각화한 html 파일을 담은 폴더. 여기에서 시각화 결과를 확인할 수 있습니다.
    6. render.py : 분석 결과를 html 파일로 렌더링 해주는 코드.
    7. visualize.ipynb, visualize.py : 분석 결과를 시각화 해주는 코드.
    
 - 사전 단어 추가
 
 텍스트 분석은 불용어 제거와 사용자 사전 추가를 얼마나 잘 하느냐에 따라 성능이 매우 크게 달라집니다.
 하지만, 일일이 사람이 확인하면서 단어를 추가해야하기 때문에 한계가 존재합니다. 
 따라서, 사용중에 보고싶지 않은 단어(불용어)는 tokenizer/korean_stopword, 토큰화가 잘못되어 추가하고 싶은 단어는 tokenizer/korean_userword에 추가해주시기 바랍니다.
 추후에 추가된 단어로 다시 분석을 돌리는 작업을 통해 업데이트하도록 하겠습니다. 
   
- 사용된 분석 기법
  1. Countervectiorizer(각 문서에서 고 빈도로 등장한 단어 순으로 정렬)
  2. TF-IDF(문서당 단어의 가중치를 다르게 줌으로써, 그 가중치가 높은 순으로 단어를 정렬) 
  3. Word2vector( 단어를 window를 기반으로 embedding하여, 문장 내에서 비슷한 맥락을 가진 단어들을 가까운 위치에 등장시키는 기법) 
  4. CountCoccur( 단어를 기준으로 그 단어가 등장한 경우, window를 만들어서, 그 window내의 단어의 개수를 파악하여, 함께 어떠한 단어가 주로 등장하는지 파악하는 기법) 
  5. LDA (Topic modeling , NMF의 일종으로 주로 문장에서 어떠한 토픽이 등장하는지 분석하는 기법) 

- 개발 환경 설정 및 분석 코드 실행
~~~
pip install -r requirements.txt
python visualize.py
~~~
![korean_joongang_screen_title_wordcloud json_circle](https://user-images.githubusercontent.com/64149539/98245674-a3589d00-1fb4-11eb-8ae2-8c12bd75c3ab.png)
![korean_joongang_screen_title_wordcloud json_kaist](https://user-images.githubusercontent.com/64149539/98245677-a5226080-1fb4-11eb-8526-cfcdac2e2554.png)
