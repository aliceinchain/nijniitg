import os
import sqlite3
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telethon import TelegramClient
import asyncio
import json

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')


# Initialize database
def init_db():
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS channels
        (channel_id TEXT PRIMARY KEY, name TEXT, avatar_path TEXT)
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS connections
        (source_id TEXT, target_id TEXT, weight INTEGER,
         PRIMARY KEY (source_id, target_id))
    ''')
    conn.commit()
    conn.close()


init_db()


# Bot command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Add Channel", callback_data='mode_add'),
            InlineKeyboardButton("Update Graph", callback_data='mode_graph')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Choose mode:',
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'mode_add':
        context.user_data['mode'] = 'add'
        await query.edit_message_text('Send me a channel link to add it to the gallery.')
    elif query.data == 'mode_graph':
        context.user_data['mode'] = 'graph'
        await query.edit_message_text('Send me a channel link to analyze its connections.')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get('mode', 'add')
    channel_link = update.message.text

    if not (channel_link.startswith('@') or channel_link.startswith('https://t.me/')):
        await update.message.reply_text('Please send a valid channel link.')
        return

    if channel_link.startswith('https://t.me/'):
        channel_link = '@' + channel_link.split('/')[-1]

    if mode == 'add':
        await add_channel(update, context, channel_link)
    else:
        await analyze_channel(update, context, channel_link)


async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, channel_link):
    try:
        chat = await context.bot.get_chat(channel_link)
        photo = chat.photo.big_file_id
        file = await context.bot.get_file(photo)

        os.makedirs('images', exist_ok=True)
        file_path = f'images/{chat.id}.jpg'
        await file.download_to_drive(file_path)

        # Save to database
        conn = sqlite3.connect('channels.db')
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO channels VALUES (?, ?, ?)',
                  (str(chat.id), chat.username, file_path))
        conn.commit()
        conn.close()

        update_website(channel_link, f'{chat.id}.jpg')
        await update.message.reply_text('Channel added successfully!')

    except Exception as e:
        await update.message.reply_text(f'Error: {str(e)}')


async def analyze_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, channel_link):
    try:
        await update.message.reply_text('Analyzing channel connections...')

        client = TelegramClient('bot_session', API_ID, API_HASH)
        await client.start()

        # Get channel entity
        channel = await client.get_entity(channel_link)

        # Get last 150 messages
        messages = await client.get_messages(channel, limit=150)

        # Analyze forwarded messages
        connections = {}
        for msg in messages:
            if msg.forward and msg.forward.channel_id:
                fwd_id = str(msg.forward.channel_id)
                connections[fwd_id] = connections.get(fwd_id, 0) + 1

        # Update database
        conn = sqlite3.connect('channels.db')
        c = conn.cursor()

        for target_id, weight in connections.items():
            c.execute('''
                INSERT OR REPLACE INTO connections (source_id, target_id, weight)
                VALUES (?, ?, ?)
            ''', (str(channel.id), target_id, weight))

        conn.commit()
        conn.close()

        await client.disconnect()
        await update.message.reply_text('Channel connections analyzed and graph updated!')

    except Exception as e:
        await update.message.reply_text(f'Error during analysis: {str(e)}')


def update_website(channel_link, image_filename):
    html_file_path = 'index.html'
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    new_image_html = f'''
    <a href="https://t.me/{channel_link.lstrip('@')}" class="image-link" target="_blank">
        <img src="images/{image_filename}" alt="Channel Avatar">
    </a>
    '''

    container_start = html_content.find('<div id="image-container">') + len('<div id="image-container">')
    html_content = html_content[:container_start] + new_image_html + html_content[container_start:]

    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)


def main():
    if not all([TELEGRAM_BOT_TOKEN, API_ID, API_HASH]):
        raise ValueError("Missing required environment variables")

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()