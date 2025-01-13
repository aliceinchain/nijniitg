import sqlite3

def check_database():
    conn = sqlite3.connect('channels.db')
    cursor = conn.cursor()
    cursor.execute('SELECT channel_link, image_filename FROM channels')
    channels = cursor.fetchall()
    conn.close()

    for channel in channels:
        print(channel)

check_database()
