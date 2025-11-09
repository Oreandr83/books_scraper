Описание проекта:

books_scraper — это парсер сайта Books to Scrape,
который автоматически собирает информацию о книгах: название, цену, наличие, рейтинг, описание и характеристики товара.


Программа выполняет следующие действия:

-Получает данные о книгах с сайта Books to Scrape
-Автоматически обходит все страницы каталога
-Сохраняет собранные данные в текстовый файл artifacts/books_data.txt
-Может запускаться по расписанию (ежедневно в 19:00)

Основные функции:

get_book_data(book_url: str) -> dict

Извлекает информацию о книге:
название (title)
цена (price)
наличие (availability)
рейтинг (rating)
описание (description)
таблица характеристик (product_information)

scrape_books(is_save: bool = False)

Собирает данные со всех страниц каталога.
Если is_save=True, сохраняет результат в artifacts/books_data.txt.

def check_book(): 

Функция проверяет обновление данных о книге на сайте 
http://books.toscrape.com каждый день в 19.00
и записывает данные об этой книге в books_data.txt

Тестирование

Тесты находятся в папке tests/test_scraper.py.
Для запуска тестов в терминале нужно запустить:
pytest
 
Тесты проверяют:

get_book_data возвращает словарь

в функции get_book_data поле title непустое 

функция scrape_books возвращает список

Структура проекта:

books_scraper/

├── artifacts/
│   └── books_data.txt

├── notebooks/
│   └── HW_03_python_ds_2025.ipynb

├── scraper.py

├── README.md

├── tests/
│   └── test_scraper.py

├── .gitignore

└── requirements.txt


Используемые библиотеки:

import time

import requests

import schedule

from bs4 import BeautifulSoup

import os

import sys

import pytest

Обновлено 09.11.2025


