import pandas as pd

df = pd.read_csv('Google_play_data/google_play_cleaned_reviews_last.csv')
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
df_one.to_csv('./Google_play_data/google_play_cleaned_review_one_last.csv', index=False)