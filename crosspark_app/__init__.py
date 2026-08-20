from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SECRET_KEY']='6910'
db = SQLAlchemy(app)

from . import views

if __name__ == '__main__':
    app.run()
