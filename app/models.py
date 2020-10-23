from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5

@login_manager.user_loader
def load_user(user):
    return User.query.get(user)

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(50), default='default.jpg', nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def create_avatar(unique_attr, size):
        digest = md5(unique_attr.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Article(db.Model):
    __bind_key__ = 'posts' # <-- binded key
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='article', lazy='dynamic')

class Comment(db.Model):
    __bind_key__ = 'comments' # <-- binded key
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)