from flask import Flask
app = Flask(__name__)
from web import view
# config
app.config.from_pyfile('web.conf')
# app.jinja_env.trim_blocks = True
# function to encrypt password
from view import encrypt_password