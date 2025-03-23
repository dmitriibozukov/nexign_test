from selenium import webdriver
from selenium.webdriver.common.by import By
import pymorphy2
from spellchecker import SpellChecker
import time
import pytest

morph_ru = pymorphy2.MorphAnalyzer()
spell_en = SpellChecker(language='en')

EXCEPTIONS = {
    "nexign", "pdf", "iso", "iec", "tuv", "bss", "iot", "pcrf", "pcf", "aaa", "udr", "rcaf", "dra", "scp", "nrf",
    "scef", "hrm", "kpi", "api", "postgresql", "sql", "tps", "cpu", "pgvector", "sdk", "highload",
    "autodeploy", "astra", "alt", "redhat", "centos", "xeon", "ghz", "ora", "pg", "nord"
}

def check_spelling(text):
    errors = []
    words = text.split()
    for word in words:
        cleaned_word = ''.join(filter(str.isalpha, word)).lower()
        if cleaned_word:
            if cleaned_word in EXCEPTIONS:
                continue
            if cleaned_word.isascii():
                if not spell_en.known([cleaned_word]):
                    errors.append(word)
            else:
                parsed_word = morph_ru.parse(cleaned_word)[0]
                if parsed_word.tag.POS is None:
                    errors.append(word)
    return errors

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()  # Открыть браузер на весь экран
    yield driver
    driver.quit()

def test_spelling_check(driver):
    visited_urls = set()
    errors_dict = {}

    try:
        main_url = "https://nexign.com/ru"
        driver.get(main_url)
        time.sleep(2)

        main_page_text = driver.find_element(By.TAG_NAME, "body").text
        errors = check_spelling(main_page_text)
        if errors:
            errors_dict[main_url] = errors

        links = [link.get_attribute("href") for link in driver.find_elements(By.TAG_NAME, "a") if link.get_attribute("href")]
        links = [link for link in links if link.startswith("https://nexign.com/ru")]
        links = list(set(links))

        for link in links[:10]:
            if link not in visited_urls:
                driver.get(link)
                time.sleep(2)
                page_text = driver.find_element(By.TAG_NAME, "body").text
                errors = check_spelling(page_text)
                if errors:
                    errors_dict[link] = errors
                visited_urls.add(link)

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

if __name__ == "__main__":
    pytest.main()