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
# app.jinja_env.undefined = StrictUndefined

os.system("source ./projectInfo/secrets.sh") 
API_KEY = os.environ['GOOGLEBOOKS_API_KEY']



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
  

    url = 'https://www.googleapis.com/books/v1/volumes'
    
    payload ={
        'apikey': API_KEY,
        'maxResults':10,
        'q': search
    }
    response = requests.get(url, params=payload)
    data = response.json()
    return render_template("book_search_results.html",books=data['items'])
   
        
   
    # book = data['items'][0]['volumeInfo']
    # title = book['title']
    # author = book['authors'][0]
    # summary = book['description']
    # book_cover = book['imageLinks']['thumbnail']
    


    # logged_in_email = session.get("user_email")    
    # current_user_id = crud.get_id_by_email(logged_in_email)
    # new_book= crud.create_book(title, summary, book_cover, author)
    # book_id = new_book.book_id
    # crud.add_book_to_user_id(current_user_id,book_id)    
   
    

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
        check_book = crud.get_book_by_title(title)
        search_author= crud.get_author(author)
        if check_book == title:
            flash("You already have this book!")
        else:
            new_book= crud.create_book(title, summary, book_cover, author)
            book_id = new_book.book_id
            crud.add_book_to_user_id(current_user_id,book_id)
            print(new_book)
        if search_author != author:
            new_author= crud.create_author(author)
            print(new_author)
           
        



    # if get_books:
    #     for book in get_books:
            
    #         title = request.form.get("title")
    #         print(title)
    #         author = request.form.get("author")
    #         summary = request.form.get("summary")
    #         book_cover = request.form.get("book_cover")
    #         check_book = crud.get_book_by_title(title)
    #         search_author= crud.get_author(author)
    #         if check_book == title:
    #             flash("You already have this book!")
    #         elif search_author != author:
    #             crud.create_author(author)
           
            # new_book= crud.create_book(title, summary, book_cover, author)
            # book_id = new_book.book_id
            # crud.add_book_to_user_id(current_user_id,book_id)
 
   
    return redirect('/find-book')



@app.route('/', methods=["GET","POST"])
def show_library():
    """View users library."""
    logged_in_email = session.get("user_email")
    if crud.get_users is None:
        return redirect('/login')
    if logged_in_email is None:
        flash("You must log in to view your tbr!")
        return redirect('/login')
    
    
    name = crud.get_username_by_email(logged_in_email)
    users_books = crud.get_books_by_email(logged_in_email) 
    print(users_books)
    print('**************')
 
 
    if request.method == 'POST':
        read_status = request.form.getlist('update-status')
        print(read_status)
    
        for book in users_books:
            book_id = book.book_id 

            for stats in read_status: 
                print(stats)
                if stats == "True":
                    print(book.title)
                    crud.update_reading_stats(book_id)
        
        return redirect('/tbr')

        
    return render_template('user_library.html', name=name, users_books=users_books)


@app.route('/set-read-status/<book_id>', methods=["POST"])
def set_book(book_id):
    """Set book status as true or false"""
    #get book by book id(query)
    book = Book.query.get(book_id)

    book.have_read = not book.have_read
    
    #get book status from request.form
    # read_status = request.form.get('status')
  
    # if read_status == "True":
    #     book_stat = False
    #     db.session.add(book_stat)
    #     db.session.commit()
    # elif read_status =="False":
    #     book_stat = True
    #db.seesion.add and commit

    db.session.add(book)
    db.session.commit()

    book_info = {

            'book_id': book_id,
            'have_read': book.have_read
        }
    #return jsonify dictionary
    # {

        #boook attributes: 

    # }

    return book_info
    

@app.route('/tbr')
def show_tbr_list():
    """View users TBR list."""
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        flash("You must log in to view your tbr!")
        return redirect('/login')
    name = crud.get_username_by_email(logged_in_email)
    tbr_list = crud.get_unread_books()
    
    return render_template('user_tbr.html',name=name,tbr_list=tbr_list)



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
    db.session.close()