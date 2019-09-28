"""
Run python autograder.py
"""

def average(priceList):
    "Return the average price of a set of fruit"
    "*** YOUR CODE HERE ***"
    uniq = set(priceList)
    return sum(uniq)/len(uniq)
