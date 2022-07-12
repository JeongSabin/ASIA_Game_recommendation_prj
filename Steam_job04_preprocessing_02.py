import pandas as pd
from konlpy.tag import Okt
import re
from konlpy.tag import Komoran
import konlpy

df = pd.read_csv('./Steam_crawling_data/301_600/steam_clr1_501_600_001_HN02.csv')

okt = Okt()
# konlpy.jvm.init_jvm(jvmpath=None, max_heap_size=4096)
# konlpy.jvm.init_jvm(jvmpath=None, max_heap_size=4096)

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
                         '빡종', '화면', '토핑같', '쫓아쥬', '게임광', '리뷰', '답변', '게암', '려고', '핸드폰', '아이폰', '딥빡', '시일', '같아뇨', '매크로', '팝업', '살수', '돵도']


first_cleaned_reviews = []

for review in df.review_clear1:

    review = re.sub('[^가-힣 ]', ' ', review)
    token = okt.pos(review, stem=True)

    df_token = pd.DataFrame(token, columns=['word', 'class'])  #튜플형태 >> 컬럼 두개짜리 데이터프레임 으로 변환
    df_token = df_token[(df_token['class']=='Noun') | (df_token['class']=='Verb') | (df_token['class']=='Adjective') | (df_token['class']=='Adverb')]
    print(df_token)
    # exit()

    words =[]
    for word in df_token.word:
        if 1 < len(word) < 10:
            if word not in stopwords :
                words.append(word)
    cleaned_sentence = ' '.join(words)
    first_cleaned_reviews.append(cleaned_sentence)

df['first_cleaned_reviews'] = first_cleaned_reviews
df = df[['title', 'first_cleaned_reviews']]
df.dropna(inplace=True)

df.to_csv('./Steam_crawling_data/301_600/steam_clr2_501_600_001_HN02.csv', index=False)
print(df)
df.info()