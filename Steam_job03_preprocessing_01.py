import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./Steam_crawling_data/1_300/reviews_181_200.csv')
df.info()

review_clear1 =[]

for i in df['reviews'] :
    if len(i) > 60:
        review_clear1.append(i)
    else:
        review_clear1.append('끝일까')

df['review_clear1'] = review_clear1
dfresult = df[~df['review_clear1'].str.contains("끝일까", na=False, case=False)]

df_clear = dfresult[['title', 'review_clear1']]
df_clear.dropna(inplace=True)
df_clear.to_csv('./Steam_crawling_data/1_300/steam_clr1_181_200.csv', index=False)
print(df_clear)
df_clear.info()

exit()