from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pytest
import time

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()  # Закрытие браузера после завершения теста

def test_count_nexign_mentions(driver):
    try:
        # Шаг 1: Открыть главную страницу сайта
        driver.get("https://nexign.com/ru")
        time.sleep(2)  # Даем странице время для загрузки

        # Множество для хранения уникальных упоминаний слова "Nexign"
        nexiqn_mentions = set()

        # Шаг 2: Найти все видимые элементы <span> и кликнуть по ним один раз
        span_elements = driver.find_elements(By.TAG_NAME, "span")

        for span in span_elements:
            try:
                # Проверяем, видим ли элемент
                if span.is_displayed():
                    # Клик по элементу <span>
                    span.click()
                    time.sleep(0.5)  # Даем время для обновления контента
            except Exception as e:
                # Если элемент нельзя кликнуть, пропускаем его
                continue

        # Шаг 3: Получить весь видимый текст страницы и привести его к нижнему регистру
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()

        # Шаг 4: Найти все упоминания слова "nexign" в видимом тексте
        mentions = [m.start() for m in re.finditer(r'\bnexign\b', page_text)]
        for pos in mentions:
            # Добавляем контекст: 15 символов слева и справа или меньше, если символов недостаточно
            start = max(0, pos - 15)
            end = min(len(page_text), pos + len("nexign") + 15)
            context = page_text[start:end]
            nexiqn_mentions.add(context)  # Уникальный ключ: контекст

        # Шаг 5: Найти все видимые ссылки (<a>) и проверить их текст
        link_elements = driver.find_elements(By.TAG_NAME, "a")

        for link in link_elements:
            try:
                # Проверяем, видим ли элемент
                if link.is_displayed():
                    # Получить текст ссылки
                    link_text = link.text.lower()

                    # Поиск слова "nexign" в тексте ссылки
                    if "nexign" in link_text:
                        # Добавляем контекст: весь текст ссылки
                        nexiqn_mentions.add(link_text)  # Уникальный ключ: текст ссылки
            except Exception as e:
                # Если что-то пошло не так, пропускаем ссылку
                continue

        # Шаг 6: Вывести количество уникальных упоминаний слова "Nexign"
        print(f"Количество уникальных упоминаний слова 'Nexign': {len(nexiqn_mentions)}")

        # Шаг 7: Вывести контекст для каждого найденного слова
        for context in nexiqn_mentions:
            print(f"Контекст: {context}")

        # Проверка, что количество упоминаний больше 0 (пример проверки)
        assert len(nexiqn_mentions) > 0, "Слово 'Nexign' не найдено на странице"

    except Exception as e:
        pytest.fail(f"Тест завершился с ошибкой: {e}")