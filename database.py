import sqlite3


CREATE_TABLE = "CREATE TABLE IF NOT EXISTS posts (" \
               "id_ INTEGER PRIMARY KEY AUTOINCREMENT," \
               "date TEXT, title TEXT, content TEXT)"

CREATE_POST = "INSERT INTO posts VALUES(null, ?, ?, ?)"
RETRIEVE_POSTS = "SELECT * FROM posts"
RETRIEVE_POST = "SELECT * FROM posts WHERE id_ = ?"


def create_tables():
    with sqlite3.connect("post.db") as connection:
        connection.execute(CREATE_TABLE)


def create_post(date, title, content):
    with sqlite3.connect("post.db") as connection:
        connection.execute(CREATE_POST, (date, title, content))


def show_post(id_):
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RETRIEVE_POST, (id_,))
        return cursor.fetchall()


def retrieve_posts():
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RETRIEVE_POSTS)
        return cursor.fetchall()


def delete_post(post_id):
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        sql_delete_query = """DELETE from posts where id_ = ?"""
        cursor.execute(sql_delete_query, (post_id,))
        connection.commit()