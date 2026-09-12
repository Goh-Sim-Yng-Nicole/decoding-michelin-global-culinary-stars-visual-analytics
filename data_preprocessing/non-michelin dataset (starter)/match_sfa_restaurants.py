import pandas as pd
from fuzzywuzzy import process
from tqdm import tqdm

print("Loading datasets...")

restaurants = pd.read_csv("singapore_restaurants.csv")
sfa = pd.read_csv("sfa_hygiene.csv")

restaurants["restaurant_name"] = restaurants["restaurant_name"].astype(str).str.lower().str.strip()
sfa["restaurant_name"] = sfa["restaurant_name"].astype(str).str.lower().str.strip()

print("Restaurants dataset size:", len(restaurants))
print("SFA dataset size:", len(sfa))

matches = []
matched_names = []

print("Matching restaurants with SFA dataset...")

sfa_names = sfa["restaurant_name"].tolist()

for name in tqdm(restaurants["restaurant_name"]):

    match = process.extractOne(name, sfa_names)

    if match:

        matched_name = match[0]
        score = match[1]

        if score >= 85:

            grade = sfa.loc[
                sfa["restaurant_name"] == matched_name,
                "hygiene_grade"
            ].values[0]

        else:
            grade = None
            matched_name = None

    else:
        grade = None
        matched_name = None

    matches.append(grade)
    matched_names.append(matched_name)

restaurants["matched_sfa_name"] = matched_names
restaurants["hygiene_grade"] = matches

print("Matched restaurants:", restaurants["hygiene_grade"].notnull().sum())

restaurants.to_csv("restaurants_with_hygiene.csv", index=False)

print("Saved dataset: restaurants_with_hygiene.csv")