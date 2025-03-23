from selenium import webdriver
from selenium.webdriver.common.by import By
import pymorphy2
from spellchecker import SpellChecker
import time
import pytest

# Инициализация морфологического анализатора для русского языка
morph_ru = pymorphy2.MorphAnalyzer()

# Инициализация SpellChecker для английского языка
spell_en = SpellChecker(language='en')

# Список исключений (широко известные слова, технические термины, аббревиатуры)
EXCEPTIONS = {
    "nexign", "pdf", "iso", "iec", "tuv", "bss", "iot", "pcrf", "pcf", "aaa", "udr", "rcaf", "dra", "scp", "nrf",
    "scef", "hrm", "kpi", "api", "postgresql", "sql", "tps", "cpu", "pgvector", "sdk", "highload",
    "autodeploy", "astra", "alt", "redhat", "centos", "xeon", "ghz", "ora", "pg", "nord"
}

# Функция для проверки орфографии
def check_spelling(text):
    errors = []
    words = text.split()
    for word in words:
        # Приводим слово к нижнему регистру и убираем знаки препинания
        cleaned_word = ''.join(filter(str.isalpha, word)).lower()
        if cleaned_word:  # Проверяем, что слово не пустое
            # Если слово в списке исключений, пропускаем его
            if cleaned_word in EXCEPTIONS:
                continue
            # Если слово состоит только из латинских букв, проверяем его через английский словарь
            if cleaned_word.isascii():
                if not spell_en.known([cleaned_word]):
                    errors.append(word)  # Сохраняем слово с ошибкой
            else:
                # Если слово содержит кириллицу, проверяем его через pymorphy2
                parsed_word = morph_ru.parse(cleaned_word)[0]
                if parsed_word.tag.POS is None:  # Если слово не распознано
                    errors.append(word)  # Сохраняем слово с ошибкой
    return errors

# Фикстура для инициализации и завершения работы драйвера
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()  # Инициализация драйвера (например, для Chrome)
    yield driver
    driver.quit()  # Закрытие браузера после завершения теста

# Тестовая функция
def test_spelling_check(driver):
    # Множество для хранения посещенных URL
    visited_urls = set()

    # Словарь для хранения ошибок: {url: [список ошибок]}
    errors_dict = {}

    try:
        # Начинаем с главной страницы
        main_url = "https://nexign.com/ru"
        driver.get(main_url)
        time.sleep(2)  # Даем странице время для загрузки

        # Проверка орфографии на главной странице
        main_page_text = driver.find_element(By.TAG_NAME, "body").text
        errors = check_spelling(main_page_text)
        if errors:
            errors_dict[main_url] = errors

        # Сбор ссылок с главной страницы
        links = [link.get_attribute("href") for link in driver.find_elements(By.TAG_NAME, "a") if link.get_attribute("href")]
        links = [link for link in links if link.startswith("https://nexign.com/ru")]
        links = list(set(links))  # Убираем дубликаты

        # Проверка орфографии на первых 10 страницах
        for link in links[:10]:
            if link not in visited_urls:
                driver.get(link)
                time.sleep(2)  # Даем странице время для загрузки
                page_text = driver.find_element(By.TAG_NAME, "body").text
                errors = check_spelling(page_text)
                if errors:
                    errors_dict[link] = errors
                visited_urls.add(link)

        # Вывод результатов
        if errors_dict:
            print("Найдены ошибки орфографии:")
            for url, errors in errors_dict.items():
                print(f"Страница: {url}")
                for error in errors:
                    print(error)
                print("-" * 50)
        else:
            print("Ошибок орфографии не найдено.")

    except Exception as e:
        pytest.fail(f"Тест завершился с ошибкой: {e}")

# Запуск теста
if __name__ == "__main__":
    pytest.main()