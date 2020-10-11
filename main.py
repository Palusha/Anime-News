from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {'posts' : 'sqlite:///posts.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'User %r' % self.id

class Article(db.Model):
    __bind_key__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', articles=Article.query.all())


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        lgn = request.form.get("username")
        passw_one = request.form.get("password-one")
        passw_two = request.form.get("password-two")
        print('Username:', lgn)
        print('Password:', passw_one, '-', passw_two)
        if passw_one == passw_two:
            user = User(username=lgn, password=passw_one)
        else:
            print("Разные пароли!")
            return redirect('/signup')

        try:
            db.session.add(user)
            db.session.commit()
            print('Регистрация прошла успешно!')
            return redirect('/login', code=302)
        except:
            print("Произошла ошибка при регистрации...")
            return redirect('/')

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        lgn = request.form.get("username")
        passw = request.form.get("password")
        user = User.query.filter_by(username=lgn).first()

        try:
            if passw == 'admin' and lgn == 'admin':
                print("Вы ввошли как Администратор")
                return redirect('/create-post', code=302)
            elif passw == user.password:
                print('Вы успешно ввошли в аккаунт!')
                return redirect('/')
        except:
            print("Что-то пошло не так...")
            print("Скорее всего, пользователя", lgn, "не существует.")
            return redirect('/')

    return render_template('login.html')

@app.route('/create-post/', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form.get("title")
        post_info = request.form.get("text")
        new_post = Article(title=title, text=post_info)

        db.session.add(new_post)
        db.session.commit()

    return render_template('create-post.html')

@app.route('/delete-post/', methods=['POST', 'GET'])
def delete_post():
    return render_template('delete-post.html', articles=Article.query.all())

@app.route('/delete-post/<int:id>')
def delete(id):
    print(id)
    print(type(id))
    db.session.query(Article).filter(Article.id==id).delete()
    db.session.commit()
    return redirect("/delete-post")


if __name__ == "__main__":
    app.run(debug=True)