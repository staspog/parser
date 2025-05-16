import time

from selenium import webdriver #сам селениум и веб-драйвер
from webdriver_manager.chrome import ChromeDriverManager #хром драйвер
from selenium.webdriver.chrome.service import Service #отвечает за автоматическую установку, открытие и закрытие
from selenium.webdriver.common.by import By

service = Service(executable_path=ChromeDriverManager().install()) #при помощи менеджера устаналиваем драйвер и устаналиваем параметры
driver = webdriver.Chrome(service=service) #создаём веб драйвер для selenium, с которым будет работать питон

driver.get("https://quotes.toscrape.com/")
time.sleep(10)


search_input = driver.find_element(By.CLASS_NAME, "form-control")
search_input.send_keys("life")
search_button = driver.find_element(By.CSS_SELECTOR, "input.btn")
search_button.click()
first_quote = driver.find_element(By.CLASS_NAME, "quote").text
print(first_quote)