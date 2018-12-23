import json
import math
import os
import datetime
import random

import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


class WeatherPredict:
	def __init__(self):
		dir_path = os.path.abspath(os.path.dirname(__file__))
		with open(os.path.join(dir_path, "server_temp_info.json"), "r") as fr:
			self.weather_data = json.load(fr)

		self.data_x = []
		self.data_y = []

	def draw_picture(self):
		# data_y_idx = [i for i in range(len(self.data_y))]
		x = np.array(self.self_x)
		y = np.array(self.data_y)

		plt.rc('font', size=15)
		plt.scatter(x, y, 60, color='blue', marker='o', linewidth=3, alpha=0.8)

		plt.xlabel('date')
		plt.ylabel('temp')
		plt.title('temp_analysis')

		plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='both', alpha=0.4)
		plt.show()

	def predict_weather_linear_regression(self, date):
		overheat_date = date
		predict_temp = 0

		while predict_temp < 60 or predict_temp >65:
			x = []
			y = []

			overheat_date = date
			predict_temp = 0

			for data in self.weather_data:
				x.append(int(data["time"]))
				y.append(round(float(data["value"]) + random.random(), 2))

			x = np.array(x)
			y = np.array(y)
			x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=0)

			clf = linear_model.LinearRegression()
			clf.fit(x_train.reshape(-1, 1).astype(np.float64), y_train)

			for i in range(86400):
				date_to_datetime = datetime.datetime.strptime(str(overheat_date), "%Y%m%d%H%M%S") + datetime.timedelta(seconds=i)
				overheat_date = date_to_datetime.strftime("%Y%m%d%H%M%S")

				predict_temp = float(clf.predict(np.array([int(overheat_date)]).reshape(-1, 1))[0])

				if 60 < predict_temp < 61:
					break

			# print("predict date :is {} , temp is :{} ".format(overheat_date, round(predict_temp, 4)))

		print("\n----------------------------------------------------")
		print("predict date :is {} , temp is :{} ".format(overheat_date, round(predict_temp, 4)))

		return overheat_date


if __name__ == "__main__":
	print("Start predict-------")
	model = WeatherPredict()
	model.predict_weather_linear_regression(20181222170000)



