# -*- coding: utf-8 -*-
import os
import json
import datetime

from flask import render_template, jsonify, request

from app import app
from app.config import Config
from app.controller.json_getter import WeatherCrawler
from app.controller.temp_predict import WeatherPredict


@app.route('/weather_predict', methods=['GET', 'POST'])
def weather_predict():
    predict_time = request.form.get('predict_date', "")
    predict_time = int(str(predict_time).replace("-", ""))
    month = int(str(predict_time).replace("-", "")[4:6])

    model = WeatherPredict()
    data_all = Config.ALL_MONTH_TEMP
    predict_data = data_all.get(str(month), "")

    if predict_data == "":
        return jsonify({'info': 'fail'})

    data_x = []
    data_y = []

    for data in predict_data:
        data_x.append(data["time"])
        data_y.append(data["value"])

    model.data_x = data_x
    model.data_y = data_y

    temp = str(model.predict_weather_linear_regression(predict_time))[1:-1]
    return jsonify({'info': 'success', 'temp': temp})


@app.route('/data_ReCrawl', methods=['GET', 'POST'])
def data_re_crawl():
    data_downloader = WeatherCrawler()
    data_downloader.temp_crawler()

    return jsonify({'info': 'success'})


@app.route('/data/<string:data_name>')
def send_data_to_d3(data_name):
    if data_name == "temp_data":
        temp_data = Config.YEAR_MONTH_TEMP

        output_json = []
        for key, value in temp_data.items():
            output_json.append({"time": key, "value": value})

        return jsonify(output_json)



@app.route('/')
def index():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(dir_path, "dongli_history_temperature.json")):
        data_downloader = WeatherCrawler()
        data_downloader.temp_crawler()

    with open(os.path.join(dir_path, "dongli_history_temperature.json"), "r") as fr:
        weather_data = json.load(fr)

    month_date = ""
    month_temp_value = []
    month_temp_data = []


    year_month_temp = {}
    all_month_temp = {"1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": []}

    idx = 0
    for data in weather_data:
        value = data["value"]
        temp_time = datetime.datetime.strptime(data["time"], "%Y%m%d").date()
        month_temp_value.append(value)
        month_temp_data.append(data)

        if month_date == "":
            month_date = temp_time + datetime.timedelta(days=30)

        if datetime.datetime.strptime(data["time"], "%Y%m%d").date() > month_date:
            month_date = temp_time + datetime.timedelta(days=30)
            time_stamp = (temp_time + datetime.timedelta(days=-30)).strftime("%Y")

            if time_stamp not in year_month_temp.keys():
                year_month_temp[time_stamp] = []

            month = idx % 12 + 1
            all_month_temp[str(month)] += month_temp_data

            avg_temp = round(sum(month_temp_value) / float(len(month_temp_value)), 2)
            year_month_temp[time_stamp].append(avg_temp)

            month_temp_value = []
            month_temp_data = []
            idx += 1

    Config.ALL_MONTH_TEMP = all_month_temp
    Config.YEAR_MONTH_TEMP = year_month_temp

    return render_template("hackathon_predict_temp.html")
