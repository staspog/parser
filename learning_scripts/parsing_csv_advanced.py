import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from urllib.parse import urljoin

# Настройки парсера
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

print('Введите число страниц, которое хотите спарсить')
pages = int(input())
print("Начинаем парсинг книг...")

# Открываем CSV файл для записи
with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['Title', 'Price', 'Rating', 'UPC', 'Availability', 'Quantity']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Основной цикл парсинга
    for page in range(1, pages + 1):
        url = base_url.format(page)
        time.sleep(1)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        
        # Обрабатываем каждую книгу
        for book in books:
            # Парсим основную информацию
            title = book.h3.a['title']
            price_text = book.find('p', class_='price_color').get_text(strip=True)
            price = float(price_text.replace('Â£', ''))
            
            # Получаем ссылку на страницу книги
            book_relative_url = book.h3.a['href']
            book_full_url = urljoin(response.url, book_relative_url)
            
            # Парсим дополнительные данные
            time.sleep(1)
            book_response = requests.get(book_full_url)
            soup_book = BeautifulSoup(book_response.text, 'html.parser')
            
            # Парсим UPC
            table = soup_book.find('table', class_='table')

            upc_th = table.find('th', string = 'UPC')
            upc = upc_th.find_next_sibling('td').text
            
            # Парсим наличие и количество
            availability_tag = soup_book.find('p', class_='instock availability')
            availability_text = availability_tag.text.strip()
            availability = availability_text.split('(')[0].strip()
            quantity_match = re.search(r'\d+', availability_text)
            quantity = quantity_match.group()
            
            # Парсим рейтинг
            rating_tag = book.find('p', class_='star-rating')
            rating_classes = rating_tag['class']
            rating = {'One': 1, 'Two': 2, 'Three': 3, 
                      'Four': 4, 'Five': 5}.get(rating_classes[1], 0)
            
            # Записываем данные
            writer.writerow({
                'Title': title,
                'Price': price,
                'Rating': rating,
                'UPC': upc,
                'Availability': availability,
                'Quantity': quantity
            })
        print(f"Обработана страница {page}")

print("\nРезультаты парсинга:")
print("Данные сохранены в файл books.csv")
print("Парсинг завершён!")