import sqlite3
from bs4 import BeautifulSoup

def import_existing_data(html_file_path):
    # Чтение HTML-файла
    with open(html_file_path, 'r') as file:
        html_content = file.read()

    # Парсинг HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    image_links = soup.find_all('a', class_='image-link')

    # Подключение к базе данных
    conn = sqlite3.connect('channels.db')
    cursor = conn.cursor()

    # Добавление данных в базу данных
    for link in image_links:
        channel_link = link['href'].split('/')[-1]
        image_filename = link.find('img')['src'].split('/')[-1]
        cursor.execute('INSERT INTO channels (channel_link, image_filename) VALUES (?, ?)', (channel_link, image_filename))

    conn.commit()
    conn.close()

# Вызов функции для импорта данных
import_existing_data('index.html')
