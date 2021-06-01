from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


db.app = flask_app
db.init_app(flask_app)

print('Connected to the db!')

class User(db.Model):
    """User info"""

    __tablename__ = 'user'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db. Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    books = db.relationship( "Book",  backref="user", viewonly=True)
    

    def __repr__(self):
        return f'<User user_id={self.user_id} name={self.name} email={self.email}>'



class Book(db.Model):
    """Book info"""

    __tablename__ = 'books'

    book_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)

    title = db.Column(db.String)
    summary = db.Column(db.Text)
    book_cover_path = db.column(db.String)
    read =db.Column(db.Boolean)


    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'), nullable=False)
    genres = db.relationship(
        "Genre", secondary="books_genres", backref="books")



    def __repr__(self):
        return f'<Book book_id={self.book_id} title={self.title} author_id={self.author_id}>'


class Author(db.Model):
    """Author information"""


    __tablename_ = 'author'

    author_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    full_name = db.Column(db.String, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    book = db.relationship('Book', backref='author')

    def __repr__(self):
        return f'<Author author_id={self.author_id} full_name={self.full_name} book={self.book}>'


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

if __name__ == '__main__':
    from server import app
    # connect_to_db(app)