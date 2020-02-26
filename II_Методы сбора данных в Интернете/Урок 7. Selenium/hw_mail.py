from selenium import webdriver
from pymongo import MongoClient
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome()
driver.get('https://mail.ru/')
assert 'Mail.ru: почта,' in driver.title

# авторизация
login = 'study.ai_172@mail.ru'
password = 'NewPassword172'
input = driver.find_element_by_id('mailbox:login')
input.send_keys(login)
button = driver.find_element_by_css_selector('input.o-control')
button.click()
input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'mailbox:password')))
input.send_keys(password)
button.click()

links = []

client = MongoClient('localhost', 27017)
db = client.mail_ru

while True:
	letters = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.js-letter-list-item")))

	letters_count = len(links)

	for letter in letters:
		links.append(letter.get_attribute('href'))
		link = letter.get_attribute('href')
		author = letter.find_element_by_class_name('ll-crpt').text
		theme = letter.find_element_by_class_name('ll-sj__normal').text

		if link:
			db['mailru'].insert_one({'link': link, 'author': author, 'theme': theme})

	links = list(set(links))

	if letters_count == len(links):
		break

	actions = ActionChains(driver)
	actions.move_to_element(letters[-1])
	actions.perform()

driver.quit()





