# -*- coding: utf-8 -*-
from flask import render_template

from app import app
from app.controller.temp_predict import WeatherPredict


@app.route('/')
def index():
    return render_template("temp20180621.html")




