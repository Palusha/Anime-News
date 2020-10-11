from flask import Flask, render_template, request, redirect
from main import User, Article, app, db

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
    """ Sign up page """
    if request.method == 'POST':
        # gets username and passwords from <input> on signup.html
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
            # adds created user to the users.db
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
    """ Log in page """
    if request.method == 'POST':
        # gets username and password from <input> on login.html
        lgn = request.form.get("username")
        passw = request.form.get("password")
        # finds the first data in the users.db 
        # matched by the provided username
        user = User.query.filter_by(username=lgn).first()
        try:
            # for username and password "admin" moves to create-post.html
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
    """ Create article page """
    if request.method == "POST":
        title = request.form.get("title")
        post_info = request.form.get("text")
        new_post = Article(title=title, text=post_info)

        # adds created article to the posts.db
        db.session.add(new_post)
        db.session.commit()

    return render_template('create-post.html')


@app.route('/delete-post/', methods=['POST', 'GET'])
def delete_post():
    """ Delete article page """
    return render_template('delete-post.html', articles=Article.query.all())


@app.route('/delete-post/<int:id>')
def delete(id):
    # clicking on the link deletes an article by it's id
    db.session.query(Article).filter(Article.id == id).delete()
    db.session.commit()
    return redirect("/delete-post")

if __name__ == "__main__":
    # runs the app in the debug mode (should be turned off)
    # and allows people in LAN connect to the website
    app.run(debug=True, host='0.0.0.0')