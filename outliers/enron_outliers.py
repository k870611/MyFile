#!/usr/bin/python

import pickle
import sys
import matplotlib.pyplot
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit


### read in data dictionary, convert to numpy array
data_dict = pickle.load( open("../final_project/final_project_dataset.pkl", "r") )
features = ["salary", "bonus"]

### your code below
for k, v in data_dict.items():
    salary = float(v.get('salary'))
    bonus = float(v.get('bonus'))
    if (salary > 1000000) and (bonus >= 5000000):
        data_dict.pop(k, 0)
        print(k)

print [r for r, v in data_dict.items()
       if v['salary'] > 1000000.0
       and v['bonus'] > 5000000.0
       and v['salary'] != 'NaN'
       and v['bonus'] != 'NaN']

data = featureFormat(data_dict, features)

for point in data:
    salary = point[0]
    bonus = point[1]
    matplotlib.pyplot.scatter(salary, bonus)

matplotlib.pyplot.xlabel("salary")
matplotlib.pyplot.ylabel("bonus")
matplotlib.pyplot.show()


