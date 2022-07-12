import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from PyQt5.QtCore import QStringListModel
from PyQt5 import QtGui, QtCore
from konlpy.tag import Okt
import re

form_window = uic.loadUiType('./GAMEBOY.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_recommendation_1.setIcon(QtGui.QIcon('./PHONE2.png'))
        self.btn_recommendation_2.setIcon(QtGui.QIcon('./COMPUTER3.png'))
        self.label_2.setPixmap(QtGui.QPixmap('GAM3-BO1_pyqt_2.png'))
        self.label.setPixmap(QtGui.QPixmap('흰배경.png'))
        self.Tfidf_matrix = mmread('./Google_play_models/Tfidf_game_review_google.mtx').tocsr()
        with open('Google_play_models/tfidf_google.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./Google_play_models/word2vec_google_play_reviews_google.model')
        self.df_reviews = pd.read_csv('./Google_play_data/google_play_cleaned_review_one_last.csv')
        self.titles = list(self.df_reviews['games'])
        self.titles.sort()  # 정렬하기
        # for title in self.titles:  # 3000개 title 가져오기
        #     self.comboBox.addItem(title)



        # self.comboBox.currentIndexChanged.connect(self.combobox_slot)
        self.btn_recommendation_1.clicked.connect(self.btn_slot)
        self.btn_recommendation_2.clicked.connect(self.btn_slot2)

        self.Tfidf_matrix2 = mmread('./Steam_models/Tfidf_steam_review.mtx').tocsr()
        with open('./Steam_models/steam_tfidf.pickle', 'rb') as f:
            self.Tfidf2 = pickle.load(f)
        self.embedding_model2 = Word2Vec.load('./Steam_models/word2vec_steam_reviews.model')
        self.df_reviews2 = pd.read_csv('./Steam_data/steam_cleaned_review_one.csv')
        self.titles2 = list(self.df_reviews2['title'])
        self.titles2.sort()  # 정렬하기

        #자동완성
        self.df_reviews3 = pd.read_csv('./Steam_Google_concat_file/All_reviews_one')
        self.titles3 = list(self.df_reviews3['games'])
        self.titles3.sort()  # 정렬하기
        model = QStringListModel()
        model.setStringList(self.titles3)
        completer = QCompleter()
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)

    def btn_slot(self):
        key_word = self.le_keyword.text()
        if key_word in self.titles:
            recommendation = self.recommendation_by_game_title(key_word)
        elif key_word in list(self.embedding_model.wv.index_to_key):
            recommendation = self.recommendation_by_keyword(key_word)
        elif key_word in self.titles2:
            self.lbl_recommendation.setText('이 게임은 컴퓨터 게임이라 검색할 수 없어요 ㅠㅠ')
            recommendation = False
        else:
            recommendation = self.recommendation_by_sentence(key_word)
        if recommendation:
            self.lbl_recommendation.setText(recommendation)
        else:
            pass


    def getRecommendation(self, cosin_sim):
        simScore = list(enumerate(cosin_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        gameIdx = [i[0] for i in simScore]
        print(gameIdx)
        recGameList = self.df_reviews.iloc[gameIdx, 0]
        print(recGameList)
        return recGameList

    # def combobox_slot(self):
    #     title = self.comboBox.currentText()
    #     recommendation = self.recommendation_by_game_title(title)
    #
    #     self.lbl_recommendation.setText(recommendation)

    def recommendation_by_game_title(self, title):
        game_idx = self.df_reviews[self.df_reviews['games'] == title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[game_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        kinds = '게임 제목으로 추천된 게임들 입니다.\n'
        recommendation = '\n'.join([kinds] + list(recommendation[1:]))
        return recommendation

    def recommendation_by_keyword(self, keyword):
        if keyword:
            keyword = keyword.split()[0]
            try:
                sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
            except:
                self.lbl_recommendation.setText('제가 모르는 단어에요 ㅠㅠ')
                return 0
            sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
            words = [keyword]
            for word, _ in sim_word:
                words.append(word)
            sentence = []
            count = 10
            for word in words:
                sentence = sentence + [word] * count
                count -= 1
            sentence = ' '.join(sentence)
            print(sentence)
            sentence_vec = self.Tfidf.transform([sentence])
            cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
            recommendation = self.getRecommendation(cosine_sim)
            kinds = '키워드로 추천된 게임들 입니다.\n'
            recommendation = '\n'.join([kinds] + list(recommendation[:10]))

            return recommendation
        else :
            return 0
    def recommendation_by_sentence(self, keyword):
        okt = Okt()
        sentence = keyword
        review = re.sub('[^가-힣 ]', ' ', sentence)
        #
        token = okt.pos(review, stem=True)
        #
        df_token = pd.DataFrame(token, columns=['word', 'class'])
        df_token = df_token[(df_token['class'] == 'Noun') |
                            (df_token['class'] == 'Verb') |
                            (df_token['class'] == 'Adjective')]
        words = []
        for word in df_token.word:
            if 1 < len(word):
                words.append(word)
        cleaned_sentence = ' '.join(words)
        print(cleaned_sentence)
        sentence_vec = self.Tfidf.transform([cleaned_sentence])
        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        kinds = '문장으로 추천된 게임들 입니다.\n'
        recommendation = '\n'.join([kinds] + list(recommendation[1:]))

        return recommendation
    def btn_slot2(self):
        key_word = self.le_keyword.text()
        if key_word in self.titles2:
            recommendation2 = self.recommendation_by_game_title2(key_word)
        elif key_word in list(self.embedding_model2.wv.index_to_key):
            recommendation2 = self.recommendation_by_keyword2(key_word)
        elif key_word in self.titles:
            self.lbl_recommendation.setText('이 게임은 모바일 게임이라 검색할 수 없어요 ㅠㅠ')
            recommendation2 = False
        else:
            recommendation2 = self.recommendation_by_sentence2(key_word)

        if recommendation2:
            self.lbl_recommendation.setText(recommendation2)
        else:
            pass


    def getRecommendation2(self, cosin_sim):
        simScore = list(enumerate(cosin_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        gameIdx = [i[0] for i in simScore]
        print(gameIdx)
        recGameList = self.df_reviews2.iloc[gameIdx, 0]
        print(recGameList)
        return recGameList

    # def combobox_slot(self):
    #     title = self.comboBox.currentText()
    #     recommendation = self.recommendation_by_game_title(title)
    #
    #     self.lbl_recommendation.setText(recommendation)

    def recommendation_by_game_title2(self, title):
        game_idx = self.df_reviews2[self.df_reviews2['title'] == title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix2[game_idx], self.Tfidf_matrix2)
        recommendation2 = self.getRecommendation2(cosine_sim)
        kinds = '게임 제목으로 추천된 게임들 입니다.\n'
        recommendation2 = '\n'.join([kinds] + list(recommendation2[1:]))
        return recommendation2

    def recommendation_by_keyword2(self, keyword):
        if keyword:
            keyword = keyword.split()[0]
            try:
                sim_word = self.embedding_model2.wv.most_similar(keyword, topn=10)
            except:
                self.lbl_recommendation2.setText('제가 모르는 단어에요 ㅠㅠ')
                return 0
            sim_word = self.embedding_model2.wv.most_similar(keyword, topn=10)
            words = [keyword]
            for word, _ in sim_word:
                words.append(word)
            sentence = []
            count = 10
            for word in words:
                sentence = sentence + [word] * count
                count -= 1
            sentence = ' '.join(sentence)
            print(sentence)
            sentence_vec = self.Tfidf2.transform([sentence])
            cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix2)
            recommendation2 = self.getRecommendation2(cosine_sim)
            kinds = '키워드로 추천된 게임들 입니다.\n'
            recommendation2 = '\n'.join([kinds] + list(recommendation2[:10]))

            return recommendation2
        else :
            return 0
    def recommendation_by_sentence2(self, keyword):
        okt = Okt()
        sentence = keyword
        review = re.sub('[^가-힣 ]', ' ', sentence)
        #
        token = okt.pos(review, stem=True)
        #
        df_token = pd.DataFrame(token, columns=['word', 'class'])
        df_token = df_token[(df_token['class'] == 'Noun') |
                            (df_token['class'] == 'Verb') |
                            (df_token['class'] == 'Adjective')]
        words = []
        for word in df_token.word:
            if 1 < len(word):
                words.append(word)
        cleaned_sentence = ' '.join(words)
        print(cleaned_sentence)
        sentence_vec = self.Tfidf2.transform([cleaned_sentence])
        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix2)
        recommendation2 = self.getRecommendation2(cosine_sim)
        kinds = '문장으로 추천된 게임들 입니다.\n'
        recommendation2 = '\n'.join([kinds] + list(recommendation2[1:]))

        return recommendation2

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())