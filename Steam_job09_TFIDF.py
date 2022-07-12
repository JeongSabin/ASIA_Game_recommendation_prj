import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

df_reviews = pd.read_csv('./Steam_data/steam_cleaned_review_one.csv')
df_reviews.info()
#  #   Column                 Non-Null Count  Dtype
# ---  ------                 --------------  -----
#  0   title                  232 non-null    object
#  1   first_cleaned_reviews  232 non-null    object

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['first_cleaned_reviews'])
print(Tfidf_matrix.shape)
# (232, 39872)
print(Tfidf_matrix[0].shape)
# (1, 39872)
with open('./Steam_models/steam_tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./Steam_models/Tfidf_steam_review.mtx', Tfidf_matrix)