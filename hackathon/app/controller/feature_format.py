#!/usr/bin/python

""" 
    A general tool for converting data from the
    dictionary format to an (n x k) python list that's 
    ready for training an sklearn algorithm

    n--no. of key-value pairs in dictonary
    k--no. of features being extracted

    dictionary keys are names of persons in dataset
    dictionary values are dictionaries, where each
        key-value pair in the dict is the name
        of a feature, and its value for that person

    In addition to converting a dictionary to a numpy 
    array, you may want to separate the labels from the
    features--this is what targetFeatureSplit is for

    so, if you want to have the poi label as the target,
    and the features you want to use are the person's
    salary and bonus, here's what you would do:

    feature_list = ["poi", "salary", "bonus"] 
    data_array = featureFormat( data_dictionary, feature_list )
    label, features = targetFeatureSplit(data_array)

    the line above (targetFeatureSplit) assumes that the
    label is the _first_ item in feature_list--very important
    that poi is listed first!
"""


import numpy as np

def feature_format( dictionary, features, remove_nan=True, remove_all_zeroes=True, remove_any_zeroes=False, sort_keys = False):

    return_list = []

    if isinstance(sort_keys, str):
        import pickle
        keys = pickle.load(open(sort_keys, "rb"))
    elif sort_keys:
        keys = sorted(dictionary.keys())
    else:
        keys = dictionary.keys()

    for key in keys:
        tmp_list = []
        for feature in features:
            try:
                dictionary[key][feature]
            except KeyError:
                print("error: key ", feature, " not present")
                return
            value = dictionary[key][feature]
            if value=="NaN" and remove_nan:
                value = 0
            tmp_list.append( float(value) )

        append = True

        if features[0] == 'poi':
            test_list = tmp_list[1:]
        else:
            test_list = tmp_list

        if remove_all_zeroes:
            append = False
            for item in test_list:
                if item != 0 and item != "NaN":
                    append = True
                    break

        if remove_any_zeroes:
            if 0 in test_list or "NaN" in test_list:
                append = False

        if append:
            return_list.append(np.array(tmp_list))

    return np.array(return_list)


def target_feature_split(data):
    target = []
    features = []
    for item in data:
        target.append(item[0])
        features.append(item[1:])

    return target, features




