import sqlite3
import comments_database

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS posts (" \
               "id_ INTEGER(1000) PRIMARY KEY AUTOINCREMENT," \
               "date TEXT, title TEXT, content TEXT)"

CREATE_POST = "INSERT INTO posts VALUES(null, ?, ?, ?)"
RETRIEVE_POSTS = "SELECT * FROM posts ORDER BY date DESC"
RETRIEVE_POST = "SELECT * FROM posts WHERE id_ = ?"
PAGINATION = "SELECT * FROM posts ORDER BY date DESC LIMIT 5 OFFSET ?"
COUNT_ARTICLES = "SELECT COUNT(*) FROM posts"
UPDATE_POST = "UPDATE posts SET title = ?, content = ? WHERE id_ = ?"
DELETE_POST = "DELETE FROM posts WHERE id_ = ?"
DELETE_COMMENTS = "DELETE from comments where id_ = ?"
pag = 5


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
        return cursor.fetchone()


def retrieve_posts():
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RETRIEVE_POSTS)
        return cursor.fetchall()


def pagination(page: int):
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        cursor.execute(PAGINATION, (str(page * pag - pag),))
        return cursor.fetchall()


def delete_post(post_id):
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        cursor.execute(DELETE_POST, (post_id,))
        cursor.execute(DELETE_COMMENTS, (post_id,))
        connection.commit()


def update_post(post_id, title, content):
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        data = (title, content, post_id)
        cursor.execute(UPDATE_POST, data)
        connection.commit()


def count_articles():
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        cursor.execute(COUNT_ARTICLES)
        return cursor.fetchone()[0]