import requests
from bs4 import BeautifulSoup
import csv
import time

# Настройки парсера
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

print('Введите число страниц, которое хотите спарсить')
pages = int(input())
print("Начинаем парсинг книг...")

# Открываем CSV файл для записи
with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Title', 'Price', 'Rating', 'Availability'])
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
            # Парсим название
            title = book.h3.a['title']
            
            # Парсим цену
            price_text = book.find('p', class_='price_color').get_text(strip=True)
            price = float(price_text.replace('Â£', ''))            
            # Парсим рейтинг
            rating_tag = book.find('p', class_='star-rating')
            rating_classes = rating_tag['class']
            rating = {'One': 1, 'Two': 2, 'Three': 3, 
                      'Four': 4, 'Five': 5}.get(rating_classes[1], 0)
            
            # Парсим наличие
            availability = book.find('p', class_='instock availability').get_text(strip=True)
            
            # Записываем данные напрямую в CSV
            writer.writerow({
                'Title': title,
                'Price': price,
                'Rating': rating,
                'Availability': availability
            })
        print(f"Обработана страница {page}")

# Выводим статистику
print("\nРезультаты парсинга:")
print("Данные сохранены в файл books.csv")
print("Парсинг завершён!")