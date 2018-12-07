import json
import math

import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

with open("dongli_history_temperature.json", "r") as fr:
	json_data = json.load(fr)

# print(json_data)

data_x = []
data_y = []
for data in json_data:
	data_x.append(data["time"])
	data_y.append(data["value"])

x = np.array(data_x)
y = np.array(data_y)

plt.rc('font', size=15)
plt.scatter(x, y, 60, color='blue', marker='o', linewidth=3, alpha=0.8)

plt.xlabel('bonus')
plt.ylabel('salary')
plt.title('bonus_salary_analysis')

plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='both', alpha=0.4)
# plt.show()

X_train, X_test, y_train, y_test= train_test_split(x, y, test_size=0.4, random_state=0)

clf =linear_model.LinearRegression()
clf.fit (X_train.reshape(-1, 1).astype(np.float64), y_train)

predict_20201010 = clf.predict(np.array([20201010]).reshape(-1, 1))
print("predict 2020/10/10 is: ", predict_20201010)

deviation_sum = ((y_test - list(clf.predict(np.array(X_test).reshape(-1, 1).astype(np.float64))))**2).sum()

print(len(y_test))
print(deviation_sum)
print("deviation: ", math.sqrt(deviation_sum/len(y_test)))
