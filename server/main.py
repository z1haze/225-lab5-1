import os
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='*')

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)