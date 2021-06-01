""" Server for Link my Library"""
from flask import (Flask,render_template, request, flash, session,
                   redirect)
from model import 

app = Flask(__name__)


@app.route('/')
def homepage():
    """Display the homepage."""

    return render_template('homepage.html')




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)