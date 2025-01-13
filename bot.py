import os
from dotenv import load_dotenv
from telegram import Update, error
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена из переменной окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Проверка, что токен загружен
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Telegram bot token is not set in environment variables.")

# Функция для добавления канала в базу данных
def add_channel_to_db(channel_link, image_filename):
    conn = sqlite3.connect('channels.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO channels (channel_link, image_filename) VALUES (?, ?)', (channel_link, image_filename))
    conn.commit()
    conn.close()

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

        # Добавление канала в базу данных
        add_channel_to_db(channel_link, f'{chat.id}.jpg')

        await update.message.reply_text('Аватарка канала успешно добавлена на сайт!')
    except error.BadRequest as e:
        await update.message.reply_text(f'Ошибка: {e.message}. Пожалуйста, проверьте ссылку на канал и убедитесь, что бот имеет доступ к каналу.')
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {str(e)}')

def main() -> None:
    # Использование вашего токена
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрация обработчика команды /start
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
