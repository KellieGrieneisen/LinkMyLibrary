""" Server for Link my Library"""
from flask import (Flask, render_template, request, flash, session,
                   redirect)

# from database import session as db_session
from model import User, connect_to_db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = "$BooksAreCOOL$"
# app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=["GET"])
def login():
    """Display the homepage and login."""


    return render_template('login.html')
    


@app.route('/login', methods=["POST"])
def handle_login():
    """Check input against user_id's and redirect to user library"""
    # username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user.password == password:
				# Call flask_login.login_user to login a user
        login_user(user)

        flash("Logged in successfully!")
        return redirect('/')
    flash("Oops! Something went wrong, check your login info!")    
    return redirect('/login')

@app.route('/create-acount', methods=["GET"])
def create_new_account():
    """Create new user and add info to library database."""

    return render_template('create_account.html')

@app.route('/create-acount', methods=["POST"])
def add_new_account():
    """Create new user and add info to library database."""
    name = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
     #check if user already exists
    if User.query.filter_by(email=email): # if a user is found, redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect('/create-account')
    
    new_user = User(name=name, email=email, password=password)#check in on password, hash?
    db.session.add(new_user) #add new user info to library db
    db.session.commit()

    return redirect('/login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/add-book', methods=["GET"])
def add_new_book():
    """Add new book to user library."""

    return render_template('add_book.html')

@app.route('/')
# @login_required
def show_library():
    """View users library."""
    if not current_user.is_authenticated:
        return redirect('/login')

    return render_template('user_library.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)