from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pytest

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_nexign(driver):
    try:
        driver.get("https://nexign.com/ru")
        time.sleep(2)  # Даем странице время для загрузки

        # Ожидание появления элемента "Продукты и решения"
        wait = WebDriverWait(driver, 10)
        products_section = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Продукты и решения')]")))

        # Наведение курсора на элемент
        ActionChains(driver).move_to_element(products_section).perform()
        time.sleep(1)  # Даем время для раскрытия меню

        # Клик на элемент "Продукты и решения"
        products_section.click()
        time.sleep(2)

        # Шаг 3: Перейти в раздел «Инструменты для ИТ-команд»
        it_tools_section = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Инструменты для ИТ-команд')]")))
        it_tools_section.click()
        time.sleep(2)

        # Шаг 4: Перейти в раздел "Nexign Nord"
        nexign_nord_section = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Nexign Nord')]")))
        nexign_nord_section.click()
        time.sleep(2)

        # Подтверждение успешного выполнения теста
        print("Тест успешно пройден: все шаги выполнены.")

    except Exception as e:
        pytest.fail(f"Тест завершился с ошибкой: {e}")