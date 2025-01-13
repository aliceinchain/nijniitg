from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('channels.db')
    cursor = conn.cursor()
    cursor.execute('SELECT channel_link, image_filename FROM channels')
    channels = cursor.fetchall()
    conn.close()

    return render_template('index.html', channels=channels)

if __name__ == '__main__':
    app.run(debug=True)
