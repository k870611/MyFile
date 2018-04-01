#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    
    cleaned_data = []

    ### your code goes here
    import numpy as np
    predictions = np.array(predictions)
    ages = np.array(ages)
    net_worths = np.array(net_worths)
    cleaned_data = []
    c = 90

    for i in range(9):
        errors = []
        for use in range(c):
            d = (predictions[use] - net_worths[use]) ** 2
            errors.append(d)

        m = max(errors)
        # print(max(errors))
        b = errors.index(m)
        predictions = np.delete(predictions, b)
        # print(len(predictions))
        ages = np.delete(ages, b)
        net_worths = np.delete(net_worths, b)
        c -= 1
    cleaned_data = zip(ages, net_worths, errors)

    return cleaned_data

