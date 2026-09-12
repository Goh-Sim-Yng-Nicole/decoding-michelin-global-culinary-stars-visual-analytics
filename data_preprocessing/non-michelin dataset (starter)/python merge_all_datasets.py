import pandas as pd

print("Loading datasets...")

# -----------------------------
# Load datasets
# -----------------------------

restaurants = pd.read_csv("restaurants_with_hygiene.csv")
reviews = pd.read_csv("reviews_with_sentiment.csv")
michelin = pd.read_csv("michelin_sg_with_hygiene.csv")

# -----------------------------
# Standardize restaurant names
# -----------------------------

restaurants["restaurant_name"] = restaurants["restaurant_name"].astype(str).str.lower().str.strip()
reviews["restaurant_name"] = reviews["restaurant_name"].astype(str).str.lower().str.strip()
michelin["restaurant_name"] = michelin["restaurant_name"].astype(str).str.lower().str.strip()

print("Restaurants:", len(restaurants))
print("Reviews:", len(reviews))
print("Michelin restaurants:", len(michelin))

# -----------------------------
# Aggregate sentiment by restaurant
# -----------------------------

print("Calculating sentiment metrics...")

sentiment_summary = reviews.groupby("restaurant_name").agg(
    avg_sentiment=("sentiment_score", "mean"),
    total_reviews=("review_text", "count")
).reset_index()

print("Sentiment summary rows:", len(sentiment_summary))

# -----------------------------
# Merge sentiment with restaurants
# -----------------------------

data = restaurants.merge(
    sentiment_summary,
    on="restaurant_name",
    how="left"
)

# -----------------------------
# Add Michelin information
# -----------------------------

data["is_michelin"] = data["restaurant_name"].isin(michelin["restaurant_name"])

data = data.merge(
    michelin[["restaurant_name", "award"]],
    on="restaurant_name",
    how="left"
)

# -----------------------------
# Rename Michelin award column
# -----------------------------

data.rename(columns={"award": "michelin_award"}, inplace=True)

# -----------------------------
# Fill missing sentiment values
# -----------------------------

data["avg_sentiment"] = data["avg_sentiment"].fillna(0)

# -----------------------------
# Fill missing hygiene values
# -----------------------------

data["hygiene_grade"] = data["hygiene_grade"].fillna("Unknown")

# -----------------------------
# Save final dataset
# -----------------------------

data.to_csv("master_restaurant_dataset.csv", index=False)

print("Saved dataset: master_restaurant_dataset.csv")
print("Total rows:", len(data))