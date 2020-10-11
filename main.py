from flask import Flask, render_template, url_for, request, redirect, session
from datetime import datetime
import database
import time

app = Flask(__name__)
app.secret_key = 'SOME SECRET'


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', articles=database.retrieve_posts())


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if 'username' in session:
        return redirect("/create-post", code=302)
    if request.method == "POST":
        lgn = request.form.get("username")
        passw = request.form.get("password")
        print(lgn)
        print(passw)
        if lgn == 'admin' and passw == 'admin':
            session['username'] = request.form['username']
            return redirect("/create-post", code=302)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


@app.route('/create-post', methods=["POST", "GET"])
def create_article():
    if 'username' not in session:
        return redirect("/login", code=302)

    if request.method == "POST":
        title = request.form.get("title")
        post_info = request.form.get("text")
        database.create_post(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), title, post_info)

    return render_template('create_post.html')


@app.route('/delete_post', methods=["POST", "GET"])
def delete_article():
    if 'username' not in session:
        return redirect("/login", code=302)

    return render_template('delete_post.html', articles=database.retrieve_posts())


@app.route('/delete_post/<int:id_>')
def delete(id_):
    if 'username' not in session:
        return redirect("/login", code=302)
    print(id_)
    database.delete_post(id_)
    return redirect("/delete_post")


app.run(host='0.0.0.0', debug=True)
