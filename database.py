import sqlite3

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS posts (title TEXT, content TEXT)"
CREATE_POST = "INSERT INTO posts VALUES(?, ?)"
RETRIEVE_POSTS = "SELECT * FROM posts"


def create_tables():
    with sqlite3.connect("post.db") as connection:
        connection.execute(CREATE_TABLE)


def create_post(title, content):
    with sqlite3.connect("post.db") as connection:
        connection.execute(CREATE_POST, (title, content))


def retrieve_posts():
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RETRIEVE_POSTS)
        return cursor.fetchall()


def delete_post(title):
    to_delete = title
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        sql_delete_query = """DELETE from posts where title = ?"""
        cursor.execute(sql_delete_query, (to_delete,))
        connection.commit()
