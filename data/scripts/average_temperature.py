import pandas as pd
import numpy as np

# read csv
df = pd.read_csv("data/outputs/all_temp.csv")

# Get averages over long & lat
df = df[["latitude", "longitude", "t2m"]]

averages_df = df.groupby(["latitude", "longitude"])["t2m"].mean().reset_index()

averages_df.sort_values(by=["latitude", "longitude"], inplace=True)
averages_df.to_csv(r"data/outputs/average_temp_02_sort_lat.csv", index=False)
