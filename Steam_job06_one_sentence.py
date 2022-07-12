#같은 게임 리뷰끼리 묶기

import pandas as pd

df = pd.read_csv('./Steam_data/steam_cleaned_review.csv')
df.dropna(inplace=True)

one_reviews = []

for title in df['title'].unique():
    temp = df[df['title']==title]
    # if len(temp) > 100:  # 리뷰가 너무 많을 수 있으니 제한
    #     temp = temp.iloc[:100, :]  # 리뷰 개수가 100개보다 크면 100개까지만 사용
    one_sentence = ' '.join(temp['first_cleaned_reviews'])
    one_reviews.append(one_sentence)

df_one = pd.DataFrame({'title': df['title'].unique(), 'first_cleaned_reviews': one_reviews})
print(df_one.head())
df_one.info()
#  #   Column   Non-Null Count  Dtype
# ---  ------   --------------  -----
#  0   title    239 non-null    object
#  1   reviews  239 non-null    object

df_one.to_csv('./Steam_data/steam_cleaned_review_one.csv', index=False)