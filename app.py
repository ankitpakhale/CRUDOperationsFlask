from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db()
        with conn:
            conn.execute('''
                CREATE TABLE items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            ''')
        conn.close()

@app.route('/')
def index():
    conn = get_db()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add_or_update', methods=['POST'])
def add_or_update_item():
    item_id = request.form.get('id')
    name = request.form['name']
    conn = get_db()
    if item_id:
        with conn:
            conn.execute('UPDATE items SET name = ? WHERE id = ?', (name, item_id))
    else:
        with conn:
            conn.execute('INSERT INTO items (name) VALUES (?)', (name,))
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:item_id>')
def edit_item(item_id):
    conn = get_db()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    conn.close()
    return render_template('index.html', item=item, items=get_all_items())

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = get_db()
    with conn:
         conn.execute('DELETE FROM items WHERE id = ?', (item_id,)).fetchone()
    conn.close()
    return redirect(url_for('index'))


def get_all_items():
    conn = get_db()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return items

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
