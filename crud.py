"""CRUD operations."""

from model import db, User, Books_User, Book, Author, connect_to_db


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
    all_books = Books_User.query.filter_by(connection)
    user_bookshelf = []

    for book in all_books:
        B_id = book.book_id
        book_obj = Book.query.get(B_id)
        user_bookshelf.append(book_obj)
    return user_bookshelf




def create_book(title, summary, book_cover_path, full_name):
    """Create and return book to user library."""
    book_author = Author(full_name=full_name)
    new_book = Book(title=title, summary=summary, book_cover_path=book_cover_path)
    book_author.books.append(new_book)

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

# def get_books_by_email(logged_in_email):
#     current_user = User.query.filter_by(logged_in_email = email).first()
#     user_books = current_user.books
    
#     return user_books

def get_books_by_user_id(current_user_id):
    """Display all books assigned to current user"""
    # connection = Books_User(user_id=current_user_id)
    
    book_info = user.books

    return book_info

def get_username_by_email(email):
    current_user = User.query.filter_by(email = email).first()
    user_name = current_user.name

    return user_name

def get_id_by_email(email):
    current_user = User.query.filter_by(email = email).first()
    u_id = current_user.user_id

    return u_id

# def get_author_by_author_id(author_id):
#     """Return Author ID"""

#     return Author.query.filter(Author.author_id == )

def get_books():
    """Return all books."""

    return Book.query.all()
