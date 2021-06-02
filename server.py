""" Server for Link my Library"""
from flask import (Flask, render_template, request, flash, session,
                   redirect)

# from database import session as db_session


app = Flask(__name__)


@app.route('/')
def homepage():
    """Display the homepage."""

    return render_template('homepage.html')

@app.route('/login', methods=["POST"])
def handle_login():
    """Check input against user_id's and redirect to user library"""
    email = request.form.get('email')
    password = request.form.get('password')

    # user = 

    return redirect('/user-library')

@app.route('/add-book')
def add_new_book():
    """Add new book to user library."""

    return render_template('add_book.html')

@app.route('/user-library')
def show_library():
    """View users library."""

if __name__ == '__main__':
    # connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)