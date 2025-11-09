import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pytest

from scraper import get_book_data, scrape_books

def test_dict():
    """Проверю, что get_book_data возвращает словарь"""
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    result = get_book_data(url)
    assert isinstance(result, dict)


def test_title():
    """Проверю, что поле title непустое"""
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    result = get_book_data(url)
    assert "title" in result
    assert result["title"] != ""



def test_list():
    """Проверю что scrape_books возвращает список"""
    books = scrape_books()
    assert isinstance(books, list)
    assert len(books) > 0
