# Data Pre-Processing for Entirely Overrated

---

## Table of Contents

1. [Pre-Processing Overview](#1-pre-processing-overview)
2. [Data Sources](#2-data-sources)
3. [Project File Structure](#3-project-file-structure)
4. [Pipeline Scripts](#4-pipeline-scripts)
   - [preprocess_restaurant_data.py](#41-preprocess_restaurant_datapy)
   - [scrape_google_reviews.py](#42-scrape_google_reviewspy)
   - [sentiment_analysis.py](#43-sentiment_analysispy)
   - [preprocess_household_expenditure_data.py](#44-preprocess_household_expenditure_datapy)
5. [Utility Scripts](#5-utility-scripts)
   - [restaurant_region.py](#51-restaurant_regionpy)
   - [classify_cuisine.py](#52-classify_cuisinepy)
   - [_map_reviews.py](#53-_map_reviewspy)
   - [build_wordcloud_data.py](#54-build_wordcloud_datapy)
6. [Output Files](#6-output-files)
7. [Configuration Reference](#7-configuration-reference)
8. [How to Run](#8-how-to-run)
9. [Known Issues & Notes](#9-known-issues--notes)

---

## 1. Pre-Processing Overview

This repository contains the full data pre-processing pipeline for the
Entirely Overrated project. It ingests raw data from multiple public sources,
cleans and enriches it with Google Maps details and NLP-based review sentiment,
and produces Tableau-ready output files.

### What this pre-processing produces

| Output File | Description |
|-------------|-------------|
| **`output/restaurants.csv`** / **`.xlsx`** | ~2,060 Singapore restaurants (Michelin + Non-Michelin) with location, cuisine, award level, hygiene grade, and NLP sentiment scores |
| **`output/household_affordability.csv`** / **`.xlsx`** | ~2,060 restaurants (Michelin + Non-Michelin) × 5 income quintiles with 14 affordability metrics each (wide format, joins to restaurants on `place_id`) |
| **`output/reviews.csv`** / **`.xlsx`** | 244,631 word-level token counts per restaurant × star rating (for Tableau word cloud) |
| **`output/master.xlsx`** | Combined workbook — Restaurants, Household_Affordability, Reviews, and Column Definitions sheets |

### Pipeline

```
┌─────────────────────────────────────────────────────────┐
│  RAW DATA SOURCES                                       │
│                                                         │
│  Kaggle: michelin_guide_restaurants_2021                │
│    └── data/michelin_my_maps.csv  (Michelin listings)   │
│                                                         │
│  Apify: Google Maps Scraper                             │
│    └── non-michelin restaurant details                  │
│                                                         │
│  SingStat HES 2023                                      │
│    └── data/singstat_household_expenditure_2024.xlsx    │
│                                                         │
│  data.gov.sg + SFA                                      │
│    └── data/sfa_hygiene.csv  (hygiene grades)           │
└─────────────────────────────────────────────────────────┘
        │
        ▼
preprocess_restaurant_data.py
  • Bootstrap Michelin CSV from Kaggle source
  • Google Places API → place_id, phone, cuisine, website
  • Derive Region from Singapore postal district map
  • Merge SFA hygiene grades
        │  michelin_restaurants.csv
        │  non-michelin_restaurants.csv
        ▼
scrape_google_reviews.py
  • Google Places Details API → up to N reviews per restaurant
        │  reviews/michelin_reviews.csv
        │  reviews/non-michelin_reviews.csv
        ▼
sentiment_analysis.py
  • Zero-shot NLI (cross-encoder/nli-MiniLM2-L6-H768)
  • 3 categories × 5 tiers = 15 labels per review
  • Aggregates sentiment back into restaurant CSVs
        │  updates michelin_restaurants.csv
        │  updates non-michelin_restaurants.csv
        │  reviews/mi_review_level_sentiment.csv
        │  reviews/nm_review_level_sentiment.csv
        ▼
preprocess_household_expenditure_data.py
  • Parses SingStat T16 (expenditure) + T34 (income)
  • Computes affordability metrics per restaurant × quintile
  • Pivots to wide format (unique place_id)
        │
        ▼
_map_reviews.py  [utility]
  • Adds place_id to all review CSVs from master
  • Combines into reviews/all_reviews.csv
        │  reviews/all_reviews.csv
        ▼
build_wordcloud_data.py  [utility]
  • Tokenises reviews; removes stop words
  • Produces word × count per restaurant for Tableau
        │
        ▼
output/
  restaurants.csv / .xlsx              ← all restaurants
  household_affordability.csv / .xlsx  ← affordability by quintile
  reviews.csv / .xlsx                  ← word cloud token counts
  master.xlsx                          ← combined workbook (4 sheets)
```

---

## 2. Data Sources

| Dataset | Source | Description |
|---------|--------|-------------|
| **Michelin restaurant listings** | [Kaggle — Michelin Guide Restaurants 2021](https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021) | Singapore Michelin listings with name, address, price tier, award level, coordinates. Stored as `data/michelin_my_maps.csv`. |
| **Non-Michelin restaurant details** | [Apify — Google Maps Scraper](https://console.apify.com/actors/Xb8osYTtOjlsgI6k9/input) | Used to bulk-scrape Google Maps data (place_id, cuisine, phone, website) for non-Michelin restaurants. |
| **Household Expenditure Survey 2023** | [SingStat HES Dashboard](https://www.singstat.gov.sg/find-data/search-by-theme/households/household-expenditure/visualising-data/household-expenditure-survey-dashboard) | Average monthly household income (T34) and food/dining expenditure by goods & services category (T16), broken down by income quintile. Downloaded as `data/singstat_household_expenditure_2024.xlsx`. |
| **Google Places API** | Google Cloud Platform | Used in the preprocessing and scraping scripts to enrich both Michelin and Non-Michelin restaurants with `place_id`, phone number, cuisine type, website URL, and review text + star ratings. |
| **SFA Hygiene Grades** | [data.gov.sg — SFA Food Establishment Inspection](https://data.gov.sg/datasets/d_546a95c5e6a0a264a82247ec107a0629/view) / [SFA Track Records](https://www.sfa.gov.sg/tools-and-resources/track-records) | Singapore Food Agency hygiene grading (A–D) for food establishments. Applied to Michelin restaurants only. |
| **Singapore Postal District Map** | [PropertyGiant — Singapore Postal Districts](https://www.propertygiant.com/resource/singapore-postal-districts-map) | Maps postal district codes (D01–D28) to Singapore regions (Central / East / West / North / North-East). Used to derive the `Region` column from restaurant addresses. |

---

## 3. Project File Structure

```
data_preprocessing/
├── data/
│   ├── michelin_my_maps.csv                     Raw Michelin listings (bootstrap source)
│   └── singstat_household_expenditure_2024.xlsx  SingStat HES 2023
│
├── restaurants/                                 Intermediary restaurant CSVs
│   ├── michelin_restaurants.csv                 Enriched Michelin (293 rows)
│   └── non-michelin_restaurants.csv             Enriched Non-Michelin (~2,047 rows)
│
├── reviews/                                     Review CSVs (generated by scrape + utility steps)
│   ├── michelin_reviews.csv                     7,691 Michelin reviews with place_id
│   ├── non-michelin_reviews.csv                 6,563 Non-Michelin reviews with place_id
│   ├── mi_review_level_sentiment.csv            Per-review sentiment (Michelin)
│   ├── nm_review_level_sentiment.csv            Per-review sentiment (Non-Michelin)
│   ├── all_reviews.csv                          Combined 14,254 reviews with Is Michelin flag
│   └── wordcloud_data.csv                       244,631 word token counts
│
├── household_affordability/                     Reference and intermediary affordability files
│   ├── household_expenditure.xlsx               Reference workbook (income + food spending, 5 sheets)
│   ├── household_income_by_quintile.csv         Income by quintile + overall avg
│   ├── household_food_spending_by_quintile.csv  Food spending breakdown
│   ├── michelin_affordability.csv               Affordability per quintile × price tier
│   ├── michelin_price_distribution.csv          Restaurant count by price tier
│   └── income_quintile_reference.csv            Quintile parameter mapping for Tableau
│
├── output/                                      Tableau-ready output files
│   ├── restaurants.csv / .xlsx                  ~2,060 restaurants (Michelin + Non-Michelin)
│   ├── household_affordability.csv / .xlsx      293 Michelin restaurants × 5 quintiles
│   ├── reviews.csv / .xlsx                      Word-level token counts for word cloud
│   └── master.xlsx                              Combined workbook (4 sheets)
│
├── _backup/
│   ├── scripts/                                 Copies of all pipeline scripts
│   ├── intermediary_data/
│   │   ├── restaurants/                         Mirrors restaurants/ folder
│   │   ├── reviews/                             Mirrors reviews/ folder
│   │   └── household_affordability/             Mirrors household_affordability/ folder
│   └── output_data/                             Copies of all output/ files
│
├── preprocess_restaurant_data.py                Pipeline script 1
├── scrape_google_reviews.py                     Pipeline script 2
├── sentiment_analysis.py                        Pipeline script 3
├── preprocess_household_expenditure_data.py     Pipeline script 4
├── restaurant_region.py                         Utility — re-derive Region from postal codes
├── classify_cuisine.py                          Utility — preview cuisine classification
├── _map_reviews.py                              Utility — map place_id to reviews + build all_reviews.csv
├── build_wordcloud_data.py                      Utility — tokenise reviews for word cloud
├── .env                                         API keys (not committed)
└── README.md
```

---

## 4. Pipeline Scripts

### 4.1 `preprocess_restaurant_data.py`

**Purpose:** Bootstrap the Michelin restaurant list from the raw CSV, enrich
both Michelin and Non-Michelin restaurants with Google Places data (place_id,
phone, cuisine, website), apply SFA hygiene grade lookup, and combine into a
single `output/restaurants.csv`.

#### Input
| File | Description |
|------|-------------|
| `data/michelin_my_maps.csv` | Raw Michelin listings (used only if `michelin_restaurants.csv` does not exist) |
| `non-michelin_restaurants.csv` (manual) | Non-Michelin restaurants with basic columns |
| Google Places API | Geocoding + Places Details |

#### Process

**Step 0 – Bootstrap Michelin CSV** (only runs if `michelin_restaurants.csv` absent)
- Filters source CSV to `Location == 'Singapore'`
- Maps price symbols (`$` → 1, `$$` → 2, etc.)
- Formats phone numbers to Singapore `XXXX XXXX` format
- Writes `michelin_restaurants.csv` with `place_id` column left empty (filled in Step 2)

**Step 1 – Region from postal code**
- Derives `Region` (Central / East / West / North / North-East) from the last
  6 digits of the address using Singapore postal district mapping

**Step 2 – Place ID lookup** (`run_michelin()`)
- For each restaurant without a `place_id`, calls
  `Places Text Search API` with restaurant name + "Singapore"
- Saves progress to `pp_mi_placeid_progress.json` (resume-safe)
- Writes enriched `michelin_restaurants.csv`

**Step 3 – Google Places Details** (`run_michelin()`)
- For each restaurant, fetches phone number, website, cuisine type from
  `Places Details API`
- Saves progress to `pp_mi_details_progress.json`

**Step 4 – SFA Hygiene Grade** (Michelin only)
- Reads `data/sfa_hygiene.csv` if present; merges on restaurant name
- Assigns `SFA Hygiene Grade` (A–D) and `Safety Penalty` (0–4)

**Step 5 – Non-Michelin enrichment** (`run_non_michelin()`)
- Runs Steps 2–3 equivalents for Non-Michelin restaurants

**Step 6 – Rebuild output**
- Concatenates `michelin_restaurants.csv` + `non-michelin_restaurants.csv`
- Sets `Is Michelin` flag
- Fills missing descriptions with `"No Description Available Yet"`
- Saves `output/restaurants.csv` + `output/restaurants.xlsx`

#### Output
| File | Rows | Description |
|------|------|-------------|
| `michelin_restaurants.csv` | 293 | Enriched Michelin restaurants (intermediary) |
| `non-michelin_restaurants.csv` | ~2,047 | Enriched Non-Michelin restaurants (intermediary) |
| `output/restaurants.csv` | ~2,060 | Combined master (both datasets) |
| `output/restaurants.xlsx` | ~2,060 | Same as CSV, Excel format |

---

### 4.2 `scrape_google_reviews.py`

**Purpose:** Fetch up to N Google reviews per restaurant from the Places Details
API and save them for sentiment analysis.

#### Input
| File | Description |
|------|-------------|
| `michelin_restaurants.csv` | Provides `place_id` for each Michelin restaurant |
| `non-michelin_restaurants.csv` | Provides `place_id` for Non-Michelin |
| Google Places API (`GOOGLE_PLACES_API_KEY`) | Review text + star ratings |

#### Process
- Reads existing review CSVs and skips restaurants already scraped (resume-safe)
- Fetches reviews sorted by `newest` via Places Details API
- Filters to English-language reviews where possible
- Appends to `reviews/<prefix>_reviews.csv`

#### Output
| File | Description |
|------|-------------|
| `reviews/michelin_reviews.csv` | Raw reviews: Restaurant Name, Stars, Review text |
| `reviews/non-michelin_reviews.csv` | Same for Non-Michelin |

---

### 4.3 `sentiment_analysis.py`

**Purpose:** Run zero-shot NLI sentiment classification on all reviews across
three dimensions (Value, Service, Taste), aggregate per restaurant, and fill
gaps for restaurants with no reviews by re-scraping via the Places API.

#### Input
| File | Description |
|------|-------------|
| `reviews/michelin_reviews.csv` | Michelin review text + star ratings |
| `reviews/non-michelin_reviews.csv` | Non-Michelin reviews |
| `michelin_restaurants.csv` / `non-michelin_restaurants.csv` | Base restaurant files to merge results into |
| HuggingFace model: `cross-encoder/nli-MiniLM2-L6-H768` | NLI classifier (downloaded automatically) |

#### Process

**Sentiment model:** Zero-shot classification with `multi_label=True` against
15 candidate labels (3 categories × 5 tiers). The label with the highest score
per category is assigned as the tier.

**Categories and tiers:**

| Category | Tiers (best → worst) |
|----------|----------------------|
| Value | excellent (5) / good (4) / average (3) / poor (2) / terrible (1) |
| Service | excellent (5) / good (4) / average (3) / poor (2) / terrible (1) |
| Taste | excellent (5) / good (4) / average (3) / poor (2) / terrible (1) |

**Pipeline per dataset:**
1. Load reviews; resume from checkpoint if run was interrupted
2. Classify every review → `{cat}_tier` + `{cat}_score` per category
3. Save `reviews/<prefix>_review_level_sentiment.csv`
4. Aggregate per restaurant: mode for tier, mean for score, mean for stars
5. Merge 11 sentiment columns into `<prefix>_restaurants.csv`

**Gap-fill step** (requires `GOOGLE_PLACES_API_KEY`):
- Finds restaurants still at `Review Count == 0`
- Scrapes up to 5 Google reviews per restaurant
- Runs sentiment on new reviews only
- Appends to review-level CSV and re-aggregates

**Columns added to restaurant CSVs:**

| Column | Type | Description |
|--------|------|-------------|
| `Review Count` | int | Number of reviews processed |
| `Average Rating` | float | Mean star rating (1–5) |
| `value_tier` | string | Dominant sentiment tier for Value |
| `value_score` | float 0–1 | Mean model confidence for assigned value tier |
| `service_tier` | string | Dominant sentiment tier for Service |
| `service_score` | float 0–1 | Mean model confidence for service tier |
| `taste_tier` | string | Dominant sentiment tier for Taste |
| `taste_score` | float 0–1 | Mean model confidence for taste tier |
| `value_tier_numeric` | float 1–5 | Mean numeric score for Value (5=excellent) |
| `service_tier_numeric` | float 1–5 | Mean numeric score for Service |
| `taste_tier_numeric` | float 1–5 | Mean numeric score for Taste |

**Checkpoints** every 500 reviews allow safe interruption and resumption.

#### Output
| File | Description |
|------|-------------|
| `reviews/mi_review_level_sentiment.csv` | Per-review sentiment results (Michelin) |
| `reviews/nm_review_level_sentiment.csv` | Per-review sentiment results (Non-Michelin) |
| `michelin_restaurants.csv` | Updated with 11 sentiment columns |
| `non-michelin_restaurants.csv` | Updated with 11 sentiment columns |
| `output/restaurants.csv` + `.xlsx` | Rebuilt combined master |

---

### 4.4 `preprocess_household_expenditure_data.py`

**Purpose:** Parse SingStat HES 2023 data, compute affordability metrics for
each Michelin restaurant by income quintile, and produce a wide Tableau-ready
table (one row per restaurant, one set of columns per quintile).

#### Input
| File | Description |
|------|-------------|
| `data/singstat_household_expenditure_2024.xlsx` | SingStat HES 2023 — sheets T16 (expenditure) and T34 (income) |
| `michelin_restaurants.csv` | Michelin restaurants with `place_id` and `Price` tier |

#### Process

**Step 1 – Extract income by quintile (T34)**
- Parses sheet T34; rows 12–16 = Q1 to Q5 monthly household income
- Produces `Monthly Household Income ($)` and `Annual Household Income ($)`

**Step 2 – Extract food & dining expenditure by quintile (T16)**
- Parses sheet T16; locates rows by exact category label
- Extracts 7 spending categories per quintile:
  - Groceries, Total Eating Out, Restaurants & Cafes, Restaurants Only,
    Cafes, Fast Food, Hawker/Food Courts

**Step 3 – Build income + food summary**
- Merges income and food data; computes spending as % of income

**Step 4 – Michelin price distribution**
- Counts Michelin restaurants by price tier; averages sentiment scores per tier

**Step 5 – Compute affordability metrics**
- For each quintile × price tier combination:
  - Meals affordable per month (from restaurant budget)
  - Annual meals affordable
  - Cost per meal as % of monthly income
  - Affordability label (Very Affordable / Affordable / Moderate / Expensive /
    Very Expensive)

**Step 6 – Save outputs**
- Writes all master files (see Output below)

**Step 7 – Build Tableau affordability table (wide format)**
- One row per Michelin restaurant (unique `place_id`)
- 14 metric columns per quintile × 5 quintiles = 70 quintile columns
- Total: 74 columns (4 base + 70 quintile)

**Wide-format quintile columns (prefix Q1–Q5):**

| Column Suffix | Type | Description |
|---------------|------|-------------|
| `Monthly HH Income ($)` | float | Avg monthly household income for this quintile |
| `Monthly Restaurant Budget ($)` | float | Avg monthly spend at restaurants |
| `Annual Restaurant Budget ($)` | int | Monthly × 12 |
| `Visits Per Month` | float | Budget ÷ Cost Per Pax |
| `Visits Per Year` | float | Visits Per Month × 12 |
| `Cost as % of Income` | float | One visit ÷ monthly income × 100 |
| `Cost as % of Restaurant Budget` | float | One visit ÷ monthly restaurant budget × 100 |
| `Affordable Daily` | bool | ≥ 30 visits/month |
| `Affordable Weekly` | bool | ≥ 4 visits/month |
| `Affordable Monthly` | bool | ≥ 1 visit/month |
| `Affordable Quarterly` | bool | ≥ 1 visit per 3 months |
| `Affordable Annually` | bool | ≥ 1 visit per year |
| `Affordability Category` | string | Very Affordable / Affordable / Moderate / Expensive / Very Expensive |
| `Best Frequency Affordable` | string | Daily / Weekly / Monthly / Quarterly / Annually / Out of Reach |

**Affordability thresholds (cost as % of monthly income):**

| Category | Threshold |
|----------|-----------|
| Very Affordable | < 1% |
| Affordable | 1% – 3% |
| Moderate | 3% – 6% |
| Expensive | 6% – 12% |
| Very Expensive | > 12% |

**Income quintile definitions (SingStat HES 2023):**

| Prefix | Label | Monthly Income Range | Avg Monthly |
|--------|-------|---------------------|-------------|
| Q1 | Bottom 20% | $0 – $5,607 | $3,254 |
| Q2 | Lower-Mid 20% | $5,608 – $10,509 | $7,961 |
| Q3 | Middle 20% | $10,510 – $15,904 | $13,058 |
| Q4 | Upper-Mid 20% | $15,905 – $26,546 | $18,751 |
| Q5 | Top 20% | > $26,547 | $34,341 |

#### Output
| File | Location | Rows | Description |
|------|----------|------|-------------|
| `household_affordability.csv` | `output/` | ~2,060 | Wide Tableau join table (unique place_id, all restaurants) |
| `household_affordability.xlsx` | `output/` | ~2,060 | Same, Excel format |
| `master.xlsx` | `output/` | — | Combined workbook (4 sheets) |
| `household_expenditure.xlsx` | `household_affordability/` | — | Reference workbook (5 sheets) |
| `household_income_by_quintile.csv` | `household_affordability/` | 6 | Income by quintile + overall avg |
| `household_food_spending_by_quintile.csv` | `household_affordability/` | 6 | Food spending breakdown |
| `michelin_affordability.csv` | `household_affordability/` | 20 | Affordability per quintile × tier |
| `michelin_price_distribution.csv` | `household_affordability/` | 4 | Restaurant count by price tier |
| `income_quintile_reference.csv` | `household_affordability/` | 5 | Quintile parameter mapping for Tableau |

---

## 5. Utility Scripts

These scripts are run manually as needed after the main pipeline completes.
They are not part of the sequential pipeline but modify or extend its outputs.

### 5.1 `restaurant_region.py`

**Purpose:** Re-populate the `Region` column in `michelin_restaurants.csv` from
postal codes in the `Address` field, using the same district → region mapping as
the preprocessing pipeline. Also cross-checks `Cuisine` values against
`data/michelin_my_maps.csv` to flag hawker stalls incorrectly classified as
"Restaurant" by the Google Places API.

**Run when:** Region values are missing or incorrect after a re-scrape.

---

### 5.2 `classify_cuisine.py`

**Purpose:** Dry-run preview of the keyword-based cuisine classification rules.
Prints what would be changed without writing any files — useful for reviewing
the `RULES` list before applying changes.

**Run when:** Investigating or updating cuisine classification logic.

---

### 5.3 `_map_reviews.py`

**Purpose:** Adds `place_id` and `Is Michelin` to all four review CSVs by
joining on `Restaurant Name` from `output/restaurants.csv`. Drops reviews for
restaurants no longer in the master. Combines Michelin and Non-Michelin
sentiment CSVs into a single `reviews/all_reviews.csv`. Syncs all five files
to `_backup/intermediary_data/reviews/`.

**Run when:** Restaurant list changes (additions/deletions) or after a fresh
review scrape.

#### Output
| File | Rows | Description |
|------|------|-------------|
| `reviews/michelin_reviews.csv` | 7,691 | Michelin reviews with place_id |
| `reviews/non-michelin_reviews.csv` | 6,563 | Non-Michelin reviews with place_id |
| `reviews/mi_review_level_sentiment.csv` | 7,691 | Michelin sentiment with place_id |
| `reviews/nm_review_level_sentiment.csv` | 6,563 | Non-Michelin sentiment with place_id |
| `reviews/all_reviews.csv` | 14,254 | Combined reviews: place_id, Restaurant Name, Is Michelin, Google Review Ratings, Reviews + 9 sentiment columns |

---

### 5.4 `build_wordcloud_data.py`

**Purpose:** Tokenises all reviews in `reviews/all_reviews.csv` into individual
words, removes English stop words and words shorter than 3 characters, and
counts word frequency per (restaurant, star rating) combination. Produces a
flat table suitable for a Tableau hierarchical word cloud.

**Run when:** `all_reviews.csv` is updated or stop-word list is changed.

#### Output
| File | Rows | Description |
|------|------|-------------|
| `reviews/wordcloud_data.csv` | 244,631 | Columns: place_id, Restaurant Name, Is Michelin, Google Review Ratings, word, count |
| `output/reviews.csv` / `.xlsx` | 244,631 | Same file copied to output for Tableau |

**Tableau setup:** Connect to `reviews.csv`. Set mark type to Text. Drag `word`
to Text, `SUM(count)` to Size and Color. Use `Is Michelin` and `Restaurant Name`
as filters or pages for drill-down.

---

## 6. Output Files

### `output/restaurants.csv` / `.xlsx`
~2,060 rows. One row per restaurant (Michelin + Non-Michelin combined).
Key columns: `place_id`, `Restaurant Name`, `Address`, `Region`, `Price`,
`Cuisine`, `Michelin Award`, `Is Michelin`, sentiment columns.
**Primary join key:** `place_id`

### `output/household_affordability.csv` / `.xlsx`
~2,060 rows (Michelin + Non-Michelin). Wide format — one row per restaurant.
Columns: `place_id`, `Price Tier`, `Price Tier Label`, `Estimated Cost Per Pax ($)`,
then 70 quintile-prefixed columns (Q1–Q5 × 14 metrics).
**Primary join key:** `place_id`

### `output/reviews.csv` / `.xlsx`
244,631 rows. Word-level token counts per restaurant × star rating.
Columns: `place_id`, `Restaurant Name`, `Is Michelin`, `Google Review Ratings`, `word`, `count`.
**Primary join key:** `place_id`

### `output/master.xlsx`
Combined workbook with 4 sheets:

| Sheet | Contents |
|-------|----------|
| `Restaurants` | ~2,060 restaurants with enrichment + sentiment columns |
| `Household_Affordability` | 293-row wide affordability table |
| `Reviews` | 244,631-row word token table (mirrors reviews.csv) |
| `Column Definitions` | 7 reference tables: Restaurant columns, Affordability columns, Q1–Q5 Income Guide, Region by Postal Code, Sentiment model info, Affordability thresholds, Reviews columns |

---

## 7. Configuration Reference

### `preprocess_restaurant_data.py`
| Constant | Default | Description |
|----------|---------|-------------|
| `SOURCE_MI_CSV` | `data/michelin_my_maps.csv` | Bootstrap source for Michelin list |
| `API_DELAY` | 0.05s | Delay between Google API calls |
| `MAX_DETAILS_RETRIES` | 3 | Retry count for failed API calls |

### `sentiment_analysis.py`
| Constant | Default | Description |
|----------|---------|-------------|
| `MAX_CHARS` | 512 | Maximum review text length sent to model |
| `API_DELAY` | 0.05s | Delay between Places API calls in gap-fill |
| Model | `cross-encoder/nli-MiniLM2-L6-H768` | HuggingFace NLI model |
| `batch_size` | 16 | GPU/CPU batch size for classifier |

### `preprocess_household_expenditure_data.py`
| Constant | Default | Description |
|----------|---------|-------------|
| `PRICE_TIER_COST` | `{1:20, 2:60, 3:120, 4:250}` | Cost per pax (SGD) per Michelin price tier |
| `QUINTILE_RANGES` | See §4.4 income table | Income range boundaries for Q1–Q5 |

### `build_wordcloud_data.py`
| Constant | Default | Description |
|----------|---------|-------------|
| `STOP_WORDS` | ~120 words | English stop words + common review filler removed before counting |
| Min word length | 3 chars | Words shorter than 3 characters are excluded |

---

## 8. How to Run

### Prerequisites
```bash
pip install pandas openpyxl transformers torch tqdm
```

Set `GOOGLE_PLACES_API_KEY` in a `.env` file in the project root:
```
GOOGLE_PLACES_API_KEY=your_api_key_here
```

### Pipeline run order

```bash
# 1. Build + enrich restaurant lists (Michelin bootstrap + Google Places lookup)
python preprocess_restaurant_data.py

# 2. Scrape Google reviews
python scrape_google_reviews.py

# 3. Classify reviews with sentiment analysis (GPU recommended)
python sentiment_analysis.py

# 4. Compute household affordability and rebuild master outputs
python preprocess_household_expenditure_data.py
```

Scripts 1–3 are **resume-safe** — re-running will pick up from where they left off
using JSON progress files (`pp_mi_placeid_progress.json`, etc.) and CSV checkpoints.

Script 4 is idempotent — safe to re-run at any time.

### Utility scripts (run as needed)

```bash
# Re-derive Region column from postal codes + check cuisine labels
python restaurant_region.py

# Preview cuisine keyword classification rules (dry run, no file writes)
python classify_cuisine.py

# Add place_id to all review files + build all_reviews.csv
python _map_reviews.py

# Tokenise reviews → word cloud data for Tableau
python build_wordcloud_data.py
```

---

## 9. Known Issues & Notes

- **place_id empty for bootstrap rows:** Step 0 writes `michelin_restaurants.csv`
  with `place_id = ""`. Step 2 of `preprocess_restaurant_data.py` fills these
  in via the Places Text Search API. Run Step 2 before `sentiment_analysis.py`
  or `preprocess_household_expenditure_data.py` to ensure all place_ids are
  populated.

- **Non-English reviews:** The sentiment model works best with English text.
  Non-English reviews are processed but may produce lower-quality tier
  assignments. Google's `reviews_no_translations=true` flag is used to minimise
  machine-translated text.

- **SingStat income ranges:** The quintile income boundaries used in
  `QUINTILE_RANGES` are approximate midpoints between consecutive quintile
  averages from HES 2023. They are used for labelling and Tableau parameter
  mapping only — the actual affordability calculations use the official quintile
  average incomes from T34.

- **Street Food cuisine:** Google Places API returns "Restaurant" for hawker
  stalls. The correct label "Street Food" is sourced from `data/michelin_my_maps.csv`
  for Michelin entries and applied via address keyword matching for Non-Michelin.
  Run `restaurant_region.py` to verify no Michelin hawker stalls have reverted
  to "Restaurant" after a re-scrape.

- **master.xlsx sheet structure:** All scripts that write `output/master.xlsx`
  must use `pd.ExcelWriter` with named sheets (Restaurants, Household_Affordability,
  Reviews, Column Definitions) to preserve the multi-sheet structure. Using
  `df.to_excel('output/master.xlsx')` directly will overwrite it as a single sheet.
