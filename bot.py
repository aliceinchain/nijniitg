from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import os

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = Bot(token='7483819477:AAEgQALJ2zROfdn3pPRSRcJlCpK_rnS26wk')
updater = Updater(token='7483819477:AAEgQALJ2zROfdn3pPRSRcJlCpK_rnS26wk', use_context=True)
dispatcher = updater.dispatcher

# Директория для сохранения изображений
IMAGE_DIR = 'path/to/your/image/directory'

def start(update: Update, context):
    update.message.reply_text('Отправьте ссылку на Telegram-канал, чтобы получить аватарку.')

def handle_message(update: Update, context):
    channel_link = update.message.text
    if not channel_link.startswith('@'):
        update.message.reply_text('Пожалуйста, отправьте корректную ссылку на канал.')
        return

    # Получение информации о канале
    chat = bot.get_chat(chat_id=channel_link)
    photo = chat.photo.big_file_id
    file = bot.get_file(photo)
    file.download(out=os.path.join(IMAGE_DIR, f'{chat.id}.jpg'))

    # Обновление веб-сайта
    update_website(channel_link, f'{chat.id}.jpg')

    update.message.reply_text('Аватарка канала успешно добавлена на сайт!')

def update_website(channel_link, image_filename):
    # Здесь вы можете добавить код для обновления вашего веб-сайта
    # Например, добавить новый элемент в HTML-файл или обновить базу данных
    pass

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
