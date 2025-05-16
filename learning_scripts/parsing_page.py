import requests
from bs4 import BeautifulSoup

# Базовый URL страниц ({} заменится на номер страницы)
base_url = "http://books.toscrape.com/catalogue/page-{}.html"

# Перебираем страницы от 1 до 2
for page_num in range(1, 3):
    # Формируем URL для текущей страницы
    current_url = base_url.format(page_num)
    
    # Отправляем запрос
    response = requests.get(current_url)
    
    # Парсим HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ищем все заголовки книг
    books = soup.find_all('h3')
    
    # Извлекаем названия
    print(f"Страница {page_num}:")
    for book in books:
        print(book.a['title'])