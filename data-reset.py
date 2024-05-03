import sqlite3

DATABASE = '/nfs/count.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def rollback_count():
    db = connect_db()
    row = db.execute('SELECT * FROM count ORDER BY id ASC LIMIT 1').fetchone()
    new_amount = row['amount'] - 1
    db.execute('UPDATE count SET amount = ? WHERE id = ?', (new_amount, row['id']))
    db.commit()
    print(f'Count has been rolled back to {new_amount}')
    db.close()

if __name__ == '__main__':
    rollback_count()