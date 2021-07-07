""" Server for Link my Library"""
from flask import (Flask, render_template, request, flash, session,
                   redirect)
import crud
import requests
import os
import json
# from database import session as db_session
from model import connect_to_db, db, Book
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "$BooksAreCOOL$"
app.jinja_env.undefined = StrictUndefined

os.system("source ./projectInfo/secrets.sh") 
API_KEY = os.environ['GOOGLEBOOKS_API_KEY']

# def create_all():
#     db.create_all()



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
        # return redirect('/login')
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
        return redirect('/user')
    else:
        crud.create_user(name, email, password)
        flash("Account created! Please log in.")
        return redirect('/login')

@app.route('/logout')
def logout():
    # logout current user
    session.clear()
    return redirect('/login')


# @app.route('/add-book')
# def add_new_book_form():
#     """Add new book form."""
#     logged_in_email = session.get("user_email")           
#     books = crud.get_books()
#     # b = crud.get_books_by_email(logged_in_email)
#     return render_template('add_book.html',books=books)

# @app.route('/add-book', methods=["POST"])
# def add_new_book():
#     logged_in_email = session.get("user_email")
#     title = request.form.get("title")
#     summary = request.form.get("summary")
#     book_cover_path = request.form.get("book_cover")
#     full_name = request.form.get("author")
#         # genre = request.form.get("genre")

#     book = crud.get_book_by_title(title)
#     search_author= crud.get_author(full_name)
#     if book:
#         flash("You already have this book!")
#     elif search_author is None:
#         crud.create_author(full_name)
    
#     current_user_id = crud.get_id_by_email(logged_in_email)
#     new_book= crud.create_book(title, summary, book_cover_path, full_name)
#     book_id = new_book.book_id
#     crud.add_book_to_user_id(current_user_id,book_id)
#     return redirect('/')


@app.route('/find-book')   
def show_book_form():
    """Book search form."""

    return render_template('search_book.html') 


@app.route('/find-book', methods=["POST"])
def search_for_book():
    """Search for Books matching description in Google Books."""
    search = request.form.get('book-search', '')
  
    if not search:
        return redirect('/find-book')
    url = 'https://www.googleapis.com/books/v1/volumes'
    # first page of search results
    payload ={
        'apikey': API_KEY,
        'startIndex':0,
        'maxResults':20,
        'q': search
    }
    response = requests.get(url, params=payload)
    data = response.json() 

    # next page search results
    payload2 ={
        'apikey': API_KEY,
        'startIndex':21,
        'maxResults':20,
        'q': search
    }
    
    response2 = requests.get(url, params=payload2)
    data2=response2.json()

    return render_template("book_search_results.html", books=data['items'], books2=data2['items'], search=search)
   
     
   
    

@app.route('/add-searched-book', methods=["POST"])
def add_searched_book():
    logged_in_email = session.get("user_email")    
    current_user_id = crud.get_id_by_email(logged_in_email)
    
    get_ids = request.form.getlist('addbooks')
    print(get_ids)
    
    
    
    for id in get_ids:
        url = f'https://www.googleapis.com/books/v1/volumes/{id}'
        payload ={
            'apikey': API_KEY,
        }
        response = requests.get(url, params=payload)
        data = response.json()
        print(data)
        title = data['volumeInfo']['title']
        author = data['volumeInfo']['authors'][0]
        book_cover = data['volumeInfo']['imageLinks']['thumbnail']
        summary = data['volumeInfo']['description']
        if 'categories' in data['volumeInfo']:
            genres = data['volumeInfo']['categories']
        else:
            genres = None
        check_book = crud.get_book_by_title(title)
        search_author= crud.get_author(author)
        if search_author is None:
            new_author= crud.create_author(author)
            print(new_author)
        if not check_book:
            new_book= crud.create_book(title, summary, book_cover, author,genres)
            book_id = new_book.book_id
            crud.add_book_to_user_id(current_user_id,book_id)
            print(new_book)
        else:
            for user in check_book.user:
                if user.email == logged_in_email:
                    flash("You already have this book!")
                else:
                    crud.add_book_to_user_id(current_user_id,check_book.book_id)
        
    return redirect('/find-book')



@app.route('/', methods=["GET","POST"])
def show_library():
    """View users library."""
    logged_in_email = session.get("user_email")
    if crud.get_users is None or logged_in_email is None:
        return redirect('/login')
    
    #get users name for more personalized experience
    name = crud.get_username_by_email(logged_in_email)
    #call for books only associated with the current user in session
    users_books = crud.get_books_by_email(logged_in_email) 

        
    return render_template('user_library.html', name=name, users_books=users_books)


@app.route('/set-read-status/<book_id>', methods=["POST"])
def set_book(book_id):
    """Set book status as true or false"""
    #get book by book id(query)
    book = Book.query.get(book_id)
    #toggle the T/F boolean value in database
    book.have_read = not book.have_read
    
    #add and commit update
    db.session.add(book)
    db.session.commit()

    book_info = {

            'book_id': book_id,
            'have_read': book.have_read
        }

    return book_info


    

@app.route('/tbr')
def show_tbr_list():
    """View users TBR list."""
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        flash("You must log in to view your tbr!")
        return redirect('/login')
    name = crud.get_username_by_email(logged_in_email)
    user_id = crud.get_id_by_email(logged_in_email)
    tbr_list = crud.get_unread_books(user_id)
    
    return render_template('user_tbr.html',name=name,tbr_list=tbr_list)

@app.route('/genres', methods=["GET","POST"])
def show_genres_in_library():
    """Display Genres in users library."""
    logged_in_email = session.get("user_email")
    users_books = crud.get_books_by_email(logged_in_email)
    book_genres = crud.get_genres(users_books)
    
    if request.method == "POST":

        search = request.form.get('genres')
  

        url = 'https://www.googleapis.com/books/v1/volumes'
        # first page search results
        payload ={
            'apikey': API_KEY,
            'startIndex':0,
            'maxResults':20,
            'q': search
        }
        response = requests.get(url, params=payload)
        data = response.json()

        # next page search results
        payload2 ={
            'apikey': API_KEY,
            'startIndex':21,
            'maxResults':20,
            'q': search
        }

        response2 = requests.get(url, params=payload2)
        data2=response2.json()
        return render_template('book_search_results.html',books=data['items'],books2=data2['items'], search=search)

    return render_template('book-recs.html', book_genres=book_genres)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
    db.session.close()