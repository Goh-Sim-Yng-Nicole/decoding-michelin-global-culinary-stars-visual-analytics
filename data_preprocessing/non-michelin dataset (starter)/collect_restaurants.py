import requests
import pandas as pd
from tqdm import tqdm
import time

# -------------------------------
# PASTE YOUR GOOGLE API KEY HERE
# -------------------------------

API_KEY = "AIzaSyDXEzooms55T0jKpvMNx_9a2RQFXmzVf8I"

# -------------------------------------------------
# Singapore coordinates (multiple areas for coverage)
# -------------------------------------------------

locations = [
    (1.3521,103.8198),  # Central Singapore
    (1.3300,103.8600),  # Geylang
    (1.3000,103.8200),  # Orchard
    (1.3100,103.9000),  # Bedok
    (1.2800,103.8500),  # Marina Bay
    (1.3400,103.7600),  # Jurong
    (1.3600,103.9000),  # Punggol
    (1.3200,103.7800),  # Clementi
    (1.2950,103.8300),  # River Valley
    (1.4000,103.8200),  # Woodlands
    (1.3800,103.7500),  # Choa Chu Kang
    (1.3500,103.9400)   # Pasir Ris
]

# radius in meters
radius = 3000

restaurants = []

print("Starting restaurant collection...")

# ------------------------------------
# Loop through all locations
# ------------------------------------

for lat, lng in tqdm(locations):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": "restaurant",
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data:
        print("No results returned")
        continue

    for place in data["results"]:

        restaurants.append({
            "restaurant_name": place.get("name"),
            "place_id": place.get("place_id"),
            "rating": place.get("rating"),
            "review_count": place.get("user_ratings_total"),
            "price_level": place.get("price_level"),
            "latitude": place["geometry"]["location"]["lat"],
            "longitude": place["geometry"]["location"]["lng"]
        })

    time.sleep(1)

# ------------------------------------
# Convert to DataFrame
# ------------------------------------

df = pd.DataFrame(restaurants)

# Remove duplicates
df = df.drop_duplicates(subset="place_id")

print("Total restaurants collected:", len(df))

# ------------------------------------
# Save dataset
# ------------------------------------

df.to_csv("singapore_restaurants.csv", index=False)

print("Dataset saved as singapore_restaurants.csv")