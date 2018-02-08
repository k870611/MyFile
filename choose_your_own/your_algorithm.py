#!/usr/bin/python

import matplotlib.pyplot as plt
from prep_terrain_data import makeTerrainData
from class_vis import prettyPicture


features_train, labels_train, features_test, labels_test = makeTerrainData()


### the training data (features_train, labels_train) have both "fast" and "slow"
### points mixed together--separate them so we can give them different colors
### in the scatterplot and identify them visually
grade_fast = [features_train[ii][0] for ii in range(0, len(features_train)) if labels_train[ii]==0]
bumpy_fast = [features_train[ii][1] for ii in range(0, len(features_train)) if labels_train[ii]==0]
grade_slow = [features_train[ii][0] for ii in range(0, len(features_train)) if labels_train[ii]==1]
bumpy_slow = [features_train[ii][1] for ii in range(0, len(features_train)) if labels_train[ii]==1]


#### initial visualization
plt.xlim(0.0, 1.0)
plt.ylim(0.0, 1.0)
plt.scatter(bumpy_fast, grade_fast, color = "b", label="fast")
plt.scatter(grade_slow, bumpy_slow, color = "r", label="slow")
plt.legend()
plt.xlabel("bumpiness")
plt.ylabel("grade")
plt.show()
################################################################################


### your code here!  name your classifier object clf if you want the 
### visualization code (prettyPicture) to show you the decision boundary
from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors=3)
clf = clf.fit(features_train, labels_train)
acc = clf.score(features_test, labels_test);

print "k-nearest neighbors _ Accuracy: ", acc

from sklearn.ensemble import AdaBoostClassifier
clf_ada = AdaBoostClassifier(n_estimators=100)
clf_ada = clf_ada.fit(features_train, labels_train)
acc_ada = clf_ada.score(features_test, labels_test)
print "AdaBoost_Accuracy: ", acc_ada

from sklearn.ensemble import RandomForestClassifier
clf_ram = RandomForestClassifier(max_depth=2, random_state=0)
clf_ram = clf_ram.fit(features_train, labels_train)
clf_ram = clf_ram.score(features_test, labels_test)
print "Random Forest_Accuracy: ", clf_ram


try:
    prettyPicture(clf, features_test, labels_test)
except NameError:
    pass
