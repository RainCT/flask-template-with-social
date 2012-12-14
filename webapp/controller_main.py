from flask import Flask
from flask import render_template

from webapp import app

@app.route('/')
def home():
    return render_template('home.html')

#@app.errorhandler(404)
#def page_not_found(error):
#    return render_template('404.html'), 404
