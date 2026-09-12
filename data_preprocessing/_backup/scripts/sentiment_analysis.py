"""
sentiment_analysis.py
=====================
Runs zero-shot sentiment analysis on both Michelin and Non-Michelin
restaurant reviews, then fills any remaining gaps by scraping reviews
for restaurants that still have none.

Pipeline per dataset:
  1. Load reviews from review/<prefix>_reviews.csv
  2. Classify each review across 3 categories x 5 tiers (15 labels total)
  3. Save per-review results to review/<prefix>_review_level_sentiment.csv
  4. Aggregate per restaurant and merge 11 sentiment columns into
     <prefix>_restaurants.csv (replacing any old sentiment columns)

Gap-fill step (runs after both datasets):
  5. Find restaurants still at Review Count == 0
  6. Scrape up to 5 Google reviews via Places Details API
  7. Run sentiment on the new reviews only
  8. Append to the review-level CSV and re-aggregate

Final step:
  9. Rebuild output/restaurants.csv and output/restaurants.xlsx

Sentiment columns added to each restaurants CSV:
    Review Count | Average Rating
    value_tier   | value_score   | value_tier_numeric
    service_tier | service_score | service_tier_numeric
    taste_tier   | taste_score   | taste_tier_numeric

Scores are on a 1-5 scale (5 = excellent, 1 = terrible).
Checkpoints every 500 reviews so the script can be interrupted and resumed.
"""

import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

import pandas as pd
from transformers import pipeline
from tqdm import tqdm

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def _load_env():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
_load_env()

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
API_KEY    = os.environ.get('GOOGLE_PLACES_API_KEY', '')
os.makedirs(OUTPUT_DIR, exist_ok=True)

MAX_CHARS = 512
API_DELAY = 0.05

# ── Categories & tiers ────────────────────────────────────────────────────────
TIERS      = ["excellent", "good", "average", "poor", "terrible"]
TIER_SCORE = {"excellent": 5, "good": 4, "average": 3, "poor": 2, "terrible": 1}

CATEGORIES = {
    "value": {
        "excellent": "excellent value for money, very affordable and worth every cent",
        "good":      "good value for money, reasonably priced",
        "average":   "average value for money, neither cheap nor expensive",
        "poor":      "poor value for money, somewhat overpriced",
        "terrible":  "terrible value for money, extremely overpriced",
    },
    "service": {
        "excellent": "excellent service, staff are very attentive and friendly",
        "good":      "good service, staff are helpful and polite",
        "average":   "average service, nothing special about the staff",
        "poor":      "poor service, staff are slow or unhelpful",
        "terrible":  "terrible service, rude or completely inattentive staff",
    },
    "taste": {
        "excellent": "excellent food, absolutely delicious and outstanding",
        "good":      "good food, tasty and enjoyable",
        "average":   "average food, neither good nor bad",
        "poor":      "poor food, disappointing taste",
        "terrible":  "terrible food, unpleasant or inedible",
    },
}

all_labels = [lbl for cat in CATEGORIES.values() for lbl in cat.values()]

OLD_SENTIMENT_COLS = [
    "true_affordability_ratio_percent", "review_count", "Average Google Rating",
    "Review Count", "Average Rating",
    "value_tier", "value_score", "service_tier", "service_score",
    "taste_tier", "taste_score",
    "value_tier_numeric", "service_tier_numeric", "taste_tier_numeric",
]

# ── Dataset definitions ───────────────────────────────────────────────────────
DATASETS = [
    {
        "label":           "Michelin",
        "reviews_csv":     os.path.join(BASE_DIR, "reviews", "michelin_reviews.csv"),
        "restaurants_csv": os.path.join(BASE_DIR, "restaurants", "michelin_restaurants.csv"),
        "checkpoint":      os.path.join(BASE_DIR, "reviews", "mi_sentiment_checkpoint.csv"),
        "review_out":      os.path.join(BASE_DIR, "reviews", "mi_review_level_sentiment.csv"),
    },
    {
        "label":           "Non-Michelin",
        "reviews_csv":     os.path.join(BASE_DIR, "reviews", "non-michelin_reviews.csv"),
        "restaurants_csv": os.path.join(BASE_DIR, "restaurants", "non-michelin_restaurants.csv"),
        "checkpoint":      os.path.join(BASE_DIR, "reviews", "nm_sentiment_checkpoint.csv"),
        "review_out":      os.path.join(BASE_DIR, "reviews", "nm_review_level_sentiment.csv"),
    },
]


