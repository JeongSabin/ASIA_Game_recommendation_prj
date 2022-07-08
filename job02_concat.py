import pandas as pd
import glob

df = pd.DataFrame()
data_paths = glob.glob('./reviews/*')

for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace = True)
    df_temp.drop_duplicates(inplace=True)
    df =  pd.concat([df, df_temp], ignore_index=True)


df.drop_duplicates(inplace=True)
df.info()

df.to_csv('./reviews/reviews_steam_ranking_1_1000.csv', index=False)