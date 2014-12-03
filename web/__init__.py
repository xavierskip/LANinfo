from flask import Flask
app = Flask(__name__)
# app.jinja_env.trim_blocks = True
app.config.from_pyfile('web.conf')
from web import view
from view import encrypt_password