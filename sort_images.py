import os
from PIL import Image

# Функция для вычисления среднего цвета изображения
def calculate_average_color(image_path):
    with Image.open(image_path) as img:
        img = img.resize((50, 50))  # Уменьшаем изображение для ускорения вычислений
        pixels = list(img.getdata())
        r, g, b = 0, 0, 0
        for pixel in pixels:
            r += pixel[0]
            g += pixel[1]
            b += pixel[2]
        count = len(pixels)
        return (r / count, g / count, b / count)

# Функция для сортировки изображений по среднему цвету
def sort_images_by_color(image_files):
    # Вычисляем средний цвет для каждого изображения
    image_colors = [(calculate_average_color(f'images/{file}'), file) for file in image_files]
    # Сортируем изображения по среднему цвету
    image_colors.sort(key=lambda x: x[0])
    return [file for _, file in image_colors]

def update_website():
    # Получение списка всех изображений
    image_files = [f for f in os.listdir('images') if f.endswith('.jpg')]

    # Сортировка изображений по среднему цвету
    sorted_images = sort_images_by_color(image_files)

    # Путь к вашему HTML-файлу
    html_file_path = 'index.html'

    # Чтение текущего содержимого HTML-файла
    with open(html_file_path, 'r') as file:
        html_content = file.read()

    # Создание HTML-кода для изображений
    images_html = ''
    for image_file in sorted_images:
        channel_link = image_file.split('.')[0]  # Используем имя файла без расширения как имя канала
        images_html += f'''
        <a href="https://t.me/{channel_link}" class="image-link" target="_blank">
            <img src="images/{image_file}" alt="Channel Avatar">
        </a>
        '''

    # Найти контейнер и добавить новый элемент
    container_start = html_content.find('<div id="image-container">') + len('<div id="image-container">')
    container_end = html_content.find('</div>', container_start)
    html_content = html_content[:container_start] + images_html + html_content[container_start:]

    # Запись обновленного содержимого в HTML-файл
    with open(html_file_path, 'w') as file:
        file.write(html_content)

if __name__ == '__main__':
    update_website()
