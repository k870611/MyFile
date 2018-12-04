from sqlalchemy.engine.url import URL
from app import dbSettingsInfo
import mysql.connector


def db_connect():
    return URL(**dbSettingsInfo.DATABASE)


def mysql_connector():
    user = dbSettingsInfo.DATABASE['username']
    password = dbSettingsInfo.DATABASE['password']
    conn = mysql.connector.connect(user=user, password=password, database='server_management')
    return conn

