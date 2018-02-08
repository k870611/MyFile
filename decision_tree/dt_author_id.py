#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 3 (decision tree) mini-project.

    Use a Decision Tree to identify emails from the Enron corpus by author:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess
from sklearn import tree


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()


def submitAccuracies():
    clf_split2 = tree.DecisionTreeClassifier(min_samples_split=40);
    clf_split2 = clf_split2.fit(features_train, labels_train);

    acc_min_samples_split_2 = clf_split2.score(features_test, labels_test);

    clf_split50 = tree.DecisionTreeClassifier(min_samples_split=50);
    clf_split50 = clf_split50.fit(features_train, labels_train);

    acc_min_samples_split_50 = clf_split50.score(features_test, labels_test);

    return {"acc_min_samples_split_2": round(acc_min_samples_split_2, 3),
            "acc_min_samples_split_50": round(acc_min_samples_split_50, 3)}

print("Desition Tree Test...............");
acc = submitAccuracies();
print(acc);


clf = tree.DecisionTreeClassifier(min_samples_split = 40);
clf.fit(features_train, labels_train);
pred = clf.predict(features_test);

by_chris = [item for item in pred if item == 1];
print(len(by_chris)) ; # prints 879


print(len(features_train[0]));




#########################################################
### your code goes here ###


#########################################################


