import os
from telegram import Update, error
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

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
        update_website(channel_link, f'{chat.id}.jpg')

        await update.message.reply_text('Аватарка канала успешно добавлена на сайт!')
    except error.BadRequest as e:
        await update.message.reply_text(f'Ошибка: {e.message}. Пожалуйста, проверьте ссылку на канал и убедитесь, что бот имеет доступ к каналу.')
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {str(e)}')

def update_website(channel_link, image_filename):
    # Путь к вашему HTML-файлу
    html_file_path = 'index.html'

    # Чтение текущего содержимого HTML-файла
    with open(html_file_path, 'r') as file:
        html_content = file.read()

    # Добавление нового изображения и ссылки в контейнер
    new_image_html = f'''
    <a href="https://t.me/{channel_link.lstrip('@')}" class="image-link" target="_blank">
        <img src="images/{image_filename}" alt="Channel Avatar">
    </a>
    '''
    # Найти контейнер и добавить новый элемент
    container_start = html_content.find('<div id="image-container">') + len('<div id="image-container">')
    container_end = html_content.find('</div>', container_start)
    html_content = html_content[:container_start] + new_image_html + html_content[container_start:]

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
