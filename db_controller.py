from flask import Flask, render_template
import psycopg2
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
    conn, cur = open_db()
    cur.execute('''CREATE TABLE IF NOT EXISTS item(
        id serial PRIMARY KEY,
        title varchar(100) NOT NULL,
        price INT NOT NULL,
        isActive BOOLEAN DEFAULT True
    );''')
    conn.commit()
    close_db(conn, cur)


def delete_data():
    conn, cur = open_db()
    cur.execute('DELETE FROM item;')
    close_db(conn, cur)


# create_table_item()
delete_data()