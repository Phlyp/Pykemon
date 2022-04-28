import pandas as pd

data = pd.read_csv("Data/pokemon.csv")

print(data["name"][0:3])