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

url = 'https://play.google.com/store/apps/details?id=com.hybeim.intheseom' # 구글플레이 게임 주소

actions = ActionChains(driver) # ActionChains 받아오기
wait = WebDriverWait(driver, 5)
driver.get(url)

