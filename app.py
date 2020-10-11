from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# configuration (location) of the FIRST database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# binds keys to the rest of the databases (there is only one named 'posts.db')
app.config['SQLALCHEMY_BINDS'] = {'posts': 'sqlite:///posts.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# model for users.db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime,  default=datetime.utcnow)

    def __repr__(self):
        return 'User %r' % self.id

# model for posts.db
class Article(db.Model):
    __bind_key__ = 'posts' # <-- binded key

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


