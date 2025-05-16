import requests
from bs4 import BeautifulSoup

response = requests.get("http://books.toscrape.com/")
soup = BeautifulSoup(response.text, 'html.parser')

# Ищем все теги <p> с классом 'price_color'
prices = soup.find_all('p', class_='price_color')

for price in prices:
    # Извлекаем текст внутри тега (например, £51.77)
    print(price.text)