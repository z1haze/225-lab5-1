import os
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__, static_folder='../dist', static_url_path='/')

DATABASE = '/nfs/count.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS count (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount INTEGER NOT NULL
            );
        ''')
        db.execute('INSERT INTO count (amount) VALUES (0);')
        db.commit()

init_db()


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/count', methods=['GET'])
def count():
    db = get_db()
    row = db.execute('SELECT amount FROM count LIMIT 1').fetchone()

    return jsonify({"count": row['amount']})


@app.route('/api/count/increment', methods=['POST'])
def increment():
    db = get_db()
    row = db.execute('SELECT * FROM count ORDER BY id ASC LIMIT 1').fetchone()
    new_amount = row['amount'] + 1
    db.execute('UPDATE count SET amount = ? WHERE id = ?', (new_amount, row['id']))
    db.commit()

    return jsonify({"count": new_amount})