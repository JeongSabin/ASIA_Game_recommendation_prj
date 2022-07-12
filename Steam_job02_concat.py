import pandas as pd
import glob

df = pd.DataFrame()
data_paths = glob.glob('./Steam_crawling_data/1_300/*')

for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace = True)
    df_temp.drop_duplicates(inplace=True)
    df =  pd.concat([df, df_temp], ignore_index=True)


df.drop_duplicates(inplace=True)
df.info()
#  #   Column   Non-Null Count   Dtype
# ---  ------   --------------   -----
#  0   title    102313 non-null  object
#  1   reviews  102313 non-null  object

df.to_csv('./Steam_crawling_data/1_300/steam_reviews_ranking_161_300.csv', index=False)