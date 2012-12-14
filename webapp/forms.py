from flask.ext.wtf import Form, TextField, validators

class LoginForm(Form):

    email = TextField('Email', [validators.Required()])
    password = TextField('Password', [validators.Required()])

    # FIXME: implement this & stuff
    # Example: http://flask.pocoo.org/snippets/64/

class EmailForm(Form):

    email = TextField('email', [validators.Required()])
