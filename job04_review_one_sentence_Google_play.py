import pandas as pd

df = pd.read_csv('google_play_data/first_cleaned_google_play_reviews.csv')
df.dropna(inplace=True)
df.info()
one_sentences = []
for title in df['game'].unique():
    temp = df[df['game'] == title]
    if len(temp) > 30:
        temp = temp.iloc[:30, :]
    one_sentence = ' '.join(temp['first_cleaned_reviews'])
    one_sentences.append(one_sentence)
df_one = pd.DataFrame({'games':df['game'].unique(), 'reviews':one_sentences})
print(df_one.head())
df_one.to_csv('./google_play_data/google_play_cleaned_review_one.csv', index=False)