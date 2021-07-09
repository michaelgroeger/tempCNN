import pandas as pd

# Read temperature csv
df = pd.read_csv("data/outputs/average_temp_discretized.csv")
print(type(df))
df["R"] = pd.Series(dtype="Int16")
df["G"] = pd.Series(dtype="Int16")
df["B"] = pd.Series(dtype="Int16")

class_1 = df["t2m"] <= 281
class_2 = (df["t2m"] > 281) & (df["t2m"] <= 283)
class_3 = (df["t2m"] > 283) & (df["t2m"] <= 285)
class_4 = (df["t2m"] > 285) & (df["t2m"] <= 287)
class_5 = (df["t2m"] > 287) & (df["t2m"] <= 289)
class_6 = (df["t2m"] > 289) & (df["t2m"] <= 291)
class_7 = (df["t2m"] > 291) & (df["t2m"] <= 293)
class_8 = (df["t2m"] > 293) & (df["t2m"] <= 295)
class_9 = (df["t2m"] > 295) & (df["t2m"] <= 297)
class_10 = df["t2m"] > 297

classes = [
    class_1,
    class_2,
    class_3,
    class_4,
    class_5,
    class_6,
    class_7,
    class_8,
    class_9,
    class_10,
]

color_codes = [
    (48, 18, 59),
    (58, 49, 126),
    (68, 132, 245),
    (32, 204, 213),
    (74, 247, 130),
    (177, 247, 58),
    (241, 197, 55),
    (248, 118, 29),
    (203, 46, 5),
    (122, 4, 3),
]

for mask, code in zip(classes, color_codes):
    df.loc[mask, "R"] = code[0]
    df.loc[mask, "G"] = code[1]
    df.loc[mask, "B"] = code[2]

df.to_csv(r"data/outputs/average_temp_discretized.csv", index=False)

