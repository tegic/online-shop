from flask import Flask, render_template, request
import psycopg2, os
from werkzeug.utils import redirect
from config import host, user, password, db_name


def open_db():
    conn = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    cur = conn.cursor()
    print('[INFO] Connection to db')
    return conn, cur


def close_db(conn, cur):
    conn.commit()
    conn.close()
    print('[INFO] Connection was closed')


def create_table_item():
    try:
        conn, cur = open_db()
        cur.execute('''CREATE TABLE IF NOT EXISTS item(
            id serial PRIMARY KEY,
            title varchar(100) NOT NULL,
            price INT NOT NULL,
            isActive BOOLEAN DEFAULT True
        );''')
    except:
        print('[ERROR] Can`t create table item')
    finally:
        close_db(conn, cur)


def add_item(title, price, isActive = True):
    try:
        conn, cur = open_db()
        create_table_item()
        cur.execute('SELECT id FROM item;')
        all_id = cur.fetchall()
        print(all_id)
        try:
            last_id = all_id[-1][0] + 1
        except:
            last_id = 0
        cur.execute(f'''INSERT INTO item(id, title, price, isActive) VALUES('{last_id}', '{title}', {price}, {isActive});''')
    except:
        print('[ERROR] Can`t add item')
    finally:
        close_db(conn, cur)


def show_item_table():
    # try:
    conn, cur = open_db()
    create_table_item()
    cur.execute('''SELECT * FROM item;''')
    items = cur.fetchall()
    result = ''
    print(items)
    for i in range(len(items)):
        result += str(items[i][0]) + ' ' + items[i][1] + ' ' + str(items[i][2]) + ' ' + str(items[i][3]) + '||'
    return items
    close_db(conn, cur)
    # except:
    #     return 'Can`t show item table'
    # finally:



app = Flask(__name__)


# def data_control_for_html(items):

#     return items

@app.route('/')
def index():
    items = show_item_table()
    # items = data_control_for_html(items)
    return render_template('index.html', data=items, count=len(items))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        # text = request.form['']
        try:
            add_item(title, price)
            return redirect('/')
        except:
            print(Exception)
            return "Error"
    else:
        return render_template('create.html')


@app.route('/show')
def show():
    items = show_item_table()
    return items


@app.route('/sign-in')
def sing_in():
    return render_template('sign_in.html')


@app.route('/sign-up')
def sign_up():
    return render_template('sign_up.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))