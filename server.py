""" Server for Link my Library"""
from flask import (Flask, render_template, request, flash, session,
                   redirect)

# from database import session as db_session
from model import User, connect_to_db

app = Flask(__name__)
app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined




@app.route('/login', methods=["GET"])
def login():
    """Display the homepage and login."""


    return render_template('login.html')
    


@app.route('/login', methods=["POST"])
def handle_login():
    """Check input against user_id's and redirect to user library"""
    email = request.form.get('email')
    password = request.form.get('password')


    user = User.query.filter_by(email=email).first()
    if not user or not password:
        flash('You are not a current user, check login info!')
        return redirect('/login')
    
    return redirect('/')

@app.route('/create-acount', methods=["GET"])
def create_new_account():
    """Create new user and add info to library database."""

    return render_template('create_account.html')

@app.route('/create-acount', methods=["POST"])
def add_new_account():
    """Create new user and add info to library database."""
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user: # if a user is found, redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect('/create-account')
    new_user = User(email=email, name=name, password=password)#check in on password, hash?
    db.session.add(new_user)
    db.session.commit()

    return redirect('/login')


@app.route('/add-book', methods=["GET"])
def add_new_book():
    """Add new book to user library."""

    return render_template('add_book.html')

@app.route('/')
def show_library():
    """View users library."""
    # if 'user' not in session:
    #     return redirect('/login')

    return render_template('user_library.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)