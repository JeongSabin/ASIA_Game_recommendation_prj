import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver import ActionChains
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random


options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver', options=options)

url = 'https://play.google.com/store/games'  # 구글플레이 게임 주소

actions = ActionChains(driver)  # ActionChains 받아오기
wait = WebDriverWait(driver, 5)
driver.get(url)

# 두번째 카테고리의 첫번째 게임 제목 Xpath
# //*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[2]/c-wiz/section/div/div/div/div/div[1]/div[1]/div/div/div/a/div[2]/div/div[1]/span
# 세번째 카테고리의 두번째 게임 제목 Xpath
# //*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[3]/c-wiz/section/div/div/div/div/div[1]/div[2]/div/div/div/a/div[2]/div/div[1]/span

# 평가 및 리뷰 Xpath
# //*[@id="yDmH0d"]/c-wiz[3]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/header/div/div[2]/button/i

# 첫번째 리뷰 Text Xpath
# //*[@id="yDmH0d"]/div[5]/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/div[1]
# 두번째 리뷰 Text Xpath
# //*[@id="yDmH0d"]/div[5]/div[2]/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]

# 무한 스크롤 함수 + 크롤링
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# 리뷰랑 게임 제목 리스트
games = []
reviews = []

# 카테고리 번호
category_cnt = 2
category_flag = True
while category_flag:  # 카테고리 번호 순서대로 크롤링
    try:
        category_cnt += 1
        game_cnt = 0
        game_flag = True

        while game_flag:
            try:
                game_cnt += 1
                #             //*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[3]/c-wiz/section/div/div/div/div/div[1]/div[1]/div/div/div/a/div[2]/div/div[1]/span
                game_path = f'//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[{category_cnt}]/c-wiz/section/div/div/div/div/div[1]/div[{game_cnt}]/div/div/div/a/div[2]/div/div[1]/span'
                try:
                    game_title = driver.find_element('xpath', game_path).text
                except:
                    game_cnt += 1
                    game_path = f'//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[{category_cnt}]/c-wiz/section/div/div/div/div/div[1]/div[{game_cnt}]/div/div/div/a/div[2]/div/div[1]/span'
                    game_title = driver.find_element('xpath', game_path).text
                try:
                    driver.find_element('xpath', game_path).click()
                except:
                    pass
                # 화면 맨 밑으로 휠 내리기
                time.sleep(0.3)
                for i in range(100):
                    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(0.3)

                # 리뷰 더 보기 버튼 클릭
                print('debug01')
                print(driver.window_handles)

                driver.find_element('xpath',
                    '//*[@id="yDmH0d"]/c-wiz[3]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/div/div/div[5]/div/div/button').send_keys(Keys.ENTER)
                time.sleep(0.3)
                print('debug03')
                # modal 윈도우로 스위칭
                print(driver.window_handles)

                print('debug04')
                crawling_flag = True
                crawling_cnt = 0

                # 크롤링
                try:
                    while crawling_flag:
                        crawling_cnt += 1
                        driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[5]/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                        # 리뷰 긁기
                        try:
                            review_xpath = f'//*[@id="yDmH0d"]/div[5]/div[2]/div/div/div/div/div[2]/div/div[1]/div[{crawling_cnt}]/div[1]'
                            review = driver.find_element('xpath', review_xpath).text
                            if len(review) > 30:
                                reviews.append(review)
                                print(review)
                                print(crawling_cnt)
                                print()
                        except:
                            mouse_on = driver.find_element_by_xpath(
                                f'//*[@id="yDmH0d"]/div[5]/div[2]/div/div/div/div/div[2]')
                            print('debug0')
                            actions.move_to_element(mouse_on).perform()

                            # 페이지 하단으로 스크롤
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                            # 페이지 로딩 대기
                            time.sleep(SCROLL_PAUSE_TIME)

                            # 이전 페이지 하단 좌표와 현재 페이지 하단 좌표 비교
                            new_height = driver.execute_script("return document.body.scrollHeight")
                            if new_height == last_height:
                                driver.back()
                                driver.back()
                                break
                            last_height = new_height
                except NoSuchElementException:
                    crawling_flag = False


            except NoSuchElementException:
                try:
                    # 마우스 올리기
                    mouse_on = driver.find_element('xpath',
                        f'//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[{category_cnt}]/c-wiz/section/div/div/div/div/div[1]/div[1]/div/div/div')
                    print('debug0')
                    actions.move_to_element(mouse_on).perform()
                    driver.find_element('xpath',
                        '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[2]/c-wiz/section/div/div/div/div/div[2]/button/span[2]/i').click()
                    time.sleep(0.4)
                except NoSuchElementException:
                    category_flag = False
                    print('다음 카테고리 크롤링으로 넘어갑니다')

        df = pd.DataFrame({'game': games, 'review': reviews})
        df.to_csv(f'./crawling_data/reviews_category_{category_cnt}.csv', index=False)
    except NoSuchElementException:
        category_flag = False
        print('크롤링을 종료합니다')