from flask import Flask, render_template, url_for, request, redirect, session
from datetime import datetime
import database
from functools import wraps

app = Flask(__name__)
app.secret_key = 'Vova'


def check_login(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect("/login", code=302)
        return func(*args, **kwargs)
    return wrap


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', articles=database.retrieve_posts())


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if 'logged_in' in session:
        return redirect("/home", code=302)

    if request.method == "POST":
        lgn = request.form.get("username")
        passw = request.form.get("password")
        if lgn == 'admin' and passw == 'admin':
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect("/create_article", code=302)

    return render_template('login.html')


@app.route('/logout')
@check_login
def logout():
    session.clear()
    return redirect('/login')


@app.route('/article/<int:id_>')
def show_post(id_):
    return render_template('show_article.html', article=database.show_post(id_))


@app.route('/create_article', methods=["POST", "GET"])
@check_login
def create_article():
    if request.method == "POST":
        title = request.form.get("title")
        post_info = request.form.get("text")
        database.create_post(datetime.now().strftime("%d.%m.%Y %H:%M"), title, post_info)

    return render_template('create_article.html')


@app.route('/edit_articles')
@check_login
def edit_articles():
    return render_template('edit_articles.html', articles=database.retrieve_posts())


@app.route('/edit_article/<int:id_>', methods=["POST", "GET"])
@check_login
def edit_article(id_):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("text")
        database.update_post(id_, title, content)
        return redirect('/edit_articles')
    return render_template('edit_article.html', article=database.show_post(id_))


@app.route('/delete_article/<int:id_>')
@check_login
def delete(id_):
    print(id_)
    database.delete_post(id_)
    return redirect("/edit_articles")


app.run(host='0.0.0.0', debug=True)
