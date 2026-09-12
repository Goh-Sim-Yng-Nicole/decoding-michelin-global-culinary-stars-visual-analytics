import pandas as pd
from fuzzywuzzy import process
from tqdm import tqdm

print("Loading datasets...")

michelin = pd.read_csv("michelin_sg.csv")
sfa = pd.read_csv("sfa_hygiene.csv")

# standardize names
michelin["restaurant_name"] = michelin["restaurant_name"].astype(str).str.lower().str.strip()
sfa["restaurant_name"] = sfa["restaurant_name"].astype(str).str.lower().str.strip()

print("Michelin restaurants:", len(michelin))
print("SFA establishments:", len(sfa))

sfa_names = sfa["restaurant_name"].tolist()

matches = []
matched_names = []

print("Matching Michelin restaurants with SFA dataset...")

for name in tqdm(michelin["restaurant_name"]):

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

michelin["matched_sfa_name"] = matched_names
michelin["hygiene_grade"] = matches

print("Matched Michelin restaurants:", michelin["hygiene_grade"].notnull().sum())

michelin.to_csv("michelin_sg_with_hygiene.csv", index=False)

print("Saved dataset: michelin_sg_with_hygiene.csv")