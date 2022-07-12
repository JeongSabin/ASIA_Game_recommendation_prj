import pandas as pd
import glob

df = pd.DataFrame()
data_paths = glob.glob('Steam_Google_concat_file/*')

for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace = True)
    df_temp.drop_duplicates(inplace=True)
    df =  pd.concat([df, df_temp], ignore_index=True)


df.drop_duplicates(inplace=True)
df.info()

df.to_csv('./Steam_Google_concat_file/All_reviews_one', index=False)