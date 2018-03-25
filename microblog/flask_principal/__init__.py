from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_login import current_user
from flask_principal import identity_loaded,UserNeed,RoleNeed

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

@identity_loaded.connect_via(app)
def on_identity_loaded(sendder,identity):
    identity.user = current_user

    if hasattr(current_user,"id"):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user,"roles"):
        identity.provides.add(RoleNeed(current_user.roles.code))

from app import routes, models
