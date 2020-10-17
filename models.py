from flask_sqlalchemy import SQLAlchemy
from app import app, db
from datetime import datetime



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'User %r' % self.id

class Article(db.Model):
    __bind_key__ = 'posts' # <-- binded key

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.String, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='article', lazy=True)

    def __repr__(self):
        return '<Article %r>' % self.id

class Comment(db.Model):
    __bind_key__ = 'comments' # <-- binded key

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.text}', '{self.date}')"