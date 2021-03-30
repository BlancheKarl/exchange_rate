from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a new Flask application
app = Flask(__name__)

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////exchange.db'
db = SQLAlchemy(app)

# Define a class for the Artist table
class exchange(db.Model):
    currency = db.Column(db.String)
    br = db.Column(db.Float)
    cbr = db.Column(db.Float)
    sr = db.Column(db.Float)
    csr = db.Column(db.Float)

# Create the table
db.create_all()