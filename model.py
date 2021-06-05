from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri='postgresql:///library', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class User(db.Model,UserMixin):
    """User info"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db. Column(db.String(30))
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    book =db.relationship('Book', secondary="books_user")
   

    def __repr__(self):
        return f'<User user_id={self.user_id} name={self.name} email={self.email}>'


class Books_User(db.Model):
    """Association table for books and users."""

    __tablename__ = "books_user"

    book_user_id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(
        db.Integer, db.ForeignKey("books.book_id"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
   
# ---------------------------------------------------------------------------------------
# All books that belong to a user:
# - get the user_id =>  (logged_in_user_id = 8)
# - query Books_User table with that user_id
#     >> all_books = Books_User.query.filter_by(user_id=logged_in_user_id)
#     [<Books_User user_id=8, book_id=78>, <Books_User user_id=8, book_id=5>,<Books_User user_id=8, book_id=22>]

# - get the book id's from this list of Books_User objects
#     >> book_list = []
#     >> for book in all_books: # book = <Books_User user_id=8, book_id=78>
#         id = book.book_id # 78
#         book_obj = Book.query.get(id) # due to the unique primary key  <Book book_id=78 title="How to think like a computer scientist"
#         book_list.append(book_obj)
#     return book_list
    
class Book(db.Model):
    """Book info"""

    __tablename__ = 'books'

    book_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)

    title = db.Column(db.String(50))
    summary = db.Column(db.Text)
    book_cover_path = db.Column(db.String)
    
   
    # user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'), nullable=False)
    

    author = db.relationship('Author', backref='books')
    user =db.relationship('User', secondary="books_user")
    genres = db.relationship(
        "Genre", secondary="books_genres")

    def __repr__(self):
        return f'<Book book_id={self.book_id} title={self.title} author={self.author}>'

# class Books_Author(db.Model):
#     """Association table for books and genres."""

#     __tablename__ = "books_author"

#     book_user_id = db.Column(db.Integer, primary_key=True)

#     book_id = db.Column(
#         db.Integer, db.ForeignKey("books.book_id"))
#     author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'))


class Author(db.Model):
    """Author information"""


    __tablename_ = 'author'

    author_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    

    def __repr__(self):
        # return f'<Author author_id={self.author_id} full_name={self.full_name}>'
        return f'{self.full_name}'


class BookGenre(db.Model):
    """Association table for books and genres."""

    __tablename__ = "books_genres"

    book_genre_id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(
        db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    
    genre_id = db.Column(
        db.Integer, db.ForeignKey("genres.genre_id"), nullable=False)


class Genre(db.Model):  
    """Literary genre."""

    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __repr__(self):
        return f'<Genre genre_id={self.genre_id} name={self.name}>'

if __name__ == '__main__':
    from server import app
    connect_to_db(app)