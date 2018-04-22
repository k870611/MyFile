from sqlalchemy.engine.url import URL
import dbSettingsInfo


def db_connect():
    """
    Performs database connection using database settings from dbSettingsInfo.py.
    Return url of sqlalchemy engine
    """
    return URL(**dbSettingsInfo.DATABASE)

