from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from database import get_db, init_db

app = Flask(__name__)
CORS(app)

init_db()

@app.route('/posts', methods=['GET'])
def get_posts():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content FROM posts ORDER BY id DESC")
    posts = cur.fetchall()
    return jsonify([dict(row) for row in posts])

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