# ── Sentiment helpers ─────────────────────────────────────────────────────────
def classify_reviews(df, classifier, checkpoint):
    """Classify all rows in df; resume from checkpoint if present."""
    if checkpoint and os.path.exists(checkpoint):
        ckpt_df   = pd.read_csv(checkpoint, encoding="utf-8-sig")
        completed = len(ckpt_df)
        records   = ckpt_df.to_dict("records")
        df        = df.iloc[completed:].reset_index(drop=True)
        print(f"  Resuming from checkpoint — {completed:,} done, {len(df):,} remaining.")
    else:
        records = []

    for i, (_, row) in enumerate(tqdm(df.iterrows(), total=len(df), desc="Sentiment")):
        text   = row["text"].strip()
        result = {"title": row["title"], "stars": row["stars"], "text": text}

        if not text:
            for cat in CATEGORIES:
                result[f"{cat}_tier"]  = "average"
                result[f"{cat}_score"] = 0.0
        else:
            out       = classifier(text[:MAX_CHARS], candidate_labels=all_labels, multi_label=True)
            score_map = dict(zip(out["labels"], out["scores"]))
            for cat, tier_labels in CATEGORIES.items():
                tier_scores = {t: score_map.get(tier_labels[t], 0.0) for t in TIERS}
                best        = max(tier_scores, key=tier_scores.get)
                result[f"{cat}_tier"]  = best
                result[f"{cat}_score"] = round(tier_scores[best], 4)

        records.append(result)
        if checkpoint and (i + 1) % 500 == 0:
            pd.DataFrame(records).to_csv(checkpoint, index=False, encoding="utf-8-sig")
            tqdm.write(f"  Checkpoint saved at {len(records):,} reviews.")

    return records


def save_review_level(records, review_out, checkpoint):
    reviews_df = pd.DataFrame(records)
    for cat in CATEGORIES:
        reviews_df[f"{cat}_tier_numeric"] = reviews_df[f"{cat}_tier"].map(TIER_SCORE)
    reviews_df.to_csv(review_out, index=False, encoding="utf-8-sig")
    print(f"  Review-level results saved -> {os.path.basename(review_out)}")
    if checkpoint and os.path.exists(checkpoint):
        os.remove(checkpoint)
    return reviews_df


def aggregate_and_merge(reviews_df, restaurants_csv):
    """Aggregate per-restaurant scores and merge into restaurants CSV."""
    agg_rows = []
    for restaurant, grp in reviews_df.groupby("title"):
        agg_rows.append({
            "Restaurant Name":      restaurant,
            "Review Count":         len(grp),
            "Average Rating":       round(grp["stars"].mean(), 2),
            "value_tier":           grp["value_tier"].mode()[0],
            "value_score":          round(grp["value_score"].mean(), 4),
            "service_tier":         grp["service_tier"].mode()[0],
            "service_score":        round(grp["service_score"].mean(), 4),
            "taste_tier":           grp["taste_tier"].mode()[0],
            "taste_score":          round(grp["taste_score"].mean(), 4),
            "value_tier_numeric":   round(grp["value_tier_numeric"].mean(), 2),
            "service_tier_numeric": round(grp["service_tier_numeric"].mean(), 2),
            "taste_tier_numeric":   round(grp["taste_tier_numeric"].mean(), 2),
        })

    agg_df      = pd.DataFrame(agg_rows)
    restaurants = pd.read_csv(restaurants_csv, dtype={"Phone Number": str}, encoding="utf-8-sig")
    restaurants.drop(columns=[c for c in OLD_SENTIMENT_COLS if c in restaurants.columns], inplace=True)
    restaurants = restaurants.merge(agg_df, on="Restaurant Name", how="left")
    restaurants["Review Count"] = restaurants["Review Count"].fillna(0).astype(int)
    for col in ["Average Rating", "value_tier", "value_score", "service_tier", "service_score",
                "taste_tier", "taste_score", "value_tier_numeric", "service_tier_numeric",
                "taste_tier_numeric"]:
        restaurants[col] = restaurants[col].fillna("")
    restaurants.to_csv(restaurants_csv, index=False, encoding="utf-8-sig")

    with_reviews    = (restaurants["Review Count"] > 0).sum()
    without_reviews = (restaurants["Review Count"] == 0).sum()
    print(f"  {os.path.basename(restaurants_csv)}: "
          f"{with_reviews} with sentiment, {without_reviews} without")
    return without_reviews


