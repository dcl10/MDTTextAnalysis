import pandas as pd

# This file made the properly merged file for the clustering

left = pd.read_csv("../../Data/TrueILD_only_ult_filt.csv")
right = pd.read_csv("../../Data/merged3.csv")

#print(left)
#print(right)

centre = pd.merge(left, right, on="S number")
print(centre)

pd.DataFrame.to_csv(centre, "../../Data/the_grand_finale.csv")
