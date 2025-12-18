import flask
import sqlite3
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os


app = flask.Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day"],
    storage_uri="memory://",
)

conn = sqlite3.connect('gifts.db') 
cursor = conn.cursor()  
cursor.execute('''
    CREATE TABLE IF NOT EXISTS gifts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gift TEXT NOT NULL,
        time INTEGER NOT NULL
    )
''')
conn.commit()  
conn.close()

@app.get("/")
@limiter.exempt
def index():
    return flask.send_from_directory("static", "index.html")
@app.post("/gifts")
def create_gift():
    data = flask.request.get_json()
    name = data.get('name')
    gift = data.get('gift')
    time = data.get('time')
    
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO gifts (name, gift, time) VALUES (?, ?, ?)', (name, gift, time))
    conn.commit()
    conn.close()

    return '', 201
    
@app.get("/gifts")
def get_gifts():
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, gift, time FROM gifts')
    rows = cursor.fetchall()
    conn.close()
    
    gifts = [{'id': row[0], 'name': row[1], 'gift': row[2], 'time': row[3]} for row in rows]
    return flask.jsonify(gifts)

@app.get("/stats")
def get_stats():
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, AVG(CAST(time AS REAL)) as avg_time, COUNT(*) as total_gifts
        FROM gifts
        GROUP BY name
        ORDER BY avg_time ASC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    stats = [{'country': row[0], 'avg_time': round(row[1], 2), 'total_gifts': row[2]} for row in rows]
    return flask.jsonify(stats)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)