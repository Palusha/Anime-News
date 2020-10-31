from flask import Blueprint, render_template, request, \
    redirect, session, flash
from flask_login import login_user, login_required, \
    logout_user, current_user
from datetime import datetime
import os
from app import app

from werkzeug.utils import secure_filename
auth = Blueprint('auth', __name__,
                        template_folder='templates')

# code below should be exactly here after the creating Blueprint (above)
from app.models import User, Article, Comment, \
    db, ACCESS




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
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':

        lgn = request.form.get("username")            
        passw_one = request.form.get("password-one")  
        passw_two = request.form.get("password-two")  

        user = User.query.filter_by(username=lgn).first()
        if user:
            flash("Користувач з іменем " + str(lgn) + " вже існує", "error")
            return redirect('/signup')
        if passw_one == passw_two:
            new_user = User(username=lgn)
            new_user.set_password(passw_one)
            db.session.add(new_user)  
            db.session.commit()
            flash('Акаунт створений', "info")
            return redirect('/login', code=302)
        else:
            flash("Ви ввели різні паролі", "error")
            return redirect('/signup')

    return render_template('users-auth/signup.html')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    """ Log in page """
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        lgn = request.form.get("username")
        passw = request.form.get("password")

        user = User.query.filter_by(username=lgn).first()
        if not user:
            flash("Користувача з іменем " + lgn + " не існує", "error")
            return redirect('/login')
        if not user.check_password(passw):
            flash("Ви ввели неправильний пароль", "error")
            return redirect('/login')
        flash('Ви успішно ввійшли в акаунт', "info")
        login_user(user)
        return redirect('/')

    return render_template('users-auth/login.html')

@auth.route('/profile/<username>')
def show_profile(username):
    if current_user.is_authenticated and username == current_user.username:
        return render_template('users-auth/personal-profile.html')
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('users-auth/profile.html', user=user)

@auth.route('/edit-profile/', methods=['POST', 'GET'])
@login_required
def edit_profile():
    if request.method == 'POST':
        uploaded_file = request.files['avatar']
        filename = secure_filename(uploaded_file.filename)

        new_username = request.form.get("username")
        check_user = User.query.filter_by(username=new_username).first()
        
        if not filename and not new_username:
            flash('Ви нічого не змінили', "error")
            return redirect('/edit-profile/')
        else:
            if filename:
                if current_user.avatar != 'default-avatar.png':
                    os.remove(os.path.join(app.config['AVATARS_FOLDER'], current_user.avatar))
                file_id = str(current_user.id) + '-' + datetime.now().strftime("%Y%m%H%M%S%f")
                uploaded_file.save(os.path.join(app.config['AVATARS_FOLDER'], file_id))
                current_user.avatar = file_id
            if new_username:
                if check_user:
                    flash("Поданий нікнейм вже використовуєтся", "error")
                    return redirect('/edit-profile/')
                else:
                    current_user.username = new_username
            flash('Зміни успішно впроваджені', "info")
            db.session.commit()

    return render_template('users-auth/edit-profile.html')

@auth.route('/change-password/', methods=['POST', 'GET'])
@login_required
def change_password():
    if request.method == 'POST':
        old_passw = request.form.get("old-password")            
        passw_one = request.form.get("password-one")  
        passw_two = request.form.get("password-two")  
        
        user = User.query.filter_by(id=current_user.id).first()
        if user.check_password(old_passw) and passw_one == passw_two:
            user.set_password(passw_one)
            db.session.commit()
            flash("Ви успішно змінили пароль", "info")
            return redirect('/profile/' + current_user.username)
        elif not user.check_password(old_passw):
            flash("Старий пароль невірний", "error")
            return redirect('/change-password/')
        else: 
            flash("Паролі не збігаються. Спробуйте ще раз", "error")
            return redirect('/change-password/')

    return render_template('users-auth/change-password.html')

@auth.route('/logout')
@login_required
def logout():
   logout_user()
   flash("Ви вийшли з акаунта", "info")
   return redirect('/')


@auth.route('/create-article/', methods=['POST', 'GET'])
@login_required
def create_article():
    """ Create article page """
    if current_user.role < ACCESS['admin']:
        return "<h1>Доступ заборонений.</h1>"
    if request.method == "POST":
        title = request.form.get("title")
        post_info = request.form.get("text")
        uploaded_file = request.files['thumbnail']
        filename = secure_filename(uploaded_file.filename)
        file_id = datetime.now().strftime("%Y%m%H%M%S%f")

        if filename == '':
            flash("Ви не вибрали зображення", "error")
            return render_template('posts/create-post.html', title_value=title, text_value=post_info)  
        
        uploaded_file.save(os.path.join(app.config['THUMBNAILS_FOLDER'], file_id))
        new_post = Article(title=title, text=post_info, user_id=current_user.id, thumbnail=file_id)
        db.session.add(new_post)
        db.session.commit()
        flash("Стаття була успішно створена", "info")
    return render_template('posts/create-post.html')


@auth.route('/article-table/', methods=['POST', 'GET'])
@login_required
def show_article_table():
    """ Deletes the article page """
    return render_template('posts/article-table.html', articles=Article.query.all())


@auth.route('/delete-article/<int:id>')
@login_required
def delete_article(id):
    article = db.session.query(Article).filter(Article.id == id).first()
    db.session.query(Article).filter(Article.id == id).delete()
    db.session.query(Comment).filter(Comment.article_id == id).delete()
    os.remove(os.path.join(app.config['THUMBNAILS_FOLDER'], article.thumbnail))
    db.session.commit()
    flash("Стаття була успішно видалена", "info")
    return redirect("/article-table")

@auth.route('/edit-post/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_post(id):
    article = Article.query.filter_by(id=id).first()

    if request.method == 'POST':
        new_title = request.form.get("title")
        new_text = request.form.get("text")

        uploaded_file = request.files['thumbnail']
        filename = secure_filename(uploaded_file.filename)
        file_id = datetime.now().strftime("%Y%m%H%M%S%f")

        article.title = new_title
        article.text = new_text
        article.last_update = datetime.now()

        if filename != '':
            os.remove(os.path.join(app.config['THUMBNAILS_FOLDER'], article.thumbnail))
            uploaded_file.save(os.path.join(app.config['THUMBNAILS_FOLDER'], file_id))
            article.thumbnail = file_id

        db.session.commit()
        flash("Зміни успішно впроваджені", "info")
    return render_template('posts/edit-post.html', article=article)


@auth.route('/post/<int:id>', methods=['POST', 'GET'])
def show_post(id):
    article = Article.query.filter_by(id=id).first_or_404()
    return render_template("posts/post.html", article=article)


@auth.route('/create-comment/<int:id>', methods=['POST', 'GET'])
@login_required
def create_comment(id):
    comm_text = request.form.get('text')
    new_comment = Comment(text=comm_text, article_id=id, user_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()
    flash("Коментар був успішно створений", "info")
    return redirect('/post/' + str(id))


@auth.route('/delete-comment/<int:id>')
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    db.session.query(Comment).filter(Comment.id == id).delete()
    db.session.commit()
    flash("Коментар був успішно видалений", "info")
    return redirect('/post/' + str(comment.article_id))
