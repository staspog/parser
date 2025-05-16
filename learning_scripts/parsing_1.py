import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

html_code = requests.get(url).text

soup = BeautifulSoup(html_code, 'html.parser')


books = soup.find_all('h3') 

for book in books:
    print(book.text)