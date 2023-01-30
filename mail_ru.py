from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import account_data
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from pprint import pprint

# Вариант I
# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о
# письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: Password172!@#
# Если тестовый почтовый ящик не работает, то нужно создать свой почтовый ящик
# и переслать на него минимум любых рекламных 50 сообщений.

# Запуск сеанса
s = Service('./chromedriver.exe')

driver = webdriver.Chrome(service=s)
driver.implicitly_wait(10)

driver.maximize_window()
driver.get('https://e.mail.ru/newsletters/')

# Ввод логина
login = driver.find_element(By.XPATH, '//input[@name="username"]')
login.send_keys(account_data.mail_login)
login.send_keys(Keys.ENTER)

# Ввод пароля
password = driver.find_element(By.XPATH, '//input[@name="password"]')
password.send_keys(account_data.mail_pass)
password.send_keys(Keys.ENTER)

# Создаём словарь писем формата ссылка - это ключ, а остальная информация хранится в значении в виде словаря
letters_dict = dict()
while True:
    # получаем список писем, показанных сервером
    letters = driver.find_elements(By.CLASS_NAME, 'llc')
    # Если последнее письмо в нашем словаре, то мы просмотрели все письма
    if letters[-1].get_attribute('href') in letters_dict:
        break
    # пробегаемся по письмам, чтобы собрать инфйормацию
    for letter in letters:
        # ссылка на письмо
        letter_link = letter.get_attribute('href')
        # Если письмо уже в нашем словарем, то мы его не трогаем
        if letter_link not in letters_dict:
            # получаем от кого письмо, тему и дату, текст оставляем пустым
            letter_from = letter.find_element(By.CLASS_NAME, 'll-crpt').text
            letter_subject = letter.find_element(By.CLASS_NAME, 'll-sj__normal').text
            letter_date = letter.find_element(By.CLASS_NAME, 'llc__item_date').text
            # print(letter_from, letter_subject, letter_date, '\n', letter_link)
            letters_dict[letter_link] = {'from': letter_from, 'subject': letter_subject,
                                         'date': letter_date, 'text': ''}

    # Если писем больше 50, то дальше не парсим, чтобы не перегузить систему
    # if len(letters_dict) > 50:
    #     break
    # перемещаемся к последнему письму, который нам выдал сервер, чтобы увидеть следующие
    action = ActionChains(driver)
    action.move_to_element(letters[-1])
    action.perform()

# Пробегаемся по ссылкам и записываем текст
for link in letters_dict:
    driver.get(link)
    letters_dict[link]['text'] = driver.find_element(By.CLASS_NAME, 'letter__body').text
    letters_dict[link]['link'] = link

# загружаем в Mongo
client = MongoClient()
db = client['db_mailru']

db.letters.drop()
for k, v in letters_dict.items():
    db.letters.insert_one(v)

# проверка
for letter in db.letters.find():
    pprint(letter)