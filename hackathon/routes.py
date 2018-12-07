# -*- coding: utf-8 -*-
import os
import pickle
import json

import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from app import app
from app.controller.feature_format import feature_format, target_feature_split

class StrToBytes:
    def __init__(self, file_obj):
        self.fileobj = file_obj
    def read(self, size):
        return self.fileobj.read(size).encode()
    def readline(self, size=-1):
        return self.fileobj.readline(size).encode()


@app.route('/')
def index():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    parent_path = os.path.abspath(os.path.dirname(dir_path))

    dictionary = pickle.load(open(os.path.join(parent_path, "static", "file", "final_project_dataset_modified.pkl"), "rb"))
    features_list = ["bonus", "salary"]

    data = feature_format(dictionary, features_list, remove_any_zeroes=True)
    data_x = []
    data_y = []

    for item in data:
        data_x.append(item[0])
        data_y.append(item[1])

    x = np.array(data_x)
    y = np.array(data_y)

    plt.rc('font', size=15)
    plt.scatter(x, y, 60, color='blue', marker='o', linewidth=3, alpha=0.8)

    plt.xlabel('bonus')
    plt.ylabel('salary')
    plt.title('bonus_salary_analysis')

    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='both', alpha=0.4)
    plt.show()



    return "hello"

