import sqlite3

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS comments (" \
               "id_ INTEGER, date TEXT, username TEXT, email TEXT, content TEXT)"

CREATE_COMMENT = "INSERT INTO comments VALUES(?, ?, ?, ?)"
RETRIEVE_COMMENTS = "SELECT * FROM comments WHERE id_ = ? ORDER BY date DESC "
UPDATE_COMMENT = "UPDATE comments SET content = ? WHERE id_ = ?, date = ?, email = ?"
DELETE_COMMENT = "DELETE from comments where id_ = ?, date = ?, email = ?"


def create_table():
    with sqlite3.connect("post.db") as connection:
        connection.execute(CREATE_TABLE)


def create_comment(id_, date, username, content):
    with sqlite3.connect("post.db") as connection:
        connection.execute(CREATE_COMMENT, (id_, date, username, content))


def retrieve_comments(id_):
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RETRIEVE_COMMENTS, (id_,))
        return cursor.fetchall()


def delete_comment(id_, name, date):
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        cursor.execute(DELETE_COMMENT, (id_, name, date))
        connection.commit()


def update_comment(id_, content, date, name):
    with sqlite3.connect("post.db") as connection:
        cursor = connection.cursor()
        data = (content, id_, date, name)
        cursor.execute(UPDATE_COMMENT, data)
        connection.commit()
