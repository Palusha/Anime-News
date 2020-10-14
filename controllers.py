from flask import Blueprint, render_template, request, redirect, session
from sqlalchemy import select
from datetime import datetime


auth = Blueprint('auth', __name__,
                        template_folder='templates')

# code below should be exactly here after the creating Blueprint (above)
from models import User, Article, db
from app import user_engine, posts_engine # importing created engines from app.py

@auth.route('/')
@auth.route('/home')
def index():
    """ Home page """
    return render_template('index.html', articles=Article.query.all())


@auth.route('/about/')
def about():
    """ About page """
    return render_template('about.html')

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    """ 
    Sign up page
    """
    if 'loggedin' in session:
        return redirect('/create-post')
    if request.method == 'POST':

        lgn = request.form.get("username")            
        passw_one = request.form.get("password-one")  
        passw_two = request.form.get("password-two")  

        conn = user_engine.connect() # connects to the created engine in app.py

        s = select([User.username]).where(User.username == lgn)
        result = conn.execute(s)
        account = result.fetchone()
        if account:
            print("Пользователь", lgn, "уже существует!")
            return redirect('/login')
        if passw_one == passw_two:
            user = User(username=lgn, password=passw_one)
            db.session.add(user)  
            db.session.commit()
            print('Регистрация прошла успешно!')
            return redirect('/login', code=302)
        else:
            print("Вы ввели разные пароли! Попробуйте ещё раз.")
            return redirect('/signup')

    return render_template('signup.html')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    """ Log in page """
    if 'loggedin' in session:
        return redirect('/create-post')
    if request.method == 'POST':
        lgn = request.form.get("username")
        passw = request.form.get("password")
        
        conn = user_engine.connect() # connects to the created engine in app.py

        s = select([User.username, User.password]).where(User.username == lgn)
        result = conn.execute(s)
        user = result.fetchone()

        if passw == 'admin' and lgn == 'admin':  
            print("Вы ввошли как Администратор")
            session['loggedin'] = True
            return redirect('/create-post', code=302)
        elif user:
            if passw == user.password:
                print('Вы успешно ввошли в аккаунт!')
                session['loggedin'] = True
                return redirect('/')
            else:
                print('Вы ввели неверный пароль!')
                return redirect('/login')
        print("Пользователя", lgn, "не существует!")
        return redirect('/login')

    return render_template('login.html')

@auth.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect('/')


@auth.route('/create-post/', methods=['POST', 'GET'])
def create_article():
    """ Create article page """
    if 'loggedin' not in session:
        return redirect('/')
    if request.method == "POST":
        title = request.form.get("title")
        post_info = request.form.get("text")
        time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S") # deletes miliseconds from the date
        new_post = Article(title=title, text=post_info, date=time)

        db.session.add(new_post)
        db.session.commit()

    return render_template('create-post.html')


@auth.route('/delete-post/', methods=['POST', 'GET'])
def delete_post():
    """ Delete article page """
    if 'loggedin' not in session:
        return redirect('/')
    return render_template('delete-post.html', articles=Article.query.all())


@auth.route('/delete-post/<int:id>')
def delete(id):
    if 'loggedin' not in session:
        return redirect('/')
    db.session.query(Article).filter(Article.id == id).delete()
    db.session.commit()
    return redirect("/delete-post")

@auth.route('/post/<int:id>')
def show_post(id):
    conn = posts_engine.connect() # connects to the created engine in app.py

    s = select([Article.title, Article.text]).where(Article.id == id)
    result = conn.execute(s)
    article = result.fetchone()
    return render_template("post.html", title=article.title, text=article.text)
