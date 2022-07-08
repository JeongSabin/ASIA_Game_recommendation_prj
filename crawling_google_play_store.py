from selenium import webdriver #브라우저 동작 자동 제어
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup #html/xml문서 parsing
from time import sleep
import random
from tqdm.auto import tqdm, trange #작업 프로세스 바 시각화

options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)

chrome_driver = '../chromedriver'

#구글플레이스토어 링크

#리뷰 모두 보기 button xpath
#//*[@id="yDmH0d"]/c-wiz[3]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/div/div/div[5]/div/div/button/span
rate_review_xpath = '//*[@id="yDmH0d"]/c-wiz[3]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/header/div/div[2]/button/i'

#review xpath pattern
#//*[@id="yDmH0d"]/div[5]/div[2]/div/div/div/div/div[2]/div/div[1]/div[4]/div[1]
#//*[@id="yDmH0d"]/div[5]/div[2]/div/div/div/div/div[2]/div/div[1]/div[3]/div[1]
url = 'https://play.google.com/store/apps/category/GAME?utm_source=apac_med&utm_medium=hasem&utm_content=Nov0220&utm_campaign=Evergreen&pcampaignid=MKT-EDR-apac-kr-1003227-med-hasem-gm-Evergreen-Nov0220-Text_Search_BKWS-BKWS%7cONSEM_kwid_43700058439438694_creativeid_477136209358_device_c&gclid=Cj0KCQjw5ZSWBhCVARIsALERCvxonCacgaNlzSMf-jfx89k40y-3_2WWU9L5fKmu4XlM524HbVUSQpcaAsqAEALw_wcB&gclsrc=aw.ds'

while Flag:
    for i in range(1, ):
        game_button_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[3]/c-wiz/section/div/div/div/div/div[1]/div[{}]/div/div/div/a'.format()


        try:
            driver.get(url)
            time.sleep(0.5)
            driver.find_element('xpath', game_button_xpath).click()
            time.sleep(0.5)


            driver.find_element('xpath', rate_review_xpath).click()
                for
                    review_xpath = '//*[@id="yDmH0d"]/c-wiz[3]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/div/div/div[{}]/div[1]'.format()

def scrolling():
    try:
        last_height = drvier.execute_script('return document.body.scrollHeight')

        while True:
            # pause_time = random.uniform(0.5, 0.8)
            pause_time = 1
            #scroll down button
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(pause_time)

            #무한 스크롤 위해 살짝 위로
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight-50);')
            time.sleep(pause_time)

            #스크롤 높이 새롭게 받아오기
            new_height = driver.execute_script('return documnet.body.scroppHeight')

            if new_height == last_height:
                    break
            last_height = new_height


    except Exception as e:
        print('error occurred: ', e)
