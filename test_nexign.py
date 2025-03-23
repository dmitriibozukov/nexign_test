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
    driver.maximize_window()  # Открыть браузер на весь экран
    yield driver
    driver.quit()

def test_nexign(driver):
    try:
        driver.get("https://nexign.com/ru")
        time.sleep(2)

        wait = WebDriverWait(driver, 10)
        products_section = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Продукты и решения')]")))

        ActionChains(driver).move_to_element(products_section).perform()
        time.sleep(1)

        products_section.click()
        time.sleep(2)

        it_tools_section = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Инструменты для ИТ-команд')]")))
        it_tools_section.click()
        time.sleep(2)

        nexign_nord_section = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Nexign Nord')]")))
        nexign_nord_section.click()
        time.sleep(2)

        print("Тест успешно пройден: все шаги выполнены.")

    except Exception as e:
        pytest.fail(f"Тест завершился с ошибкой: {e}")