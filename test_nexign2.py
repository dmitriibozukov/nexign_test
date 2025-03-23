from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pytest
import time

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()  # Открыть браузер на весь экран
    yield driver
    driver.quit()

def test_count_nexign_mentions(driver):
    try:
        driver.get("https://nexign.com/ru")
        time.sleep(2)

        nexiqn_mentions = set()

        span_elements = driver.find_elements(By.TAG_NAME, "span")
        for span in span_elements:
            try:
                if span.is_displayed():
                    span.click()
                    time.sleep(0.5)
            except Exception:
                continue

        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        mentions = [m.start() for m in re.finditer(r'\bnexign\b', page_text)]
        for pos in mentions:
            start = max(0, pos - 15)
            end = min(len(page_text), pos + len("nexign") + 15)
            context = page_text[start:end]
            nexiqn_mentions.add(context)

        link_elements = driver.find_elements(By.TAG_NAME, "a")
        for link in link_elements:
            try:
                if link.is_displayed():
                    link_text = link.text.lower()
                    if "nexign" in link_text:
                        nexiqn_mentions.add(link_text)
            except Exception:
                continue

        print(f"Количество уникальных упоминаний слова 'Nexign': {len(nexiqn_mentions)}")
        for context in nexiqn_mentions:
            print(f"Контекст: {context}")

        assert len(nexiqn_mentions) > 0, "Слово 'Nexign' не найдено на странице"

    except Exception as e:
        pytest.fail(f"Тест завершился с ошибкой: {e}")