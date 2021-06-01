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

    return redner_template('')

@app.route('/add-book',methods=["POST"])
def add_new_book():
    """Add new book to user library."""

    return render_tamplate('')

if __name__ == '__main__':
    # connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)