from turtle import back
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

rc('font', family='LG_PC.TTF')
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('./Steam_data/steam_cleaned_review_one.csv')
words = df[df['title']=='7 Days to Die']['first_cleaned_reviews']
print(words.iloc[0])
words = words.iloc[0].split()
print(words)

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)

wordcloud_img = WordCloud(background_color='white', max_words=2000, font_path='LG_PC.TTF').generate_from_frequencies(worddict)

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()