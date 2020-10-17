from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'this_definetly_has_to_be_changed'
# allows to connect to the second database with articles
app.config['SQLALCHEMY_BINDS'] = {'posts': 'sqlite:///posts.db', 'comments' : 'sqlite:///comments.db'} # bind key is used in models.py
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# code below should be exactly here after app and db creating
from controllers import auth
app.register_blueprint(auth) # connects to the main API functions in controllers.py

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')