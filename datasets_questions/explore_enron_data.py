#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle


enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

'''
poi = int(0)
print enron_data
for i in enron_data:
    print enron_data[i]
    count = int(1)

    for info in enron_data[i]:
        print count, ". ", info, ":", enron_data[i][info]
        count += 1

        if info == "poi":
            if enron_data[i][info]:
                poi += 1
                print "poi num = ", poi
'''

poi_name_record = open("../final_project/poi_names.txt").read().split("\n")
poi_name_total = [record for record in poi_name_record if "(y)" in record or "(n)" in record]
print("Total number of POIs: ", len(poi_name_total))


for i in enron_data:
    if "LAY KENNETH L" in i:
        print i
        for info in enron_data[i]:
            print info, ":", enron_data[i][info]

total_stock_james = enron_data["PRENTICE JAMES"]["total_stock_value"]
print total_stock_james

poi_form_wesley = enron_data["COLWELL WESLEY"]["from_poi_to_this_person"]
print(poi_form_wesley)

stock_option_jeffery = enron_data["SKILLING JEFFREY K"].get("exercised_stock_options")
print(stock_option_jeffery)

salary_quantified = int(0)
email_quantified = int(0)
for i in enron_data:
    if enron_data[i]["salary"] != "NaN":
        salary_quantified += 1
        print i, "salary_quantified:", salary_quantified

    if enron_data[i]["email_address"] != "NaN":
        email_quantified += 1
        print i, "email_quantified:", email_quantified
