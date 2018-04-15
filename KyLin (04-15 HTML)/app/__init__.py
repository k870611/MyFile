from flask import Flask
from flask_login import LoginManager, current_user
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config

import logging

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
csrf.init_app(app)

login = LoginManager(app)
login.login_view = 'login'
login.login_message = "Please login again(session is expire or need login to access)"

from app.web import accmanagement, eventlist, itmanagement, role, routes, serverinfo, log, online
from app.SQLAlchemyHandler import SQLAlchemyHandler
from app import error

principal = Principal()
principal.init_app(app)


@identity_loaded.connect_via(app)
def on_identity_loaded(sendder, identity):
    identity.user = current_user

    if hasattr(current_user, "acc_management_id"):
        identity.provides.add(UserNeed(current_user.acc_management_id))

    if hasattr(current_user, "role_id"):
        identity.provides.add(RoleNeed(current_user.role.role_auth))

db_handler = SQLAlchemyHandler()
db_handler.setLevel(logging.INFO)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(db_handler)
