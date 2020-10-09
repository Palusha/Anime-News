from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
post = []


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('index.html', articles=articles)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        lgn = request.form.get("username")
        passw = request.form.get("password")
        print(lgn)
        print(passw)
        if lgn == 'admin' and passw == 'admin':
            return redirect("/create-post", code=302)

    return render_template('login.html')


@app.route('/create-post', methods=["POST", "GET"])
def create_article():
    if request.method == "POST":
        title = request.form.get("title")
        post_info = request.form.get("text")
        post.append({request.form.get("title"), request.form.get("text")})
        print(post)
        article = Article(title=title, text=post_info)

        try:
            db.session.add(article)
            db.session.commit()
            print('Success')
        except:
            print("При добавлении статьи произошла ошибка")
    return render_template('create_post.html')


@app.route('/post/<int:post_id>')
def show_user_profile(post_id):
    return 'This post id is:  %d' % post_id


app.run(host='0.0.0.0', debug=True)
