import pandas as pd
import glob

df = pd.DataFrame()
data_paths = glob.glob('Google_play_crawling_data/*')

for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace = True)
    df_temp.drop_duplicates(inplace=True)
    df =  pd.concat([df, df_temp], ignore_index=True)


df.drop_duplicates(inplace=True)
df.info()

df.to_csv('./Google_play_data/google_play_store_reviews_last.csv', index=False)