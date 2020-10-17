from flask import Blueprint, render_template, request, redirect, session
from sqlalchemy import select
from datetime import datetime


auth = Blueprint('auth', __name__,
                        template_folder='templates')

# code below should be exactly here after the creating Blueprint (above)
from models import User, Article, Comment, db


@auth.route('/')
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

        user = User.query.filter_by(username=lgn).first()
        if user:
            print("Пользователь", lgn, "уже существует!")
            return redirect('/login')
        if passw_one == passw_two:
            new_user = User(username=lgn, password=passw_one)
            db.session.add(new_user)  
            db.session.commit()
            print('Регистрация прошла успешно!')
            return redirect('/login', code=302)
        else:
            print("Вы ввели разные пароли! Попробуйте ещё раз.")
            return redirect('/signup')

    return render_template('users-auth/signup.html')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    """ Log in page """
    if 'loggedin' in session:
        return redirect('/create-post')
    if request.method == 'POST':
        lgn = request.form.get("username")
        passw = request.form.get("password")

        user = User.query.filter_by(username=lgn).first()
        if passw == 'admin' and lgn == 'admin':  
            print("Вы ввошли как Администратор")
            session['loggedin'] = True
            return redirect('/create-post', code=302)
        if user:
            if passw == user.password:
                print('Вы успешно ввошли в аккаунт!')
                session['loggedin'] = True
                return redirect('/')
            else:
                print('Вы ввели неверный пароль!')
                return redirect('/login')
        print("Пользователя", lgn, "не существует!")
        return redirect('/login')

    return render_template('users-auth/login.html')

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

    return render_template('posts/create-post.html')


@auth.route('/delete-post/', methods=['POST', 'GET'])
def delete_post():
    """ Delete article page """
    if 'loggedin' not in session:
        return redirect('/')
    return render_template('posts/delete-post.html', articles=Article.query.all())


@auth.route('/delete-post/<int:id>')
def delete(id):
    if 'loggedin' not in session:
        return redirect('/')
    db.session.query(Article).filter(Article.id == id).delete()
    # db.session.query(Comment).filter(Comment.article_id == id).delete()
    db.session.commit()
    return redirect("/delete-post")

@auth.route('/edit-post/<int:id>', methods=['POST', 'GET'])
def edit(id):
    if 'loggedin' not in session:
        return redirect('/')
    article = Article.query.filter_by(id=id).first()

    if request.method == 'POST':
        new_title = request.form.get("title")
        new_text = request.form.get("text")

        if new_title == article.title and new_text == article.text:
            print('Вы ничего не изменили!')
            return redirect('/edit-post/' + str(id))

        article.title = new_title
        article.text = new_text
        db.session.commit()

    return render_template('posts/edit-post.html', article=article)


@auth.route('/post/<int:id>', methods=['POST', 'GET'])
def show_post(id):
    article = Article.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(article_id=id)
    if request.method == 'POST':
        comm_text = request.form.get('text')
        new_comment = Comment(text=comm_text, article_id=id)

        db.session.add(new_comment)
        db.session.commit()
        return redirect('/post/' + str(id))
    return render_template("posts/post.html", article=article, comments=comments)

