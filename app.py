from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
DATABASE = 'blog.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    print(conn)
    return conn

with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)

@app.route('/posts', methods=['GET'])
def get_posts():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content FROM posts ORDER BY id DESC")
    posts = cur.fetchall()
    return jsonify(posts)

@app.route('/add', methods=['POST'])
def add_post():
    data = request.get_json()
    title = data['title']
    content = data['content']
    if title and content:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        return jsonify({'message': 'Post added successfully!'}), 201
    return jsonify({'message': 'Title and content required!'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
