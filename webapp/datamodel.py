from datetime import datetime
from urlparse import urlparse

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin

from social import *

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'login'

def init_datamodel(app):
    db.init_app(app)
    login_manager.setup_app(app)

class User(db.Model, UserMixin):

    # Basic data
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String)
    email = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # FIXME: modified_at, last_login

    # Traditional authentication
    # FIXME: password (for login w/ e-mail)

    # Facebook OAuth
    facebook_id = db.Column(db.String, unique=True)
    facebook_token = db.Column(db.String)

    # Google OAuth
    google_email = db.Column(db.String, unique=True)
    google_token = db.Column(db.String)

    # Twitter OAuth
    twitter_id = db.Column(db.Integer, unique=True)
    twitter_name = db.Column(db.String(60))
    twitter_token = db.Column(db.String(200))
    twitter_secret = db.Column(db.String(200))

    def save(self):
        # FIXME: save() is a candidate for moving into a common base-class
        db.session.add(self)
        db.session.commit()
        return self

    @property
    def display_name(self):
        return self.fullname or self.email

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @classmethod
    def from_facebook(cls, data):
        info = facebook.get('/me').data

        # Look for an existing user with this Facebook account
        user = cls.query.filter(cls.facebook_id == info['id']).first()
        if user:
            return user

        # Look for an existing user with the same e-mail address
        if info['verified'] and info['email']:
            user = cls.query.filter(cls.email == info['email']).first()
            if user:
                user.facebook_id = info['id']
                user.facebook_token = data['access_token']
                if not user.fullname:
                    user.fullname = info['name']
                return user.save()
            else:
                # Create a new user
                user = cls()
                user.email = info['email']
                user.fullname = info['name']
                user.facebook_id = info['id']
                user.facebook_token = data['access_token']
                return user.save()

    def link_facebook(self, data):
        info = facebook.get('/me').data
        self.facebook_id = info['id']
        self.facebook_token = data['access_token']
        if not self.fullname:
            self.fullname = info['name']
        self.save()

    @classmethod
    def from_google(cls, data):
        token = data['access_token']
        email = get_email_from_google(token)
        if email:
            user = cls.query.filter(cls.email == email).first()
            if not user:
                user = cls()
                user.email = email
                user.google_email = email
                user.google_token = token
                # FIXME: request name
                user.save()
            elif user.google_token != token:
                user.google_email = email
                user.google_token = token
                user.save()
            return user

    def link_google(self, data):
        token = data['access_token']
        email = get_email_from_google(token)
        self.google_email = email
        self.google_token = token
        self.save()

    @classmethod
    def from_twitter(cls, data):
        user = cls.query.filter(cls.twitter_id == data['user_id']).first()
        if not user:
            user = cls()
            user.fullname = data['screen_name']
            user.twitter_id = data['user_id']
            user.twitter_name = data['screen_name']
            user.twitter_token = data['oauth_token']
            user.twitter_secret = data['oauth_token_secret']
            user.save()
        return user

    def link_twitter(self, data):
        self.twitter_id = data['user_id']
        self.twitter_name = data['screen_name']
        self.twitter_token = data['oauth_token']
        self.twitter_secret = data['oauth_token_secret']
        self.save()
