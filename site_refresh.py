def update_website(channel_link, image_filename):
    # Путь к вашему HTML-файлу
    html_file_path = 'path/to/your/index.html'

    # Чтение текущего содержимого HTML-файла
    with open(html_file_path, 'r') as file:
        html_content = file.read()

    # Добавление нового изображения и ссылки
    new_image_html = f'''
    <a href="{channel_link}" class="image-link" target="_blank">
        <img src="images/{image_filename}" alt="Channel Avatar">
    </a>
    '''
    # Обновление содержимого HTML-файла
    html_content = html_content.replace('</body>', f'{new_image_html}</body>')

    # Запись обновленного содержимого в HTML-файл
    with open(html_file_path, 'w') as file:
        file.write(html_content)
