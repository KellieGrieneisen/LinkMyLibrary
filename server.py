""" Server for Link my Library"""
from flask import (Flask, render_template, request, flash, session,
                   redirect)
import crud
# from database import session as db_session
from model import connect_to_db, db
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "$BooksAreCOOL$"
# app.jinja_env.undefined = StrictUndefined

def create_all():
    db.create_all()

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

    user = crud.get_user_by_email(email)
    
    if not user or user.password != password:
        flash("Oops! Something went wrong, check your login info!")
        return redirect('/login')
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
     
    return redirect('/')

@app.route('/user')
def create_new_account():
    """Create new user and add info to library database."""
    
        
    return render_template('create_account.html')

@app.route('/user', methods=["POST"])
def add_new_account():
    """Create new user and add info to library database."""
   
    name = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    if user:
        flash("Email already in use. Try again.")
    else:
        crud.create_user(name, email, password)
        flash("Account created! Please log in.")

        return redirect('/login')

@app.route('/logout')
def logout():
    # logout current user
    session.clear()
    return redirect('/login')


@app.route('/add-book')
def add_new_book_form():
    """Add new book form."""
              
    books = crud.get_books()
    return render_template('add_book.html',books=books)

@app.route('/add-book', methods=["POST"])
def add_new_book():
    logged_in_email = session.get("user_email")
    title = request.form.get("title")
    summary = request.form.get("summary")
    book_cover_path = request.form.get("book_cover")
    full_name = request.form.get("author")
        # genre = request.form.get("genre")

    book = crud.get_book_by_title(title)
    search_author= crud.get_author(full_name)
    if book:
        flash("You already have this book!")
    elif search_author is None:
        crud.create_author(full_name)
    
    user = crud.get_user_by_email(logged_in_email)
    crud.create_book(title, summary, book_cover_path, full_name)
    return redirect('/')



@app.route('/')
def show_library():
    """View users library."""
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        flash("You must log in to view your library!")
    
       
    books = crud.get_books_by_email(logged_in_email)
    current_user = crud.get_username_by_email(logged_in_email)
    return render_template('user_library.html',books=books,current_user=current_user)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
    db.session.close()