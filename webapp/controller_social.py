from flask import abort, flash, g, jsonify, request, redirect, \
    render_template, send_file, session, url_for
from flask.ext.login import current_user, login_user, logout_user, \
     login_required

from webapp import app
from datamodel import *

import social
from forms import *
from social import *

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login_user(user)
        # redirect(next)
        pass
    return render_template('login.html', form=form)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup/email')
def signup_email():
    form = LoginForm()
    if form.validate_on_submit():
        # login_user(user)
        # redirect(next)
        pass
    return render_template('signup-email.html', form=form)

@app.route('/login/<provider>', methods=['GET', 'POST'])
def social_login(provider):
    if provider not in social.providers:
        abort(404)
    #FIXME: save return_url in session and redirect once authenticated;
    #       Google doesn't like if it's in GET
    #return_url = request.args.get('next') or request.referrer or url_for('myapps')
    url = url_for('%s_authorized' % provider, _external=True)
    return getattr(social, provider).authorize(callback=url)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/oauth_authorized_facebook')
@facebook.authorized_handler
def facebook_authorized(resp):
    return _social_authorized('facebook', resp)

@app.route('/oauth_authorized_google')
@google.authorized_handler
def google_authorized(resp):
    return _social_authorized('google', resp)

@app.route('/oauth_authorized_twitter')
@twitter.authorized_handler
def twitter_authorized(resp):
    return _social_authorized('twitter', resp)

def _social_authorized(provider, data):
    if provider not in social.providers:
        abort(404)

    if data is None:
        flash('You denied the request to sign in.')
        return redirect(url_for('login'))

    token = data.get('access_token', data.get('oauth_token', ''))
    secret = data.get('oauth_token_secret', '')

    setattr(g, '%s_token' % provider, token)
    setattr(g, '%s_secret' % provider, secret)

    if current_user.is_active():
        getattr(current_user, 'link_%s' % provider)(data)
        flash('%s has been linked with your account!' % provider)
        return redirect(url_for('my_apps'))

    user = getattr(User, 'from_%s' % provider)(data)
    if user:
        login_user(user)
        flash('You were signed in!')

    # FIXME: redirect to wherever the user was
    return redirect(url_for('home'))

@facebook.tokengetter
def get_facebook_token():
    return _social_token('facebook')

@google.tokengetter
def get_google_token():
    return _social_token('google')

@twitter.tokengetter
def get_twitter_token():
    return _social_token('twitter')

def _social_token(provider):
    assert provider in social.providers
    if hasattr(g, '%s_token' % provider):
        # This provides access to tokens until the user account is created
        token = getattr(g, '%s_token' % provider)
        secret = getattr(g, '%s_secret' % provider)
        return token, secret
    if not current_user.is_anonymous():
        token = getattr(current_user, '%s_token' % provider)
        secret = getattr(current_user, '%s_secret' % provider, None)
        return token, secret
