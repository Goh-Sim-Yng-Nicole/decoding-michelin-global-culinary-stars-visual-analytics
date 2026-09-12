import requests
import pandas as pd
import time
from tqdm import tqdm

API_KEY = "AIzaSyDXEzooms55T0jKpvMNx_9a2RQFXmzVf8I"

# -------------------------------------------------
# Generate grid across Singapore
# -------------------------------------------------

latitudes = [1.20 + i*0.02 for i in range(15)]
longitudes = [103.60 + i*0.02 for i in range(15)]

locations = [(lat, lng) for lat in latitudes for lng in longitudes]

radius = 2000

restaurants = []

print("Scanning Singapore grid for restaurants...")

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
                "latitude": place["geometry"]["location"]["lat"],
                "longitude": place["geometry"]["location"]["lng"]
            })

        next_page_token = response.get("next_page_token")

        if next_page_token:

            time.sleep(2)

            response = requests.get(url, params={
                "pagetoken": next_page_token,
                "key": API_KEY
            }).json()

        else:
            break

    time.sleep(0.2)

df = pd.DataFrame(restaurants)

df = df.drop_duplicates(subset="place_id")

print("Total restaurants collected:", len(df))

df.to_csv("singapore_restaurants.csv", index=False)

print("Dataset saved as singapore_restaurants.csv")