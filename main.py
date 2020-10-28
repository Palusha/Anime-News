from flask import Flask, render_template, url_for, request, redirect, session, flash
from datetime import datetime
import posts_database
from functools import wraps
import comments_database
from flask_bcrypt import Bcrypt
import users_database

app = Flask(__name__)
app.secret_key = 'Vova'
bcrypt = Bcrypt(app)


def check_login(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect("/login", code=302)
        return func(*args, **kwargs)
    return wrap


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    page = request.args.get('page', default=1, type=int)
    page_count = posts_database.count_articles() // posts_database.pag + (posts_database.count_articles() % posts_database.pag > 0)
    if page <= 0 or page > page_count:
        return redirect("/home")
    return render_template('index.html', articles=posts_database.pagination(page), pages=page_count)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if 'logged_in' in session:
        return redirect("/home", code=302)
    if request.method == "POST":
        email = request.form.get("email")
        passw = request.form.get("password")
        user = users_database.retrieve_user(email)
        print(user)
        if user and bcrypt.check_password_hash(user[2], passw):
            session['logged_in'] = True
            session['email'] = email
            if user[1] == "monday13081@gmail.com":
                session['admin'] = True
            else:
                session['admin'] = False
            return redirect("/create_article", code=302)
        flash("Wrong password or email!")

    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if "logged_in" in session:
        return redirect("/home", code=302)
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        passw = request.form.get("password")
        passw_confirm = request.form.get("confirm")
        if users_database.retrieve_user_email(email):
            flash("This email is not available!")
            return redirect(request.url)
        elif users_database.retrieve_username(username):
            flash("This username is not available!")
            return redirect(request.url)
        elif passw != passw_confirm:
            flash("Passwords doesn't match!")
            return redirect(request.url)
        else:
            passw = bcrypt.generate_password_hash(passw).decode("utf-8")
            users_database.create_user(username, email, passw)

    return render_template("register.html")


@app.route('/logout')
@check_login
def logout():
    session.clear()
    return redirect('/login')


@app.route('/article/<int:id_>', methods=["POST", "GET"])
def show_post(id_):
    if request.method == "POST":
        name = request.form.get("name")
        content = request.form.get("text")
        comments_database.create_comment(id_, datetime.now().strftime("%d.%m.%Y %H:%M:%S"), name, content)
    return render_template('show_article.html', article=posts_database.show_post(id_),
                           comments=comments_database.retrieve_comments(id_))


@app.route('/create_article', methods=["POST", "GET"])
@check_login
def create_article():
    if request.method == "POST":
        title = request.form.get("title")
        post_info = request.form.get("text")
        posts_database.create_post(datetime.now().strftime("%d.%m.%Y %H:%M:%S"), title, post_info)

    return render_template('create_article.html')


@app.route('/edit_articles')
@check_login
def edit_articles():
    return render_template('edit_articles.html', articles=posts_database.retrieve_posts())


@app.route('/edit_article/<int:id_>', methods=["POST", "GET"])
@check_login
def edit_article(id_):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("text")
        posts_database.update_post(id_, title, content)
        return redirect('/edit_articles')
    return render_template('edit_article.html', article=posts_database.show_post(id_))


@app.route('/delete_article/<int:id_>')
@check_login
def delete(id_):
    print(id_)
    posts_database.delete_post(id_)
    return redirect("/edit_articles")


app.run(host='0.0.0.0', debug=True)
