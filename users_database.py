import sqlite3

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS users (" \
               "username TEXT, email TEXT, password TEXT)"

CREATE_USER = "INSERT INTO users VALUES(?, ?, ?)"
RETRIEVE_USER_EMAIL = "SELECT * FROM users WHERE email = ?"
RETRIEVE_USERNAME = "SELECT * FROM users WHERE username = ?"
UPDATE_PASSWORD = "UPDATE users SET password = ? WHERE email = ?"
UPDATE_USERNAME = "UPDATE users SET username = ? WHERE email = ?"
RETRIEVE_USER = "SELECT * FROM users WHERE email = ?"
# DELETE_USER = "DELETE from comments where id_ = ?, name = ?, date = ?"


def create_table():
    with sqlite3.connect("users.db") as connection:
        connection.execute(CREATE_TABLE)


def create_user(username, email, password):
    with sqlite3.connect("users.db") as connection:
        connection.execute(CREATE_USER, (username, email, password))


def retrieve_user(email):
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RETRIEVE_USER, (email,))
        return cursor.fetchone()


def retrieve_user_email(email):
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RETRIEVE_USER_EMAIL, (email,))
        return cursor.fetchone()


def retrieve_username(username):
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RETRIEVE_USERNAME, (username,))
        return cursor.fetchone()


# def delete_comment(id_, name, date):
#     with sqlite3.connect("users.db") as connection:
#         cursor = connection.cursor()
#         cursor.execute(DELETE_COMMENT, (id_, name, date))
#         connection.commit()


def update_password(password, email):
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute(UPDATE_PASSWORD, (password, email))
        connection.commit()


def update_username(username, email):
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute(UPDATE_USERNAME, (username, email))
        connection.commit()
