from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

USER_EMAIL = "your@email.com"
USER_PASSWORD = "your_password"

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)

all_data = []
last = 16

try:
    # Читаем файл, предполагая что первая строка - заголовок
    df = pd.read_excel('INN.xlsx', engine='openpyxl')
    
    # Получаем первые 15 ИНН начиная со второй строки (индексы 1-15)
    INN_LIST = df.iloc[1:last, 0].dropna().tolist()  # [1:16] - строки с 1 по 15 включительно
    
    # Проверяем, что список не пустой
    if not INN_LIST:
        raise ValueError("Не найдено ни одного ИНН в указанном диапазоне")
    
    print("Первые 15 ИНН со второй строки:")
    for i, inn in enumerate(INN_LIST, 1):
        print(f"{i}. {inn}")

except FileNotFoundError:
    print("Ошибка: файл INN.xlsx не найден!")
except Exception as e:
    print(f"Произошла ошибка: {str(e)}")

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

def parse_page(inn):
    # Раскрываем все категории
    buttons = driver.find_elements(By.CSS_SELECTOR, "button.vehicles-category__control")
    for btn in buttons:
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)
    
    # Парсим данные
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    models = soup.find_all('div', class_='vehicles-category__header')
    
    for model in models:
        model_name = model.find('span').text.strip()
        
        table = model.find_next('table', class_='vehicles__items')
        if table:
            rows = table.find_all('tr', class_='vehicles__items__item')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 4:
                    car_data = {
                        'ИНН': inn,
                        'Модель': model_name,
                        'Автомобиль': cells[1].text.strip(),
                        'Год': cells[2].text.strip(),
                        'Дата': cells[3].text.strip()
                    }
                    all_data.append(car_data)

try:
    for inn in INN_LIST:
        try:  # Добавляем внутренний try-except для каждого ИНН
            current_url = f"https://torgbox.ru/contragents/{inn}/vehicles"
            driver.get(current_url)
            time.sleep(2)
            
            # Проверка на необходимость авторизации
            if "login" in driver.current_url or driver.find_elements(By.CSS_SELECTOR, 'a[href="/login"]'):
                login()
                driver.get(current_url)
            
            # Проверка наличия контента на странице
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "vehicles-category__title")))
            except:
                print(f"На странице ИНН {inn} не найдено контента. Пропускаем.")
                continue  # Переходим к следующему ИНН

            page_count = 1
            while True:
                print(f"Обрабатываем ИНН {inn}, страница {page_count}")
                
                # Дополнительная проверка перед парсингом
                if not driver.find_elements(By.CLASS_NAME, "vehicles-category__title"):
                    print(f"Контент исчез после загрузки. Пропускаем ИНН {inn}")
                    break
                
                parse_page(inn)
                
                try:
                    next_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.pagination__link--next:not([aria-disabled="true"])')))
                    
                    driver.execute_script("arguments[0].scrollIntoView();", next_btn)
                    driver.execute_script("arguments[0].click();", next_btn)
                    
                    WebDriverWait(driver, 20).until(
                        EC.staleness_of(next_btn))
                    page_count += 1
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Больше страниц нет: {str(e)}")
                    break

        except Exception as e:  # Ловим все ошибки для текущего ИНН
            print(f"Ошибка при обработке ИНН {inn}: {str(e)}. Пропускаем.")
            continue  # Переходим к следующему ИНН

    # Сохраняем все данные в Excel
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_excel('parsed_data.xlsx', index=False)
        print("\nДанные сохранены в parsed_data.xlsx")

except Exception as e:
    print(f"Произошла критическая ошибка: {str(e)}")

finally:
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_excel('parsed_data.xlsx', index=False)
        print("\nДанные сохранены в parsed_data.xlsx")
    driver.quit()