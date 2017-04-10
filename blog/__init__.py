import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import BASE_DIR


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
open_id = OpenID(app, os.path.join(BASE_DIR, 'tmp'))

from blog import views, models
