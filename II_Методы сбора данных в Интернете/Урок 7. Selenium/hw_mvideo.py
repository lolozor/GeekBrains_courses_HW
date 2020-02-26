from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from hashlib import sha1
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def insert_data(carousel):

    client = MongoClient('localhost', 27017)
    db = client.mvideo270

    goods = carousel.find_elements_by_class_name('gallery-list-item')

    for good in goods:
        title = good.find_element_by_class_name('sel-product-tile-title').text
        price = good.find_element_by_class_name('c-pdp-price__current').text
        if title:
            db['hits'].insert_one({'title': title,
                                   'price': price
                                   })
            # print(title, price)


chrome_options = Options()
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')

try: # закрываем всплывающее окно с супер-предложением
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it("fl-306642"))
    driver.find_element_by_class_name("close").click()
    driver.switch_to.default_content()
except:
    print('Всплывающеее окно не найдено')


hits = driver.find_element_by_xpath('//div[contains(text(), "Хиты продаж")]/../../..')
ActionChains(driver).move_to_element(hits).perform()

insert_data(hits)

next_btn = hits.find_element_by_xpath('//div[contains(text(), "Хиты продаж")]/../../..//a[contains(@class, "next-btn")]')

while next_btn.is_displayed(): # пока доступна кнопка прокрутки - кликаем по ней
    next_btn.click()
    time.sleep(2)
    insert_data(hits)

driver.quit()