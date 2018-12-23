# -*- coding: utf-8 -*-
import os
import json

from flask import render_template, jsonify

from app import app
from app.config import Config
from app.controller.temp_predict import WeatherPredict
from app.controller.server_temp_info import ServerTemp


@app.route('/weather_predict', methods=['GET', 'POST'])
def weather_predict():
    model = WeatherPredict()
    data_all = Config.ALL_MONTH_TEMP["server_temp"]
    # print(data_all)

    if data_all == "":
        return jsonify({'info': 'fail'})

    model.weather_data = data_all

    predict_date = str(model.predict_weather_linear_regression(20181222170000))
    output_date = str(predict_date)[:4] + "/" + str(predict_date)[4:6] + "/" + str(predict_date)[6:8] + " " + \
                  str(predict_date)[8:10] + ":" + str(predict_date)[10:12] + ":" + str(predict_date)[12:]

    return jsonify({'info': 'success', 'temp': output_date})


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
    if not os.path.exists(os.path.join(dir_path, "server_temp_info.json")):
        data_downloader = ServerTemp()
        data_downloader.server_temp_json()

    with open(os.path.join(dir_path, "server_temp_info.json"), "r") as fr:
        weather_data = json.load(fr)

    all_temp = {"server_temp": []}

    output_data ={}
    for data in weather_data["server_temp_info"]:
        time = data["time"]
        value = data["value"]

        temp_data = {"time": time.replace("-","").replace(":","").replace(" ", ""), "value": value}
        all_temp["server_temp"].append(temp_data)

        output_data[time] = value
    # print(output_data)
    # print(all_temp)

    Config.ALL_MONTH_TEMP = all_temp
    Config.YEAR_MONTH_TEMP = output_data

    return render_template("hackathon_predict_temp.html")
