import pandas as pd
import requests
from tqdm import tqdm
import time

API_KEY = "AIzaSyDXEzooms55T0jKpvMNx_9a2RQFXmzVf8I"

restaurants = pd.read_csv("singapore_restaurants.csv")

reviews = []

print("Collecting restaurant reviews...")

for place_id in tqdm(restaurants["place_id"]):

    url = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "place_id": place_id,
        "fields": "name,reviews",
        "key": API_KEY
    }

    response = requests.get(url, params=params).json()

    result = response.get("result", {})

    place_reviews = result.get("reviews", [])

    for review in place_reviews:

        reviews.append({
            "restaurant_name": result.get("name"),
            "review_rating": review.get("rating"),
            "review_text": review.get("text"),
            "review_time": review.get("time"),
            "author": review.get("author_name")
        })

    time.sleep(0.1)

reviews_df = pd.DataFrame(reviews)

print("Total reviews collected:", len(reviews_df))

reviews_df.to_csv("restaurant_reviews.csv", index=False)

print("Dataset saved as restaurant_reviews.csv")