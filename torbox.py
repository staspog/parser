from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

USER_EMAIL = "your@email.com"
USER_PASSWORD = "your_password"
INN_LIST = [7729657870, 8700000466]  # Список ИНН для обработки

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)

def login():
    try:
        driver.get("https://torgbox.ru/login")
        print("Выполняем авторизацию...")
        
        email_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "email")))
        email_field.send_keys(USER_EMAIL)
        
        driver.find_element(By.ID, "password").send_keys(USER_PASSWORD)
        
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn--secondary') and contains(., 'Войти в аккаунт')]")))
        login_button.click()

        WebDriverWait(driver, 15).until(
            EC.url_contains("torgbox.ru/contragents"))
        print("Авторизация успешно выполнена!")
        
    except Exception as e:
        print(f"Ошибка при авторизации: {str(e)}")

def parse_page():
    # Раскрываем все категории
    buttons = driver.find_elements(By.CSS_SELECTOR, "button.vehicles-category__control")
    for btn in buttons:
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)
    
    # Парсим данные
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    models = soup.find_all('div', class_='vehicles-category__header')
    
    for index, model in enumerate(models, 1):
        model_name = model.find('span').text.strip()
        print(f"\n{index}. Модель: {model_name}")
        
        table = model.find_next('table', class_='vehicles__items')
        if table:
            rows = table.find_all('tr', class_='vehicles__items__item')
            for row in rows:
                cells = row.find_all('td')
                print(f"   - Номер: {cells[0].text.strip()}")
                print(f"     Название: {cells[1].text.strip()}")
                print(f"     Год: {cells[2].text.strip()}")
                print(f"     Дата: {cells[3].text.strip()}\n")

try:
    for inn in INN_LIST:
        current_url = f"https://torgbox.ru/contragents/{inn}/vehicles"
        driver.get(current_url)
        time.sleep(2)
        
        # Проверяем необходимость авторизации
        if "login" in driver.current_url or driver.find_elements(By.CSS_SELECTOR, 'a[href="/login"]'):
            login()
            driver.get(current_url)
        
        # Обрабатываем все страницы пагинации
        page_count = 1
        while True:
            print(f"\n{'='*50}\nИНН: {inn}, Страница: {page_count}\n{'='*50}")
            
            # Ждем загрузки данных
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "vehicles-category__title")))
            
            # Парсим текущую страницу
            parse_page()
            
            # Проверяем наличие следующей страницы
            try:
                next_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.pagination__link--next:not([aria-disabled="true"])')))
                
                # Скроллим и кликаем через JS
                driver.execute_script("arguments[0].scrollIntoView();", next_btn)
                driver.execute_script("arguments[0].click();", next_btn)
                
                # Ждем обновления данных
                WebDriverWait(driver, 20).until(
                    EC.staleness_of(next_btn))
                page_count += 1
                time.sleep(2)
                
            except Exception as e:
                print(f"Больше страниц нет: {str(e)}")
                break

except Exception as e:
    print(f"Произошла ошибка: {str(e)}")

finally:
    driver.quit()