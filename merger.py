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


parent_dir = r'/home/dcl10/Individual_Research_Project/Data/webscrape'

dead_dict = {}
for tsv_file in glob.glob(os.path.join(parent_dir, '*.tsv')):
    file = os.path.split(tsv_file)
    try:
        df = pd.read_table("../../Data/webscrape/" + file[1], sep="\t")
        dead_dict.update({df['Hospital Number:'][0]: df['Deceased:'][0]})
    except UnicodeDecodeError:
        print(file[1], "is fucked")


output = open("../../Data/merged3.csv", "w")
dw = DictWriter(output, fieldnames=["S number", "Outcome", "Deceased"], delimiter=",")
dw.writeheader()
for i in dead_dict.keys():
    try:
        dw.writerow({'S number' : i, 'Outcome' : MDT_dict[i], 'Deceased': dead_dict[i]})
    except KeyError:
        print("Can't find key", i)


