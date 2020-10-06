from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post/<int:post_id>')
def show_user_profile(post_id):
    return 'This post id is:  %d' % post_id


app.run(host='0.0.0.0', debug=True)
