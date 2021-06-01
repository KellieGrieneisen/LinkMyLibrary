from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()




class User(db.Model):
    """User info"""

    __tablename__ = 'user'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db. Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    

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
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.genre_id"), nullable=False)
    

    user = db.relationship('User', backref='books')
    author = db.relationship('Author', backref='books')



    def __repr__(self):
        return f'<Book book_id={self.book_id} title={self.title} author_id={self.author_id}>'


class Author(db.Model):
    """Author information"""


    __tablename_ = 'author'

    author_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fullname = db.Column(db.String, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    book = db.relationship('Book', backref='author')

    def __repr__(self):
        return f'<Author author_id={self.author_id} fullname={self.fullname} book_id={self.book_id}>'


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