from app.DbConnector import db_connect


class Config(object):
    SQLALCHEMY_DATABASE_URI = db_connect()
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    CSRF_ENABLED = True
    SECRET_KEY = 'KyLin'
    DATA_PER_PAGE = 2

