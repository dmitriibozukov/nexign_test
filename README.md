
# Проект: Автоматизация тестирования веб-страницы Nexign

Этот проект содержит тесты для автоматизации взаимодействия с веб-страницей [Nexign](https://nexign.com/ru) с использованием Selenium. Тесты проверяют навигацию по сайту, подсчитывают упоминания слова "Nexign" и проверяют орфографию на страницах.

---

## Установка зависимостей


Перед запуском тестов установите необходимые библиотеки:

pip install selenium pytest 

pip install pytest

pip install selenium

pip install pymorphy2

pip install pyspellchecker

pip install webdriver-manager


## Запуск тестов

Запуск через PyCharm

Откройте файл с тестом (например, test_nexign.py).

Нажмите правой кнопкой мыши в редакторе кода и выберите Run 'test_nexign'.

Тест начнет выполняться, и вы увидите вывод в консоли PyCharm.

Результаты 1 задания  

![Screenshot_3](https://github.com/user-attachments/assets/89992bd4-d1c9-470d-b58e-f5ab134a22b6)

Результаты 2 задания 
![Screenshot_2](https://github.com/user-attachments/assets/590ebc7c-5f28-4b65-a13a-3dd0ae010cea)

Результаты 3 задания

(Для третьего задания были выбраны pymorphy2 и SpellChecker. Они не включают орфографию всех слов. Поэтому были добавлены исключения в виде сокращений, названий, аббревиатур, которые встречаются чаще всего и широко известны. Остались термины, которые по моему мнению должны пройти ручную проверку)

![Screenshot_4](https://github.com/user-attachments/assets/b0150195-accd-4d9a-a55a-368b00df80c6)

