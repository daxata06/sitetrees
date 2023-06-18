from datetime import datetime
from flask_login import UserMixin, LoginManager, login_manager
from flask_security import RoleMixin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


import os


newsite = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

newsite.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
newsite.config['SQLALCHEMY_DATABASE_URI']='sqlite:///registr.db'
newsite.config['SQLALCHEMY_DATABASE_URI']='sqlite:///UserModifications.db'
newsite.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
newsite.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

newsite.secret_key = os.urandom(24) 
login_manager = LoginManager()
login_manager.init_app(newsite)

db = SQLAlchemy(newsite)


def __str__(self):
        return self.name

class registr(db.Model, UserMixin):
    username = db.Column(db.String, unique=True, primary_key=True)
    password = db.Column(db.Integer, unique=True)
    def get_id(self):
        return str(self.username) 


class UserModifications(db.Model):
    usernick = db.Column(db.String)
    itemname = db.Column(db.String)
    itemprice = db.Column(db.String)
    itemdescr = db.Column(db.String, primary_key=True)
    itemphoto = db.Column(db.BLOB)

    # Flask - Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # Flask-Security
    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def get_id(self):
        return self.username
    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    @login_manager.user_loader
    def load_user(user_id):
      return db.session.query(registr).get(user_id)