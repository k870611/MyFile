import json
import datetime
import math

import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


class WeatherPredict:
	def __init__(self):
		with open("dongli_history_temperature.json", "r") as fr:
			self.weather_data = json.load(fr)
		self.data_x = []
		self.data_y = []

		for data in self.weather_data:
			self.data_x.append(data["time"])
			self.data_y.append(data["value"])

	def draw_picture(self):
		data_y_idx = [i for i in range(len(self.data_y))]
		x = np.array(data_y_idx)
		y = np.array(self.data_y)

		plt.rc('font', size=15)
		plt.scatter(x, y, 60, color='blue', marker='o', linewidth=3, alpha=0.8)

		plt.xlabel('date')
		plt.ylabel('temp')
		plt.title('temp_analysis')

		plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='both', alpha=0.4)
		# plt.show()

	def predict_weather_linear_regression(self, date):
		x = np.array(self.data_x)
		y = np.array(self.data_y)

		x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=0)

		clf = linear_model.LinearRegression()
		clf.fit(x_train.reshape(-1, 1).astype(np.float64), y_train)

		predict_datetime = clf.predict(np.array([int(date)]).reshape(-1, 1))
		datetime = str(date)[:4]+"/"+str(date)[4:6]+"/"+str(date)[6:]
		print("predict {} is: ".format(datetime), predict_datetime)

		deviation_sum = ((y_test - list(clf.predict(np.array(x_test).reshape(-1, 1).astype(np.float64)))) ** 2).sum()

		print("Data number: ", len(y_test))
		print("Deviation sqrt sum: ", deviation_sum)
		print("Temp Deviation: ", math.sqrt(deviation_sum / len(y_test)))


if __name__ == "__main__":
	print("Start predict-------")
	# model = WeatherPredict()
	# model.predict_weather_linear_regression(20011000)
	with open("dongli_history_temperature.json", "r") as fr:
		weather_data = json.load(fr)

	month_date = ""
	month_temp = []
	temp_data = []
	year_month_temp = {}

	all_month_temp = {"1": [], "2":[], "3":[], "4":[], "5":[], "6":[], "7":[], "8":[], "9":[], "10":[], "11":[], "12":[]}
	i = 0

	for data in weather_data:
		value = data["value"]
		temp_time = datetime.datetime.strptime(data["time"], "%Y%m%d").date()
		month_temp.append(value)

		if month_date == "":
			month_date = temp_time + datetime.timedelta(days=30)

		if datetime.datetime.strptime(data["time"], "%Y%m%d").date() > month_date:
			month_date = temp_time + datetime.timedelta(days=30)
			time_stamp = (temp_time + datetime.timedelta(days=-30)).strftime("%Y")

			if time_stamp not in year_month_temp.keys():
				year_month_temp[time_stamp] = []

			avg_temp = round(sum(month_temp) / float(len(month_temp)), 2)

			year_month_temp[time_stamp].append(avg_temp)

			month = i % 12 + 1

			all_month_temp[str(month)] += month_temp

			month_temp = []
			i += 1

	print(all_month_temp)
	print(year_month_temp)
	with open("output_file.json", "w") as fw:
		output_json = []
		for key, value in year_month_temp.items():
			output_json.append({"time": key, "value": value})

		fw.write(json.dumps(output_json))



