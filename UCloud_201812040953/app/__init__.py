from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
csrf.init_app(app)

login = LoginManager(app)
login.login_view = 'login'
login.login_message = "Please login again(session is expire or need login to access)"

from app.controller import routes, tank, ucloud
