"""Flask is a micro python-based web technology or framework that it very
  enjoyable to work with backend of these application

  our app is initialize in __init__.py file"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

# Create instance of Flask
app = Flask(__name__)

"""Secret-key will help our website to be protected from
from different attacks like CSRF attack which stands for 
Cross-site forgery attack.
To generate a secret-key , open up terminal ... 
start python .... import secrets ... secrets.token_hex(16)."""
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

"""Database URI will help us to set a location for our database """
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# initialize the database
db = SQLAlchemy(app)
# initialize the bcrypt (hashing the password)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Jabiraziz430@gmail.com'
app.config['MAIL_PASSWORD'] = 'Jabir@123'
# initialize the mail or cannot mail with the flask app
mail = Mail(app)

from flaskblog import routes

"""follow the path flaskblog < erorrs < handlers and from there import errors 
which is instance of Blueprint
"""
from flaskblog.erorrs.handlers import errors

"""Now to make the above blueprint work...
register that blueprintwith the app"""
app.register_blueprint(errors)
