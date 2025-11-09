import requests
from bs4 import BeautifulSoup
import os
import time
import schedule


def get_book_data(book_url: str) -> dict:
    """
    Получает информацию с сайта "Books to Scrape":
    функция загружает страницу книги, парсит HTML с помощью BeautifulSoup
    и извлекает информацию: название, цену, рейтинг, количество в наличии, описание
    и дополнительные характеристики из таблицы Product Information

    Аргументы:
    book_url: URL страницы книги.

    return:
    book_data: cловарь с данными книги:
    title : название книги
    price : цена книги
    availability : количество в наличии
    rating : рейтинг книги
    description : описание книги
    product_information : дополнительные характеристики из таблицы Product Information

    """

    response = requests.get(book_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')


    title_tag = soup.find('title')
    title = title_tag.text.replace(" | Books to Scrape - Sandbox", "").strip()

    price = soup.find('p', class_='price_color').text.strip()

    stock = soup.find('p', class_='instock availability').text.strip()

    rating_tag = soup.find('p', class_='star-rating')
    rating = None
    if rating_tag is not None:
        cl = rating_tag.get('class', [])
    ratings_map = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    for key, value in ratings_map.items():
        if key in cl:
            rating = value
            break

    header = soup.find('div', id = 'product_description')
    if header is not None:
        paragraph = header.find_next_sibling('p')
        if paragraph is not None:
            description = paragraph.text.strip()
        else:
            description = None
    else:
        description = None

    product_info = {}
    table = soup.find('table', class_= 'table table-striped')
    if table is not None:
        rows = table.find_all('tr')
        for row in rows:
            key = row.find('th').text.strip()
            value = row.find('td').text.strip()
            product_info[key] = value

    book_data = {
        'title': title,
        'price': price,
        'availability': stock,
        'rating': rating,
        'description': description,
        'product_information': product_info
    }

    return book_data

book_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
res = get_book_data(book_url)
print(res)


def scrape_books(is_save: bool = False):
    """
    Автоматически скрейпит все книги с сайта books.toscrape.com.

    Функция проходит по всем страницам каталога с книгами,
    собирает данные о каждой книге при помощи функции 'get_book_data'
    и возвращает данные в виде списка словарей.
    Количество страниц в каталоге определяется автоматически,
    останавливаясь, когда книги заканчиваются или страница недоступна.

    Параметры:
    is_save: если True — сохраняет результат в файл books_data.txt

    return:
    список словарей all_books с информацией о каждой книге.
    Каждый словарь содержит:
    title : название книги
    price : цена книги
    availability : количество в наличии
    rating : рейтинг книги
    description : описание книги
    product_information : дополнительные характеристики из таблицы Product Information
    """
    BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
    CATALOGUE_URL = "http://books.toscrape.com/catalogue/"

    all_books = []
    page_num = 1
    max_page = 2

    while True:
        if page_num > max_page:
            break
        page_url = BASE_URL.format(page_num)
        print("Начал проходить по страницам")
        response = requests.get(page_url)

        if response.status_code != 200:
            print("Дошел до последней страницы каталога.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select("h3 > a")

        if not books:
            break


        for book in books:
            rel_url = book.get("href")
            book_url = os.path.join(CATALOGUE_URL, rel_url.replace("../../", ""))
            book_data = get_book_data(book_url)
            all_books.append(book_data)

        page_num += 1  # Перехожу на следующую страницу

    if is_save:
        with open("artifacts/books_data.txt", "w", encoding="utf-8") as f:
            for book in all_books:
                f.write(str(book) + "\n")

    return all_books

res = scrape_books(is_save = True)
print(type(res), len(res))



def check_book():
    """
    Функция проверяет обновление данных о книге на сайте http://books.toscrape.com каждый день в 19.00
    и записывает данные этой книги в books_data.txt
    return: dict
    """

    book_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

    try:
        data = get_book_data(book_url)
    except Exception as e:
        print("Ошибка: ", e)
        return


    # Обновление записываю в файл
    with open("artifacts/books_data.txt", "a", encoding="utf-8") as f:
        f.write(f"\n Данные первой книги обновлены:\n")
        f.write(str(data))
        f.write("\n" + "-" * 50 + "\n")


# Запускаю задачу каждый день в 19:00
print("Ожидаю 19:00")
schedule.every().day.at("13:02").do(check_book)


while True:
    # Проверка, пора ли запустить задачу
    schedule.run_pending()
    # Проверка каждые 60 секунд
    time.sleep(60)

