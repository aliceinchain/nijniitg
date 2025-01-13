from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/api/channels')
def get_channels():
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()

    # Get all channels
    c.execute('SELECT channel_id, name FROM channels')
    channels = c.fetchall()

    # Get all connections
    c.execute('SELECT source_id, target_id, weight FROM connections')
    connections = c.fetchall()

    conn.close()

    # Format data for sigma.js
    nodes = [{"id": ch[0], "name": ch[1]} for ch in channels]
    edges = [{"source": conn[0], "target": conn[1], "weight": conn[2]}
             for conn in connections]

    return jsonify({
        "nodes": nodes,
        "edges": edges
    })


if __name__ == '__main__':
    app.run(port=5000)