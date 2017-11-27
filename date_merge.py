import pandas as pd
from csv import DictWriter

# This file was used to find the MDT dates to see if the cluster with higher pirfenidone mentions
# clustered around the pirfenidone release date.

df1 = pd.read_csv("../../Data/NoDupMDT.csv", na_filter='')
df2 = pd.read_csv("../../Data/the_grand_finale.csv", na_filter='')

date_dict = {df1['HospNo'][i]: df1['dateMDT'][i] for i in range(len(df1['HospNo']))}
outcome_dict = {df2['S number'][i]: df2['Outcome'][i] for i in range(len(df2['S number']))}
print(date_dict)
print(outcome_dict)

file = open("datemerged.csv", "w")
output = DictWriter(file, ['S number', 'dateMDT', 'Outcome'], delimiter=",")
output.writeheader()
for i in date_dict.keys():
    try:
        output.writerow({'S number': i, 'dateMDT': date_dict[i], 'Outcome': outcome_dict[i]})
    except Exception:
        print("Can't add", i)