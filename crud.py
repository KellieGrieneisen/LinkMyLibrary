"""CRUD operations."""

from model import db, User, Books_User, Book, Author, connect_to_db, Genre


def create_user(name, email, password):
    """Create and return a new user."""

    user = User(name=name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def add_book_to_user_id(current_user_id,book_id):
    """Connect book to user_id"""
    connection = Books_User(user_id=current_user_id,book_id=book_id)
    db.session.add(connection)
    db.session.commit()

    return connection

def get_genres(books):
    """Query for genres related to users books."""
    genre_list =[]
    for book in books:
        genres = book.genres
        for genre in genres:
            print(genre.genre_id)
            if genre.name not in genre_list:
                genre_list.append(genre.name)
    return sorted(genre_list)


def create_book(title, summary, book_cover, author,genres):
    """Create and return book to user library."""
    book_author = Author(full_name=author)
    new_book = Book(title=title, summary=summary, book_cover_path=book_cover)
    book_author.books.append(new_book)
    if genres == None:
        db.session.add(new_book)
        db.session.commit()

        return new_book

    for genre in genres:
        print(genre)
        book_genres = Genre.query.filter(Genre.name==genre).first()
        print('***************')
        print(book_genres)
        if book_genres is None:
            new_genres = Genre(name=genre)
            new_genres.books.append(new_book)
        else:
            book_genres.books.append(new_book)
        
    
    db.session.add(new_book)
    db.session.commit()

    return new_book

def create_author(full_name):
    """Add new author to library database."""
    new_author = Author(full_name = full_name)

    db.session.add(new_author)
    db.session.commit()
    return new_author

def get_book_by_title(title):
    """Return a book by title."""

    return Book.query.filter(Book.title == title).first()

def get_author(author):
    """Return books by author."""

    return Author.query.filter(Author.full_name==author).first()


def get_books_by_email(email):
    """Display all books assigned to current user"""
    # connection = Books_User(user_id=current_user_id)
    current_user = User.query.filter(User.email == email).first()

    book_info = current_user.book

    return book_info


def update_reading_stats(book_id):
    update_status = Book.query.filter_by(book_id=book_id).first()
    update_status.have_read = False
    db.session.add(update_status)
    db.session.commit()
    return update_status
   

def get_username_by_email(email):
    current_user = User.query.filter_by(email = email).first()
    #grabbing users name from logged in email 
    # to give customized experience
    user_name = current_user.name

    return user_name

def get_id_by_email(email):
    current_user = User.query.filter_by(email = email).first()
    u_id = current_user.user_id

    return u_id


def get_books():
    """Return all books."""

    return Book.query.all()

def get_unread_books(user_id):
    """Return all books in users library where have_read is False."""
    user = User.query.filter_by(user_id=user_id).first()
    #list to hold books user has not yet read
    books_unread =[]
    for book in user.book:
        #iterate through users books and select books 
        #with a bollenvalue of false for have_read
        if book.have_read ==False:
            #add book to unread book list
            books_unread.append(book)
    
    #return book list to user for tbr list
    return books_unread
