# In NoDupMDT there are duplicates of S numbers.
# This script extracts all the MDT terms and assigns them to unique S numbers,
# merging them into one key-value pair where applicable

import glob, os
import pandas as pd
from csv import DictWriter

raw = pd.read_csv("~/Individual_Research_Project/Data/NoDupMDT.csv")
snumbers = raw['HospNo']
outcomes = raw['Outcome']

MDT_dict = {}
for i in raw['HospNo']:
    MDT_dict.update({i : ''})

for i in range(len(snumbers)):
    MDT_dict[snumbers[i]] = outcomes[i]


#parent_dir = r'/home/dcl10/Individual_Research_Project/Data/webscrape'
true_false_file = pd.read_csv("../../Data/TrueILD_only_ult_filt.csv")
last_dict = {true_false_file['HospNo'][i]: true_false_file['Sarcoid'][i]
             for i in range(len(true_false_file['HospNo']))}

print(last_dict)
#exit(0)

output = open("../../Data/merged_on_Sarcoid.csv", "w")
dw = DictWriter(output, fieldnames=["S number", "Outcome", "Sarcoid"], delimiter=",")
dw.writeheader()
for i in last_dict.keys():
    try:
        dw.writerow({'S number' : i, 'Outcome' : MDT_dict[i], 'Sarcoid': last_dict[i]})
    except KeyError:
        print("Can't find key", i)
