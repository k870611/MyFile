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



@app.route('/')
def index():
    features_list = ["year", "temp"]


    return "hello"

