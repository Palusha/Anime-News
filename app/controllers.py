from flask import Blueprint, render_template, request, \
    redirect, session, flash
from flask_login import login_user, login_required, \
    logout_user, current_user
from datetime import datetime

auth = Blueprint('auth', __name__,
                        template_folder='templates')

# code below should be exactly here after the creating Blueprint (above)
from app.models import User, Article, Comment, db




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
            flash("Користувач з іменем " + str(lgn) + " вже існує.")
            return redirect('/signup')
        if passw_one == passw_two:
            new_user = User(username=lgn, avatar=User.create_avatar(lgn, 512))
            new_user.set_password(passw_one)
            db.session.add(new_user)  
            db.session.commit()
            flash('Акаунт створений!')
            return redirect('/login', code=302)
        else:
            flash("Ви ввели різні паролі. Спробуйте знову.")
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
        if not user or not user.check_password(passw):
            flash("Некорректне ім'я користувача або пароль.")
            return redirect('/login')
        flash('Ви успішно ввійшли в акаунт!')
        login_user(user)
        return redirect('/')

    return render_template('users-auth/login.html')

@auth.route('/profile/<username>')
@login_required
def show_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('users-auth/profile.html', user=user)

@auth.route('/logout')
@login_required
def logout():
   logout_user()
   flash("Ви вийшли з акаунта.")
   return redirect('/')


@auth.route('/create-article/', methods=['POST', 'GET'])
@login_required
def create_article():
    """ Create article page """
    if request.method == "POST":
        title = request.form.get("title")
        post_info = request.form.get("text")
        new_post = Article(title=title, text=post_info, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash("Стаття була успішно створена.")
    return render_template('posts/create-post.html')


@auth.route('/article-table/', methods=['POST', 'GET'])
@login_required
def show_article_table():
    """ Deletes the article page """
    return render_template('posts/delete-post.html', articles=Article.query.all())


@auth.route('/delete-article/<int:id>')
@login_required
def delete_article(id):
    db.session.query(Article).filter(Article.id == id).delete()
    db.session.query(Comment).filter(Comment.article_id == id).delete()
    db.session.commit()
    flash("Стаття була успішно видалена.")
    return redirect("/article-table")

@auth.route('/edit-post/<int:id>', methods=['POST', 'GET'])
@login_required
def edit(id):
    article = Article.query.filter_by(id=id).first()

    if request.method == 'POST':
        new_title = request.form.get("title")
        new_text = request.form.get("text")

        if new_title == article.title and new_text == article.text:
            flash('Ви нічого не змінили!')
            return redirect('/edit-post/' + str(id))

        article.title = new_title
        article.text = new_text
        article.last_update = datetime.now()
        db.session.commit()
        flash("Зміни успішно впроваджені.")
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
    return redirect('/post/' + str(id))


@auth.route('/delete-comment/<int:id>')
@login_required
def delete_comment(id):
    article = Comment.query.filter_by(id=id).first().article_id
    db.session.query(Comment).filter(Comment.id == id).delete()
    db.session.commit()
    flash("Коментар був успішно видалений.")
    return redirect('/post/' + str(article))