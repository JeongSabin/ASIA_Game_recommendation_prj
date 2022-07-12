import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

df_reviews = pd.read_csv('Google_play_data/google_play_cleaned_review_one_last.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['reviews'])
print(Tfidf_matrix.shape)
# (3182, 84461)
print(Tfidf_matrix[0].shape)
# (1, 84461)
with open('google_play_models/tfidf_google.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./Google_play_models/Tfidf_game_review_google.mtx', Tfidf_matrix)