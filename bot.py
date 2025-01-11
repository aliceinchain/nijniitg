import os
from telegram import Update, error
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
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

# Функция, которая будет вызываться при получении команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я ваш Telegram-бот. Отправьте ссылку на канал.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    channel_link = update.message.text

    # Проверка формата ссылки
    if not (channel_link.startswith('@') or channel_link.startswith('https://t.me/')):
        await update.message.reply_text('Пожалуйста, отправьте корректную ссылку на канал.')
        return

    # Если ссылка начинается с https://t.me/, извлекаем имя пользователя и добавляем @
    if channel_link.startswith('https://t.me/'):
        channel_link = '@' + channel_link.split('/')[-1]

    try:
        # Получение информации о канале
        chat = await context.bot.get_chat(chat_id=channel_link)
        photo = chat.photo.big_file_id
        file = await context.bot.get_file(photo)

        # Создание директории для сохранения изображений, если она не существует
        os.makedirs('images', exist_ok=True)

        # Сохранение изображения
        file_path = f'images/{chat.id}.jpg'
        await file.download_to_drive(file_path)

        # Обновление веб-сайта
        update_website()

        await update.message.reply_text('Аватарка канала успешно добавлена на сайт!')
    except error.BadRequest as e:
        await update.message.reply_text(f'Ошибка: {e.message}. Пожалуйста, проверьте ссылку на канал и убедитесь, что бот имеет доступ к каналу.')
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {str(e)}')

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

def main() -> None:
    # Использование вашего токена
    application = ApplicationBuilder().token('7483819477:AAEgQALJ2zROfdn3pPRSRcJlCpK_rnS26wk').build()

    # Регистрация обработчика команды /start
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
