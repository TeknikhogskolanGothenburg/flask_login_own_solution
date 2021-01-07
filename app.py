from flask import Flask, render_template, request, redirect, url_for, session
import os
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sql3")
app.config["SECRET_KEY"] = "thisisthesecretkey"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.VARCHAR(255))


def is_authenticated():
    return 'username' in session


def authenticated(fail_route='index'):
    def decorator(route):
        @wraps(route)
        def wrapper(*args, **kwargs):
            if is_authenticated():
                return route(*args, **kwargs)
            return redirect(url_for(fail_route))
        return wrapper
    return decorator


@app.route('/')
def index():
    return render_template('index.html', authenticated=is_authenticated())


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    first = request.form['first']
    last = request.form['last']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(str.encode(password), salt)
    user = User(
        first_name=first,
        last_name=last,
        email=email,
        username=username,
        password=hashed_password
    )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('signin'))

@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signin', methods=['POST'])
def signin_post():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
        if bcrypt.checkpw(str.encode(password), user.password):
            session['username'] = user.username
            return redirect(url_for('profile'))
    return render_template('error.html')


@app.route('/profile')
@authenticated()
def profile():
    user = User.query.filter_by(username=session['username']).first()
    return render_template('profile.html', username=user.first_name)


@app.route("/signout")
def signout():
    session.clear()
    return render_template('index.html', authenticeted=is_authenticated())


@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run()
