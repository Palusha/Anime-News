from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from datetime import datetime


app = Flask(__name__)
# configuration (location) of the FIRST database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# binds keys to the rest of the databases (there is only one named 'posts.db')
app.secret_key = 'xyipizda'
app.config['SQLALCHEMY_BINDS'] = {'posts': 'sqlite:///posts.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# model for users.db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'User %r' % self.id

# model for posts.db
class Article(db.Model):
    __bind_key__ = 'posts' # <-- binded key

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.String, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    """ Home page """
    return render_template('index.html', articles=Article.query.all())


@app.route('/about/')
def about():
    """ About page """
    return render_template('about.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """ 
    Sign up page (everything is hidden because
    signing up is not nessecery yet.
    """
    return redirect('/login')

    # if request.method == 'POST':
    #     # gets username and passwords from <input> on signup.html
    #     lgn = request.form.get("username")            
    #     passw_one = request.form.get("password-one")  
    #     passw_two = request.form.get("password-two")  
    #     engine = create_engine('sqlite:///users.db')
    #     with engine.connect() as connection:
    #         userdata = (lgn, passw)
    #         cursor = connection.execute('SELECT * FROM users WHERE username = %s AND password = %s', userdata)
    #         account = cursor.fetchone()
    #         if account:
    #             print("Пользователь", lgn, "уже существует!")
    #             return redirect('/login')
    #     if passw_one == passw_two:
    #         user = User(username=lgn, password=passw_one)
    #         db.session.add(user)  
    #         db.session.commit()
    #         print('Регистрация прошла успешно!')
    #         return redirect('/login', code=302)
    #     else:
    #         print("Вы ввели разные пароли! Попробуйте ещё раз.")
    #         return redirect('/signup')

    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    """ Log in page """
    if 'loggedin' in session:
        return redirect('/create-post')
    if request.method == 'POST':
        # gets username and password from <input> on login.html
        lgn = request.form.get("username")
        passw = request.form.get("password")

        user = User.query.filter_by(username=lgn).first()
        # for username and password "admin" moves to create-post.html
        if passw == 'admin' and lgn == 'admin':  
            print("Вы ввошли как Администратор")
            session['loggedin'] = True
            return redirect('/create-post', code=302)
        # elif passw == user.password:
        #     print('Вы успешно ввошли в аккаунт!')
        #     return redirect('/')
        # print("Пользователя", lgn, "не существует!")
        # return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect('/')


@app.route('/create-post/', methods=['POST', 'GET'])
def create_article():
    """ Create article page """
    if 'loggedin' not in session:
        return redirect('/')
    if request.method == "POST":
        title = request.form.get("title")
        post_info = request.form.get("text")
        time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        new_post = Article(title=title, text=post_info, date=time)

        # adds created article to the posts.db
        db.session.add(new_post)
        db.session.commit()

    return render_template('create-post.html')


@app.route('/delete-post/', methods=['POST', 'GET'])
def delete_post():
    """ Delete article page """
    if 'loggedin' not in session:
        return redirect('/')
    return render_template('delete-post.html', articles=Article.query.all())


@app.route('/delete-post/<int:id>')
def delete(id):
    if 'loggedin' not in session:
        return redirect('/')
    # clicking on the link deletes an article by it's id
    db.session.query(Article).filter(Article.id == id).delete()
    db.session.commit()
    return redirect("/delete-post")

if __name__ == "__main__":
    # runs the app in the debug mode (should be turned off)
    # and allows people in LAN connect to the website
    app.run(debug=True, host='0.0.0.0')