import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('Google_play_data/google_play_store_reviews_last.csv')
df.info()
#  #   Column   Non-Null Count  Dtype
# ---  ------   --------------  -----
#  0   title    7117 non-null   object
#  1   reviews  7117 non-null   object


okt = Okt()
df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])
stopwords = stopwords + ['게임', '개새끼', '씨부랄', '지랄', '발작', '존나', '병신', '똥겜', '님덜', '븅신겜', '개꿀', '개판', '빠따', '좆망', '씨벌애', '애비', '새끼', '시발',
                         '오우야', '애액', '조온나', '싯팔', '좃같은겜', '졸라', '씨발', '짱짱', '스레기', '줫망겜임', '발련', '야겜', '쎾스', '엉덩이', '가슴', '줫망겜', '발년',
                         '갇갇갇갇겜', '좃같', '발련들', '씨불', '갞끼', '야껨', '개뿔', '호로', '개객기', '욕설', '줫같', '쒸발년들', '시벌', '섹스', '좆똥겜임', '섹스', '씨빨',
                         '개객끼', '존내', '빻았', '헛지랄', '시발련', '줫패', '개줫같음', '좃돼', '좆목', '씹새끼야', '족치다', '좃도없', '개좆', '부럴', '창년', '좆집', '썅놈',
                         '졋같음', '좆망', '졷같', '대가리', '쥰내', '개빡', '육갑', '빠큐', '싸가지', '일배', '병신임', '창렬겜', '개암', '떵물', '하다', '가격', '진행', '개편',
                         '출시', '안되다', '쓰브랄', '일기토', '개다', '뭣같음', '뭣같아', '개똥', '할인', '구매', '파일', '세이브', '시스템', '유저', '개색기', '쒸바', '플레이',
                         '겠다', '뒤지다', '버그', '제작자', '확장팩', '씨팔', '니미럴', '스팀', '라이브러리', '씨발련', '출시일', '좆망껨', '따먹다', '환불', '게이', '개자식',
                         '펑펑', '톡톡', '빵빵', '컴퓨터', '유료', '결재', '이메일', '로그인', '어떻다', '근데', '니당다', '계정', '던데', '광고', '태블렛', '로만', '현질', '알못',
                         '빡종', '화면', '토핑같', '쫓아쥬', '게임광', '리뷰', '답변', '게암', '려고', '핸드폰', '아이폰', '딥빡', '시일', '같아뇨', '매크로', '팝업', '살수', '돵도',
                         '좋다', '업데이트', '재미있다', '많이', '많다', '고치다', '모드', '제발', '아쉽다', '이렇다', '나오다', '훌륭하다', '그치다', '감사하다', '정도', '문제점', '모바일',
                         '단점', '자체', '접다', '안좋다', '수많다', '되어다', '재밌다', '재미', '적다', '추천', '괜찮다', '어렵다', '없이', '열심히', '충분하다', '싶다', '중요하다', '확실하다',
                         '적당하다', '운영', '주다', '부탁드리다', '드리다', '특징', '가다', '같습니다', '즐기다', '관련', '걸리다', '모르다', '필요', '진짜', '현상', '올리다', '재밌다', '돼다',
                         '모든', '버전', '먹다', '저장', '따르다','추가', '안녕하다', '경우', '보상', '심해지다', '울리다', '해주다', '자다', '짜증나다', '끊기다', '가능하다', '처음', '접속',
                         '느끼다', '느껴지다', '이슈', '서버', '오픈', '버튼', '굉장하다', '갖다', '상당하다', '상황', '두다', '설치', '제거', '중국', '필요하다', '당연하다', '확인', '넣다',
                         '여러가지', '개선', '맞추다', '뱉다', '느낌', '최적화']


# count = 0
first_cleaned_reviews = []

for review in df.review:
    # count += 1
    # if count % 10 == 0 :
    #     print('.', end='')
    # if count % 100 == 0 :
    #     print()

    review = re.sub('[^가-힣 ]', ' ', review)
    #review = review.split()
    token = okt.pos(review, stem=True)

    df_token = pd.DataFrame(token, columns=['word', 'class'])  #튜플형태 >> 컬럼 두개짜리 데이터프레임 으로 변환
    df_token = df_token[(df_token['class']=='Noun') | (df_token['class']=='Verb') | (df_token['class']=='Adjective') | (df_token['class']=='Adverb')]
    print(df_token)
    # exit()

    words =[]
    for word in df_token.word:
        if 1 < len(word) < 10 :
            if word not in stopwords :
                words.append(word)
    cleaned_sentence = ' '.join(words)
    first_cleaned_reviews.append(cleaned_sentence)

df['first_cleaned_reviews'] = first_cleaned_reviews
df = df[['game', 'first_cleaned_reviews']]
df.dropna(inplace=True)

df.to_csv('./Google_play_data/google_play_cleaned_reviews_last.csv', index=False)
print(df)
df.info()