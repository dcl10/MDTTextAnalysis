# In NoDupMDT there are duplicates of S numbers.
# This script extracts all the MDT terms and assigns them to unique S numbers,
# merging them into one key-value pair where applicable

import glob, os
import pandas as pd
from csv import DictWriter

raw = pd.read_csv("~/Individual_Research_Project/Data/the_grand_finale.csv")
snumbers = raw['S number']
outcomes = raw['Outcome']

MDT_dict = {}
for i in raw['S number']:
    MDT_dict.update({i : ''})

for i in range(len(snumbers)):
    MDT_dict[snumbers[i]] = outcomes[i]


#parent_dir = r'/home/dcl10/Individual_Research_Project/Data/webscrape'
true_false_file = pd.read_csv("../../Data/the_grand_finale.csv")
last_dict = {true_false_file['S number'][i]: true_false_file['IPF'][i]
             for i in range(len(true_false_file['S number']))}

print(last_dict)
#exit(0)

output = open("../../Data/merged_on_IPF2.csv", "w")
dw = DictWriter(output, fieldnames=["S number", "Outcome", "IPF"], delimiter=",")
dw.writeheader()
for i in last_dict.keys():
    try:
        dw.writerow({'S number' : i, 'Outcome' : MDT_dict[i], 'IPF': last_dict[i]})
    except KeyError:
        print("Can't find key", i)
