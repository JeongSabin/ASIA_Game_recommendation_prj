import pandas as pd
import glob

df = pd.DataFrame()
data_paths = glob.glob('./Steam_crawling_data/clr2/*')

for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace = True)
    df_temp.drop_duplicates(inplace=True)
    df =  pd.concat([df, df_temp], ignore_index=True)


df.drop_duplicates(inplace=True)
df.info()
#  #   Column                 Non-Null Count  Dtype
# ---  ------                 --------------  -----
#  0   title                  60485 non-null  object
#  1   first_cleaned_reviews  60485 non-null  object

df.to_csv('./Steam_data/steam_cleaned_review.csv', index=False)