# ── Gap-fill helpers ──────────────────────────────────────────────────────────
def fetch_google_reviews(place_id):
    """Fetch up to 5 newest reviews from Places Details API."""
    params = urllib.parse.urlencode({
        "place_id":                place_id,
        "key":                     API_KEY,
        "fields":                  "reviews",
        "reviews_sort":            "newest",
        "reviews_no_translations": "true",
    })
    url = f"https://maps.googleapis.com/maps/api/place/details/json?{params}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
        reviews = data.get("result", {}).get("reviews", [])
        return [(r.get("rating", ""), r.get("text", "")) for r in reviews]
    except Exception as e:
        print(f"    x {place_id}: {e}")
        return []


def fill_missing(dataset, classifier):
    """Scrape, classify, and merge reviews for restaurants with Review Count == 0."""
    restaurants_csv = dataset["restaurants_csv"]
    reviews_csv     = dataset["reviews_csv"]
    review_out      = dataset["review_out"]

    restaurants = pd.read_csv(restaurants_csv, dtype={"Phone Number": str}, encoding="utf-8-sig")
    missing     = restaurants[restaurants["Review Count"] == 0][["Restaurant Name", "place_id"]]

    if missing.empty:
        print(f"  {os.path.basename(restaurants_csv)}: no gaps to fill.")
        return

    print(f"  Scraping {len(missing)} restaurants with no reviews ...")
    existing_reviews = pd.read_csv(reviews_csv, encoding="utf-8-sig")
    new_rows = []

    for _, row in tqdm(missing.iterrows(), total=len(missing), desc="Scraping"):
        for rating, text in fetch_google_reviews(str(row["place_id"])):
            if str(text).strip():
                new_rows.append({
                    "Restaurant Name":       row["Restaurant Name"],
                    "Google Review Ratings": rating,
                    "Reviews":               text,
                })
        time.sleep(API_DELAY)

    if not new_rows:
        print("  No reviews returned from API — restaurants remain without sentiment.")
        return

    print(f"  {len(new_rows)} new reviews fetched. Running sentiment ...")
    appended = pd.concat([existing_reviews, pd.DataFrame(new_rows)], ignore_index=True)
    appended.to_csv(reviews_csv, index=False, encoding="utf-8-sig")

    # Classify new rows only
    new_df = pd.DataFrame(new_rows).rename(columns={
        "Restaurant Name":       "title",
        "Google Review Ratings": "stars",
        "Reviews":               "text",
    })
    new_df["text"]  = new_df["text"].fillna("").astype(str)
    new_df["stars"] = pd.to_numeric(new_df["stars"], errors="coerce")

    new_records = classify_reviews(new_df, classifier, checkpoint=None)  # no checkpoint for small batch
    new_sent_df = pd.DataFrame(new_records)
    for cat in CATEGORIES:
        new_sent_df[f"{cat}_tier_numeric"] = new_sent_df[f"{cat}_tier"].map(TIER_SCORE)

    # Append to review-level sentiment file and re-aggregate
    existing_sent = pd.read_csv(review_out, encoding="utf-8-sig")
    combined_sent = pd.concat([existing_sent, new_sent_df], ignore_index=True)
    combined_sent.to_csv(review_out, index=False, encoding="utf-8-sig")

    aggregate_and_merge(combined_sent, restaurants_csv)


