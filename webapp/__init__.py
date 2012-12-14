from flask import Flask, session, request

from datamodel import *
from settings import config

app = Flask(__name__)

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
