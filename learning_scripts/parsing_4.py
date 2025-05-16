import requests
from bs4 import BeautifulSoup

# URL конкретной книги
book_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(book_url)
soup = BeautifulSoup(response.text, 'html.parser')

# 1. Извлекаем описание:
# Находим блок с id="product_description", затем переходим к следующему тегу (параграфу)
description_tag = soup.find('div', id='product_description')
if description_tag:  # Проверяем, найден ли тег
    description = description_tag.find_next_sibling('p').text
else:
    description = "Нет описания"
print("Описание:", description)

# 2. Извлекаем категорию:
# Категория находится в третьем элементе списка breadcrumb (индекс 2)
breadcrumb = soup.find('ul', class_='breadcrumb').find_all('a')
category = breadcrumb[2].text  # Индексы: 0 = Home, 1 = Books, 2 = Poetry...
print("Категория:", category)