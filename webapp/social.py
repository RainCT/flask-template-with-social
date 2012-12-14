from flask.ext.oauth import OAuth
import httplib2
import json

oauth = OAuth()
http = httplib2.Http()

# FIXME: re-evaluate using flask-social? (first attempt didn't work)

TWITTER_KEY     = ''
TWITTER_SECRET  = ''

FACEBOOK_KEY    = ''
FACEBOOK_SECRET = ''

GOOGLE_KEY      = ''
GOOGLE_SECRET   = ''

providers = ['facebook', 'google', 'twitter']

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=TWITTER_KEY,
    consumer_secret=TWITTER_SECRET
)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_KEY,
    consumer_secret=FACEBOOK_SECRET,
    request_token_params={'scope': 'email'}
)

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
    consumer_key=GOOGLE_KEY,
    consumer_secret=GOOGLE_SECRET)

# FIXME: is there some nicer way to do this? with flask-oauth?
def get_email_from_google(token):
    request = http.request('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=%s' % token)
    data = json.loads(request[1])
    if data['verified_email']:
        return data['email']
