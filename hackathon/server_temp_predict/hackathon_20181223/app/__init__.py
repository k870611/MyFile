from flask import Flask

from app.config import Config

app = Flask(__name__)

from app.controller import routes
