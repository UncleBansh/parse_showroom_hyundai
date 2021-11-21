from selenium import webdriver
from telegram import Bot
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
load_dotenv()


def send_message(bot, text):
    bot.send_message(chat_id=user_chat_id, text=text)

user_chat_id = os.environ['USER_CHAT_ID']
token = os.environ['BOT_TOKEN']
CarIsFind = False

# datetime object containing current date and time

bot = Bot(token=token)
bot.send_message(chat_id=user_chat_id, text='bot is working')
while True:
    CarIsFind = False
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = '/usr/bin/google-chrome'
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920,1080')
    browser = webdriver.Chrome(
        executable_path="./chromedriver",
        options=chrome_options)
    browser.get('https://showroom.hyundai.ru/')
    element = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.ID, "cars-all")))
    browser.save_screenshot("screenshot.png")
    soup = BeautifulSoup(browser.page_source, 'lxml')
    cars = soup.find_all(class_='car-item__wrap')
    for car in cars:
        car_brand = car.find(class_='text-uppercase').text
        car_price = car.find(class_='car-item__price-top').text
        car_engine = car.find_all(class_='mt-8')[1].find(class_='title').text
        car_count = car.find_all(class_='text-sm')[3].text
        #car_image = car.find_all(class_='car-item__img asd-bg-fit')
        #print(car_image)
        text = f'''Автомобиль - Hyundai {car_brand}\nЦена - {car_price}\nДвигатель - {car_engine}\n{car_count}\nhttps://showroom.hyundai.ru/'''
        if "TUCSON" in car_brand  or "CRETA" in car_brand or "SOLARIS" in car_brand or "SONATA" in car_brand  or "ELANTRA" in car_brand:
            send_message(bot, text=text)
            bot.send_message(chat_id=242568032, text=text)
            browser.save_screenshot("screenshot2.png")
            print(dt_string,': шото нашлося')
            CarIsFind = True
    
    if CarIsFind == False:
        print(dt_string,': ничаго нету опять')
   
    browser.quit()
    time.sleep(1)

