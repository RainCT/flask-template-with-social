from flask import Flask, session, request
import json
import traceback

from datamodel import *

app = Flask(__name__)

def fatal(msg):
    stars = '*' * len(msg)
    print '\n%s\n%s\n%s\n' % (stars, msg, stars)
    traceback.print_exc()
    raise SystemExit

try:
    CONFIG_FILE = 'webapp/config.json'
    config = json.load(open(CONFIG_FILE))
except Exception:
    fatal('Error parsing configuration file: %s' % CONFIG_FILE)

app.secret_key = str(config['global']['secret_key'])
app.config['SQLALCHEMY_DATABASE_URI'] = config['global']['database_uri']

init_datamodel(app)

@app.before_request
def request_setup():
    # Fix URL (strip trailing slashes)
    if request.path != '/' and request.path.endswith('/'):
        return redirect(request.path[:-1], code=301)

    # FIXME: figure out language & stuff
    pass

import webapp.controller_main
import webapp.controller_social
