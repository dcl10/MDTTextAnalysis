# In NoDupMDT there are duplicates of S numbers.
# This script extracts all the MDT terms and assigns them to unique S numbers,
# merging them into one key-value pair where applicable


import pandas as pd
from csv import DictWriter

raw = pd.read_csv("~/Individual_Research_Project/Data/NoDupMDT.csv")
snumbers = raw['HospNo']
outcomes = raw['Outcome']

MDT_dict = {}
for i in raw['HospNo']:
    MDT_dict.update({i : ''})

for i in range(len(snumbers)):
    if snumbers[i] in MDT_dict.keys():
        MDT_dict[snumbers[i]] = str(MDT_dict[snumbers[i]]) + " " + str(outcomes[i])
    else:
        MDT_dict[snumbers[i]] = outcomes[i]

for i in MDT_dict.keys():
    print(MDT_dict[i])

output = open("../../Data/merged.csv", "w")
dw = DictWriter(output, fieldnames=["S number", "Outcome"], delimiter=",")
dw.writeheader()
for i in MDT_dict.keys():
    dw.writerow({'S number' : i, 'Outcome' : MDT_dict[i]})
