from flask.ext.oauth import OAuth
import httplib2
import json

from settings import config

oauth = OAuth()
http = httplib2.Http()

# FIXME: re-evaluate using flask-social? (first attempt didn't work)

providers = ['facebook', 'google', 'twitter']

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=config['social']['facebook']['key'],
    consumer_secret=config['social']['facebook']['secret'],
    request_token_params={'scope': 'email'})

google = oauth.remote_app('google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=config['social']['google']['key'],
    consumer_secret=config['social']['google']['secret'])

# FIXME: is there some nicer way to do this? with flask-oauth?
def get_email_from_google(token):
    request = http.request('https://www.googleapis.com/oauth2/v1/' \
                           'userinfo?alt=json&access_token=%s' % token)
    data = json.loads(request[1])
    if data['verified_email']:
        return data['email']

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=config['social']['twitter']['key'],
    consumer_secret=config['social']['twitter']['secret'])
