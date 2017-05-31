from flask import Flask
from flask_login import LoginManager
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config.from_object('config')

Base = declarative_base()

lm = LoginManager(app)
lm.login_view = 'homepage'

from . import views
