from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from app.config import Config

import logging

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
csrf.init_app(app)

from app.controller import routes, tank
from app.SQLAlchemyHandler import SQLAlchemyHandler


