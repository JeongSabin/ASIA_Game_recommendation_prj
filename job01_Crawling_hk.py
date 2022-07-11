from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
import warnings
from selenium.webdriver.common.keys import Keys
import datetime

options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)

warnings.filterwarnings('ignore')

title_list = []
review_list = []

for i in range(91,101):
    driver.get('https://store.steampowered.com/?l=koreana')
    time.sleep(1)
    driver.find_element("link text", '신규 및 특집').click()
    time.sleep(1)
    driver.find_element("link text", '최고 인기 제품').click()
    time.sleep(1)
    for f in range(15) :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
    try:
        driver.find_element("css selector", '#search_resultsRows > a:nth-child({}) > div.responsive_search_name_combined > div.col.search_name.ellipsis > span'.format(i)).click()
        time.sleep(1)
    except :
        continue
    try :
        title = driver.find_element("xpath", '//*[@id="appHubAppName"]').text
        time.sleep(1)
    except :
        continue

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:  # 페이지 끝까지 다운
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        time.sleep(1)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    try :
        driver.find_element("css selector", '#ViewAllReviewssummary > a').click()
        time.sleep(1)
    except :
        continue
    try :
        driver.find_element('xpath', '/html/body/div[1]/div[7]/div[9]/div/div[1]/label').click()
        driver.find_element('xpath', '//*[@id="age_gate_btn_continue"]/span').click()
        time.sleep(1)
    except :
        pass

    driver.find_element("xpath", '//*[@id="filterlanguage_activeday"]').click()
    time.sleep(1)
    driver.find_element("xpath", '//*[@id="filterlanguage_option_5"]').click()
    time.sleep(1)

    def doScrollDown(Seconds):
        start = datetime.datetime.now()
        end = start + datetime.timedelta(seconds=Seconds)
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(0.1)
            if datetime.datetime.now() > end:
                break

    doScrollDown(100)

    elements = driver.find_elements("css selector", '.apphub_CardTextContent')

    for j in range(0, len(elements)):
        title_list.append(title)
        review_list.append(elements[j].text)

    print('rank=', i)

df = pd.DataFrame({'title': title_list, 'reviews': review_list})
df.to_csv('./reviews/reviews_91_101.csv', index=False)