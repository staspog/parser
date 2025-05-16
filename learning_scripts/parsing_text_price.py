import requests
from bs4 import BeautifulSoup

# Настройки парсера
base_url = "http://books.toscrape.com/catalogue/page-{}.html"
books_dict = {}  # Словарь для хранения данных
page = 1          # Начинаем с первой страницы

print("Начинаем парсинг книг...")

# Основной цикл парсинга
while page < 5:
    # Формируем URL и получаем страницу
    url = base_url.format(page)
    response = requests.get(url)
    
    # Проверяем существование страницы
    if response.status_code != 200:
        print(f"Достигнут конец списка (страница {page} не существует)")
        break
    
    # Парсим HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    
    # Обрабатываем каждую книгу на странице
    for book in books:
        try:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            books_dict[title] = price
        except Exception as e:
            print(f"Ошибка при обработке книги: {e}")
            continue
    
    print(f"Обработана страница {page}")
    page += 1  # Переходим к следующей странице

# Выводим результаты
print("\nРезультаты парсинга:")
for title, price in books_dict.items():
    print(f"• {title}: {price}")

print(f"\nВсего найдено книг: {len(books_dict)}")
print("Парсинг завершён!")