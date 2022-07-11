import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./reviews/reviews_steam_ranking_1_1000.csv')
df.info()

okt = Okt()

df_stopwords = pd.read_csv('./stopwords.csv')