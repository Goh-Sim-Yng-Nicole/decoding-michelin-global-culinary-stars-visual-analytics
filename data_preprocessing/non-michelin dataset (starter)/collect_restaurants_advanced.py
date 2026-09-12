import requests
import pandas as pd
from tqdm import tqdm
import time

API_KEY = "AIzaSyDXEzooms55T0jKpvMNx_9a2RQFXmzVf8I"

# Expanded Singapore grid (more locations)
locations = [
    (1.3521,103.8198),
    (1.3300,103.8600),
    (1.3000,103.8200),
    (1.3100,103.9000),
    (1.2800,103.8500),
    (1.3400,103.7600),
    (1.3600,103.9000),
    (1.3200,103.7800),
    (1.2950,103.8300),
    (1.4000,103.8200),
    (1.3800,103.7500),
    (1.3500,103.9400),
    (1.3100,103.7200),
    (1.4300,103.8300),
    (1.3600,103.7600),
    (1.3900,103.8900)
]

radius = 3000

restaurants = []

print("Collecting restaurants across Singapore...")

for lat, lng in tqdm(locations):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": "restaurant",
        "key": API_KEY
    }

    response = requests.get(url, params=params).json()

    while True:

        for place in response.get("results", []):

            restaurants.append({
                "restaurant_name": place.get("name"),
                "place_id": place.get("place_id"),
                "rating": place.get("rating"),
                "review_count": place.get("user_ratings_total"),
                "price_level": place.get("price_level"),
                "lat": place["geometry"]["location"]["lat"],
                "lng": place["geometry"]["location"]["lng"]
            })

        # check if next page exists
        next_page_token = response.get("next_page_token")

        if next_page_token:

            time.sleep(2)

            response = requests.get(url, params={
                "pagetoken": next_page_token,
                "key": API_KEY
            }).json()

        else:
            break

df = pd.DataFrame(restaurants)

df = df.drop_duplicates(subset="place_id")

print("Total restaurants collected:", len(df))

df.to_csv("singapore_restaurants.csv", index=False)

print("Saved dataset: singapore_restaurants.csv")