# ── Output helpers ────────────────────────────────────────────────────────────
def rebuild_output():
    mi = pd.read_csv(
        os.path.join(BASE_DIR, "restaurants", "michelin_restaurants.csv"),
        dtype={"Phone Number": str}, encoding="utf-8-sig"
    )
    nm = pd.read_csv(
        os.path.join(BASE_DIR, "restaurants", "non-michelin_restaurants.csv"),
        dtype={"Phone Number": str}, encoding="utf-8-sig"
    )
    mi["Is Michelin"] = True
    nm["Is Michelin"] = False
    master = pd.concat([mi, nm], ignore_index=True)

    out_csv  = os.path.join(OUTPUT_DIR, "restaurants.csv")
    out_xlsx = os.path.join(OUTPUT_DIR, "restaurants.xlsx")
    master.to_csv(out_csv,  index=False, encoding="utf-8-sig")
    master.to_excel(out_xlsx, index=False, engine="openpyxl")
    print(f"  output/restaurants.csv + .xlsx rebuilt ({len(master)} rows)")


# ── Main ──────────────────────────────────────────────────────────────────────
print("=" * 60)
print("  Sentiment Analysis  |  5-Tier / 3-Category")
print("=" * 60)

try:
    import torch
    DEVICE = 0 if torch.cuda.is_available() else -1
    print(f"\nPyTorch {torch.__version__} | device: {'GPU' if DEVICE == 0 else 'CPU'}")
except ImportError:
    print("ERROR: PyTorch not installed.")
    sys.exit(1)

print("\nLoading model: cross-encoder/nli-MiniLM2-L6-H768 ...")
classifier = pipeline(
    "zero-shot-classification",
    model="cross-encoder/nli-MiniLM2-L6-H768",
    device=DEVICE,
    batch_size=16,
)

# ── Step 1-4: Classify and aggregate both datasets ────────────────────────────
any_missing = False
for dataset in DATASETS:
    print(f"\n{'='*60}")
    print(f"  {dataset['label']}")
    print(f"{'='*60}")

    df = pd.read_csv(dataset["reviews_csv"], encoding="utf-8-sig")
    df = df.rename(columns={
        "Restaurant Name":       "title",
        "Google Review Ratings": "stars",
        "Reviews":               "text",
    })
    df["text"]  = df["text"].fillna("").astype(str)
    df["stars"] = pd.to_numeric(df["stars"], errors="coerce")
    print(f"\nLoaded {len(df):,} reviews across {df['title'].nunique()} restaurants")

    records    = classify_reviews(df, classifier, dataset["checkpoint"])
    reviews_df = save_review_level(records, dataset["review_out"], dataset["checkpoint"])
    missing    = aggregate_and_merge(reviews_df, dataset["restaurants_csv"])
    if missing > 0:
        any_missing = True

# ── Step 5-8: Fill gaps for restaurants still without reviews ─────────────────
if any_missing and API_KEY:
    print(f"\n{'='*60}")
    print("  Gap-Fill: Scraping missing restaurant reviews")
    print(f"{'='*60}")
    for dataset in DATASETS:
        print(f"\n-- {dataset['label']} --")
        fill_missing(dataset, classifier)
elif any_missing and not API_KEY:
    print("\nNote: GOOGLE_PLACES_API_KEY not set in .env — skipping gap-fill.")

# ── Step 9: Rebuild combined output ──────────────────────────────────────────
print(f"\n{'='*60}")
print("  Rebuilding output/restaurants.csv + .xlsx")
print(f"{'='*60}")
rebuild_output()

print("\nDone.")
