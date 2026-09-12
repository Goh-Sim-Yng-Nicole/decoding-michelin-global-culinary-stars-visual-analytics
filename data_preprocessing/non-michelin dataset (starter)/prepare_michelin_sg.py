import pandas as pd

print("Loading Michelin dataset...")

michelin = pd.read_csv("michelin_restaurants.csv")

# standardize column names
michelin.columns = michelin.columns.str.lower()

print("Columns:", michelin.columns)

# ------------------------------------------------
# Filter restaurants located in Singapore
# ------------------------------------------------

michelin_sg = michelin[
    michelin["location"].str.lower().str.contains("singapore", na=False)
]

print("Singapore Michelin restaurants found:", len(michelin_sg))

# ------------------------------------------------
# Create standardized restaurant name
# ------------------------------------------------

michelin_sg["restaurant_name"] = (
    michelin_sg["name"]
    .astype(str)
    .str.lower()
    .str.strip()
)

# keep only useful columns
michelin_sg = michelin_sg[
    [
        "restaurant_name",
        "name",
        "award",
        "price",
        "cuisine",
        "latitude",
        "longitude"
    ]
]

michelin_sg.to_csv("michelin_sg.csv", index=False)

print("Saved dataset: michelin_sg.csv")