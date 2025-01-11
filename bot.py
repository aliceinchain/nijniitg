from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Функция, которая будет вызываться при получении команды /start
async def start(update: Update, context) -> None:
    await update.message.reply_text('Привет! Я ваш Telegram-бот.')

async def handle_message(update: Update, context) -> None:
    channel_link = update.message.text
    if not channel_link.startswith('@'):
        await update.message.reply_text('Пожалуйста, отправьте корректную ссылку на канал.')
        return

    # Получение информации о канале
    chat = await context.bot.get_chat(chat_id=channel_link)
    photo = chat.photo.big_file_id
    file = await context.bot.get_file(photo)
    await file.download_to_drive(f'images/{chat.id}.jpg')

    # Обновление веб-сайта
    update_website(channel_link, f'{chat.id}.jpg')

    await update.message.reply_text('Аватарка канала успешно добавлена на сайт!')

def update_website(channel_link, image_filename):
    # Здесь вы можете добавить код для обновления вашего веб-сайта
    # Например, добавить новый элемент в HTML-файл или обновить базу данных
    pass

def main() -> None:
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    application = ApplicationBuilder().token('7483819477:AAEgQALJ2zROfdn3pPRSRcJlCpK_rnS26wk').build()

    # Регистрация обработчика команды /start
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
