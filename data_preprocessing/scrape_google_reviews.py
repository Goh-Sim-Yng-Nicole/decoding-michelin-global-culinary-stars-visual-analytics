"""
scrape_non_michelin_reviews.py
Fetches up to 5 newest Google reviews per restaurant from non-michelin_restaurants.csv
using the Google Places Details API (legacy, supports reviews_sort=newest).
Output: review/non-michelin_reviews.csv  (Restaurant Name, Google Review Ratings, Reviews)
Progress is saved every 50 restaurants so the script can be safely interrupted and resumed.
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request

import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')


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
API_KEY    = os.environ.get('GOOGLE_PLACES_API_KEY', '')
INPUT_CSV  = f"{BASE_DIR}/restaurants/non-michelin_restaurants.csv"
OUTPUT_CSV = f"{BASE_DIR}/reviews/non-michelin_reviews.csv"
PROG_FILE  = f"{BASE_DIR}/reviews/nm_review_progress.json"
SAVE_EVERY = 50
API_DELAY  = 0.05   # ~20 req/s


# ── Progress helpers ──────────────────────────────────────────────────────────
def load_progress():
    if os.path.exists(PROG_FILE):
        with open(PROG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_progress(done):
    with open(PROG_FILE, 'w', encoding='utf-8') as f:
        json.dump(done, f)


# ── API call ──────────────────────────────────────────────────────────────────
def fetch_reviews(place_id):
    """Return list of (rating, text) tuples for a place (up to 5)."""
    params = urllib.parse.urlencode({
        "place_id":               place_id,
        "key":                    API_KEY,
        "fields":                 "reviews",
        "reviews_sort":           "newest",
        "reviews_no_translations": "true",
    })
    url = f"https://maps.googleapis.com/maps/api/place/details/json?{params}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
        reviews = data.get("result", {}).get("reviews", [])
        return [(r.get("rating", ""), r.get("text", "")) for r in reviews]
    except Exception as e:
        print(f"    ✗ {place_id}: {e}")
        return []


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    df = pd.read_csv(INPUT_CSV)
    total = len(df)
    print(f"Loaded {total} restaurants from {INPUT_CSV.split('/')[-1]}")

    done = load_progress()

    # Load existing rows (support resume)
    if os.path.exists(OUTPUT_CSV) and done:
        existing = pd.read_csv(OUTPUT_CSV, encoding='utf-8-sig')
        rows = existing.to_dict('records')
        print(f"  Resuming — {len(done)} already done, {len(rows)} rows in output")
    else:
        rows = []
        print("  Starting fresh")

    new_places = 0
    new_reviews = 0

    for idx, record in df.iterrows():
        place_id = str(record['place_id'])
        name     = record['Restaurant Name']

        if place_id in done:
            continue

        reviews = fetch_reviews(place_id)
        for rating, text in reviews:
            if str(text).strip():
                rows.append({
                    'Restaurant Name':      name,
                    'Google Review Ratings': rating,
                    'Reviews':              text,
                })
                new_reviews += 1

        done[place_id] = len(reviews)
        new_places += 1

        # Progress report
        if new_places % 100 == 0:
            pct = (len(done) / total) * 100
            print(f"  [{len(done):>4}/{total}] {pct:.1f}%  "
                  f"— {new_reviews} new review rows this run")

        # Checkpoint
        if new_places % SAVE_EVERY == 0:
            save_progress(done)
            _save_output(rows)

        time.sleep(API_DELAY)

    # Final save
    save_progress(done)
    _save_output(rows)

    print(f"\nDone.")
    print(f"  Restaurants processed this run : {new_places}")
    print(f"  New review rows added          : {new_reviews}")
    print(f"  Total rows in output file      : {len(rows)}")
    print(f"  Output → {OUTPUT_CSV}")


def _save_output(rows):
    out = pd.DataFrame(rows, columns=['Restaurant Name', 'Google Review Ratings', 'Reviews'])
    out.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    main()
