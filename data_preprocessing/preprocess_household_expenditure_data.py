"""
preprocess_household_expenditure_data.py
=========================================
Parses SingStat Household Expenditure Survey 2023 data
(data/singstat_household_expenditure_2024.xlsx) and produces clean
CSV/XLSX outputs in output/ for affordability analysis against Michelin
restaurant price tiers.

Pipeline:
  Step 1 : Extract average monthly household income by income quintile (T34)
  Step 2 : Extract average monthly food & dining expenditure by quintile (T16)
  Step 3 : Build household income & food spending summary table
  Step 4 : Load Michelin restaurant distribution by price tier
  Step 5 : Compute affordability metrics per price tier × quintile
  Step 6 : Save all tables to output/household_expenditure.xlsx (multi-sheet)
           and individual CSVs
  Step 7 : Build Tableau-ready flat table (1 row per restaurant × quintile)
           with all dimensions and pre-computed affordability metrics

Output files (output/):
  household_expenditure.xlsx
    sheet "Income_and_Food_Summary"     — monthly/annual income + spending per quintile
    sheet "Food_Spending_by_Quintile"   — grocery + dining breakdown per quintile
    sheet "Michelin_Affordability"      — meals affordable, % of income, etc.
    sheet "Michelin_Price_Distribution" — count of Michelin restaurants by tier
    sheet "Tableau_Affordability"       — Tableau-ready flat table (restaurant × quintile)

  household_income_by_quintile.csv
  household_food_spending_by_quintile.csv
  michelin_affordability.csv
  michelin_price_distribution.csv
  tableau_michelin_affordability.csv    ← primary Tableau data source

Price-tier assumptions (cost per person, adjustable below):
  Tier 1 ($)    : ~$20  — hawker / kopitiam Michelin
  Tier 2 ($$)   : ~$60  — casual to mid-range dining
  Tier 3 ($$$)  : ~$120 — fine dining / tasting menu
  Tier 4 ($$$$) : ~$250 — ultra-premium fine dining
"""

import os
import sys

import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding="utf-8")


# ── Configuration ─────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
SOURCE     = os.path.join(BASE_DIR, "data", "singstat_household_expenditure_2024.xlsx")
MI_CSV     = os.path.join(BASE_DIR, "restaurants", "michelin_restaurants.csv")
NM_CSV     = os.path.join(BASE_DIR, "restaurants", "non-michelin_restaurants.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Estimated cost per person (SGD) for each Michelin price tier
PRICE_TIER_COST = {1: 20, 2: 60, 3: 120, 4: 250}
PRICE_TIER_LABEL = {
    1: "$ (~$20/pax, Hawker/Kopitiam)",
    2: "$$ (~$60/pax, Casual Dining)",
    3: "$$$ (~$120/pax, Fine Dining)",
    4: "$$$$ (~$250/pax, Ultra-Premium)",
}

QUINTILES = [
    "1st-20th (Lowest)",
    "21st-40th",
    "41st-60th",
    "61st-80th",
    "81st-100th (Highest)",
]

# Income quintile range boundaries (approximate — midpoints between consecutive
# quintile averages from SingStat HES 2023).  Used to label columns and to
# build the Tableau income-mapping reference table.
#
# Quintile averages: Q1=$3,254  Q2=$7,961  Q3=$13,058  Q4=$18,751  Q5=$34,341
# Midpoints:  Q1-Q2=(3254+7961)/2≈5,608   Q2-Q3≈10,510   Q3-Q4≈15,905   Q4-Q5≈26,546
#
# Each entry: (income_min, income_max_or_None, pct_label, column_prefix)
QUINTILE_RANGES = {
    1: (0,      5607,  "Bottom 20%",    "Q1"),
    2: (5608,  10509,  "Lower-Mid 20%", "Q2"),
    3: (10510, 15904,  "Middle 20%",    "Q3"),
    4: (15905, 26546,  "Upper-Mid 20%", "Q4"),
    5: (26547, None,   "Top 20%",       "Q5"),
}


# ── Parser helpers ────────────────────────────────────────────────────────────
def _row_value(df, row_idx, col_idx=1):
    """Return numeric value from a DataFrame cell, or None."""
    try:
        v = df.iloc[row_idx, col_idx]
        return float(str(v).replace(",", "")) if str(v).strip() not in ("nan", "-", "") else None
    except (ValueError, IndexError):
        return None


def _find_row(df, label):
    """Return row index where column 0 matches label (strip whitespace)."""
    for i, row in df.iterrows():
        if str(row.iloc[0]).strip() == label.strip():
            return i
    return None


# ── Step 1: Income by quintile ────────────────────────────────────────────────
def extract_income(xl):
    print("\nStep 1: Extracting income by quintile (T34)")
    df = xl.parse("T34", header=None)

    # Rows 11-16: Total + 5 quintile rows (header is rows 9-10, data starts row 11)
    # row 11 = Total, rows 12-16 = Q1..Q5
    quintile_rows = [12, 13, 14, 15, 16]   # iloc indices
    records = []
    for i, (qrow, qlabel) in enumerate(zip(quintile_rows, QUINTILES)):
        monthly = _row_value(df, qrow, 1)   # column 1 = "Total" income
        if monthly is None:
            continue
        records.append({
            "Quintile":               qlabel,
            "Quintile Rank":          i + 1,
            "Monthly Household Income ($)":  monthly,
            "Annual Household Income ($)":   round(monthly * 12),
        })

    # Also add overall average
    total_monthly = _row_value(df, 11, 1)
    records.insert(0, {
        "Quintile":               "Overall Average",
        "Quintile Rank":          0,
        "Monthly Household Income ($)":  total_monthly,
        "Annual Household Income ($)":   round(total_monthly * 12),
    })

    income_df = pd.DataFrame(records)
    print(f"  Extracted {len(income_df)} rows")
    print(income_df.to_string(index=False))
    return income_df


# ── Step 2: Food & dining expenditure by quintile ─────────────────────────────
def extract_food_spending(xl):
    print("\nStep 2: Extracting food & dining expenditure by quintile (T16)")
    df = xl.parse("T16", header=None)

    # Columns: 0=label, 1=Total, 2=Q1, 3=Q2, 4=Q3, 5=Q4, 6=Q5
    COLS = [1, 2, 3, 4, 5, 6]   # col indices → [Total, Q1..Q5]

    def get_row(label):
        idx = _find_row(df, label)
        if idx is None:
            return [None] * len(COLS)
        return [_row_value(df, idx, c) for c in COLS]

    # Category labels exactly as they appear in column 0
    cat_map = {
        "groceries":          "FOOD AND NON-ALCOHOLIC BEVERAGES",
        "eating_out_total":   "FOOD AND BEVERAGE SERVING SERVICES",
        "restaurants_cafes":  "  RESTAURANTS, CAFES AND PUBS",
        "restaurants_only":   "    Restaurants",
        "cafes":              "    Cafes",
        "fast_food":          "  FAST FOOD RESTAURANTS",
        "hawker":             "  HAWKER CENTRES, FOOD COURTS, COFFEE SHOPS, CANTEENS, KIOSKS AND STREET VENDORS",
    }

    rows_data = {k: get_row(v) for k, v in cat_map.items()}

    group_labels = ["Overall Average"] + QUINTILES
    records = []
    for gi, (grp, col_idx) in enumerate(zip(group_labels, range(len(COLS)))):
        groceries       = rows_data["groceries"][col_idx]
        eating_out      = rows_data["eating_out_total"][col_idx]
        restaurants_cafes = rows_data["restaurants_cafes"][col_idx]
        restaurants     = rows_data["restaurants_only"][col_idx]
        cafes           = rows_data["cafes"][col_idx]
        fast_food       = rows_data["fast_food"][col_idx]
        hawker          = rows_data["hawker"][col_idx]

        records.append({
            "Quintile":                                    grp,
            "Quintile Rank":                               gi,
            "Monthly Groceries ($)":                       groceries,
            "Monthly Total Eating Out ($)":                eating_out,
            "Monthly Restaurants & Cafes ($)":             restaurants_cafes,
            "Monthly Restaurants Only ($)":                restaurants,
            "Monthly Cafes ($)":                           cafes,
            "Monthly Fast Food ($)":                       fast_food,
            "Monthly Hawker/Food Courts ($)":              hawker,
            "Annual Total Eating Out ($)":                 round(eating_out * 12) if eating_out else None,
            "Annual Restaurants Only ($)":                 round(restaurants * 12) if restaurants else None,
        })

    food_df = pd.DataFrame(records)
    print(f"  Extracted {len(food_df)} rows")
    print(food_df[["Quintile", "Monthly Groceries ($)",
                   "Monthly Total Eating Out ($)", "Monthly Restaurants Only ($)"]
                  ].to_string(index=False))
    return food_df


# ── Step 3: Combined income + food spending summary ───────────────────────────
def build_summary(income_df, food_df):
    print("\nStep 3: Building household income & food spending summary")
    merged = income_df.merge(food_df, on=["Quintile", "Quintile Rank"], how="outer")

    # Derived ratios
    merged["Eating Out % of Income"] = (
        merged["Monthly Total Eating Out ($)"] /
        merged["Monthly Household Income ($)"] * 100
    ).round(1)
    merged["Restaurant % of Income"] = (
        merged["Monthly Restaurants Only ($)"] /
        merged["Monthly Household Income ($)"] * 100
    ).round(1)
    merged["Groceries % of Income"] = (
        merged["Monthly Groceries ($)"] /
        merged["Monthly Household Income ($)"] * 100
    ).round(1)

    # Sort by quintile rank
    merged = merged.sort_values("Quintile Rank").reset_index(drop=True)
    print(f"  Summary table: {len(merged)} rows × {len(merged.columns)} columns")
    return merged


# ── Step 4: Michelin price distribution ───────────────────────────────────────
def extract_michelin_distribution():
    print("\nStep 4: Loading Michelin restaurant price distribution")
    if not os.path.exists(MI_CSV):
        print(f"  WARNING: {MI_CSV} not found — skipping price distribution")
        return pd.DataFrame()

    df = pd.read_csv(MI_CSV, dtype={"Phone Number": str}, encoding="utf-8-sig")
    counts = (
        df.groupby("Price")
        .agg(
            Restaurant_Count=("Restaurant Name", "count"),
            Avg_Value_Score=("value_score", "mean"),
            Avg_Service_Score=("service_score", "mean"),
            Avg_Taste_Score=("taste_score", "mean"),
            Avg_Review_Rating=("Average Rating", "mean"),
        )
        .reset_index()
        .rename(columns={"Price": "Price Tier"})
    )
    counts["Price Tier Label"]         = counts["Price Tier"].map(PRICE_TIER_LABEL)
    counts["Estimated Cost Per Pax ($)"] = counts["Price Tier"].map(PRICE_TIER_COST)
    counts["Pct of Michelin Restaurants (%)"] = (
        counts["Restaurant_Count"] / counts["Restaurant_Count"].sum() * 100
    ).round(1)
    for col in ["Avg_Value_Score", "Avg_Service_Score", "Avg_Taste_Score", "Avg_Review_Rating"]:
        counts[col] = counts[col].round(3)

    counts = counts.rename(columns={
        "Restaurant_Count":    "Number of Restaurants",
        "Avg_Value_Score":     "Avg Value Score",
        "Avg_Service_Score":   "Avg Service Score",
        "Avg_Taste_Score":     "Avg Taste Score",
        "Avg_Review_Rating":   "Avg Review Rating",
    })
    print(counts[["Price Tier", "Price Tier Label", "Number of Restaurants",
                  "Pct of Michelin Restaurants (%)"]].to_string(index=False))
    return counts


# ── Step 5: Affordability analysis ────────────────────────────────────────────
def compute_affordability(income_df, food_df):
    print("\nStep 5: Computing Michelin affordability metrics")
    records = []

    # Skip "Overall Average" row (rank 0) for per-quintile analysis
    q_income = income_df[income_df["Quintile Rank"] > 0].copy()
    q_food   = food_df[food_df["Quintile Rank"] > 0].copy()
    merged   = q_income.merge(q_food, on=["Quintile", "Quintile Rank"])

    for _, row in merged.iterrows():
        monthly_income      = row["Monthly Household Income ($)"]
        monthly_restaurants = row["Monthly Restaurants Only ($)"]
        quintile            = row["Quintile"]
        qrank               = int(row["Quintile Rank"])

        for tier, cost in PRICE_TIER_COST.items():
            meals_from_restaurant_budget = (
                monthly_restaurants / cost if (monthly_restaurants and cost) else None
            )
            pct_income_per_meal = (
                cost / monthly_income * 100 if monthly_income else None
            )
            annual_michelin_budget = monthly_restaurants * 12 if monthly_restaurants else None
            annual_meals = annual_michelin_budget / cost if (annual_michelin_budget and cost) else None

            # Affordability label
            if pct_income_per_meal is None:
                label = "Unknown"
            elif pct_income_per_meal < 1:
                label = "Very Affordable"
            elif pct_income_per_meal < 3:
                label = "Affordable"
            elif pct_income_per_meal < 6:
                label = "Moderate"
            elif pct_income_per_meal < 12:
                label = "Expensive"
            else:
                label = "Very Expensive"

            records.append({
                "Quintile":                           quintile,
                "Quintile Rank":                      qrank,
                "Monthly Household Income ($)":       monthly_income,
                "Annual Household Income ($)":        round(monthly_income * 12),
                "Price Tier":                         tier,
                "Price Tier Label":                   PRICE_TIER_LABEL[tier],
                "Estimated Cost Per Pax ($)":         cost,
                "Monthly Restaurant Budget ($)":      monthly_restaurants,
                "Meals Affordable / Month (from restaurant budget)":
                    round(meals_from_restaurant_budget, 1) if meals_from_restaurant_budget else None,
                "Annual Restaurant Budget ($)":       round(annual_michelin_budget) if annual_michelin_budget else None,
                "Annual Meals Affordable (from restaurant budget)":
                    round(annual_meals, 0) if annual_meals else None,
                "Cost Per Meal as % of Monthly Income":
                    round(pct_income_per_meal, 2) if pct_income_per_meal else None,
                "Affordability":                      label,
            })

    aff_df = pd.DataFrame(records).sort_values(
        ["Price Tier", "Quintile Rank"]
    ).reset_index(drop=True)
    print(f"  Affordability table: {len(aff_df)} rows")
    print(aff_df[["Quintile", "Price Tier Label",
                  "Meals Affordable / Month (from restaurant budget)",
                  "Cost Per Meal as % of Monthly Income",
                  "Affordability"]].to_string(index=False))
    return aff_df


# ── Step 7: Tableau-ready affordability table (wide, unique place_id) ─────────
def build_tableau_table(income_df, food_df):
    """
    Produce one row per restaurant (Michelin + Non-Michelin) with a unique place_id.
    Quintile affordability metrics are pivoted WIDE as Q1_…Q5_ prefixed columns.

    Restaurant detail columns (name, cuisine, region, scores, etc.) are intentionally
    excluded — they already exist in restaurants.xlsx and will be brought in via a
    place_id join in Tableau.

    Affordability frequency flags (from restaurant dining budget):
      Daily    : ≥ 30 visits / month  (every day)
      Weekly   : ≥  4 visits / month  (every week)
      Monthly  : ≥  1 visit  / month  (once a month)
      Quarterly: ≥  1 visit  / 3 months
      Annually : ≥  1 visit  / year
    """
    print("\nStep 7: Building Tableau affordability table (wide, unique place_id)")
    if not os.path.exists(MI_CSV):
        print(f"  WARNING: {MI_CSV} not found — skipping Tableau table")
        return pd.DataFrame()

    mi = pd.read_csv(MI_CSV, dtype={"Phone Number": str}, encoding="utf-8-sig")
    nm = pd.read_csv(NM_CSV, dtype={"Phone Number": str}, encoding="utf-8-sig") if os.path.exists(NM_CSV) else pd.DataFrame()
    restaurants = pd.concat([mi, nm], ignore_index=True)
    print(f"  Loaded {len(mi)} Michelin + {len(nm)} Non-Michelin = {len(restaurants)} restaurants")

    q_income  = income_df[income_df["Quintile Rank"] > 0].copy()
    q_food    = food_df[food_df["Quintile Rank"] > 0].copy()
    quintiles = q_income.merge(q_food, on=["Quintile", "Quintile Rank"]).sort_values("Quintile Rank")

    # Column prefix = full descriptive label including income range
    Q_PREFIX = {rank: info[3] for rank, info in QUINTILE_RANGES.items()}

    def _aff_cat(pct):
        if pct is None:     return "Unknown"
        if pct < 1:         return "Very Affordable"
        if pct < 3:         return "Affordable"
        if pct < 6:         return "Moderate"
        if pct < 12:        return "Expensive"
        return "Very Expensive"

    def _freq_label(visits):
        if visits is None:          return "Unknown"
        if visits >= 30:            return "Daily"
        if visits >= 4:             return "Weekly"
        if visits >= 1:             return "Monthly"
        if visits >= (1 / 3):       return "Quarterly"
        if visits >= (1 / 12):      return "Annually"
        return "Out of Reach"

    records = []
    for _, r in restaurants.iterrows():
        price_tier = r.get("Price")
        cost       = PRICE_TIER_COST.get(price_tier)

        row = {
            "place_id":                   r.get("place_id", ""),
            "Price Tier":                 price_tier,
            "Price Tier Label":           PRICE_TIER_LABEL.get(price_tier, ""),
            "Estimated Cost Per Pax ($)": cost,
        }

        if cost is None:
            records.append(row)
            continue

        for _, qrow in quintiles.iterrows():
            qrank           = int(qrow["Quintile Rank"])
            p               = Q_PREFIX[qrank]
            monthly_income  = qrow["Monthly Household Income ($)"]
            monthly_rest    = qrow["Monthly Restaurants Only ($)"]
            annual_rest     = round(monthly_rest * 12) if monthly_rest else None

            visits_month    = (monthly_rest / cost)    if (monthly_rest and cost) else None
            visits_year     = (visits_month * 12)      if visits_month else None
            pct_income      = (cost / monthly_income * 100) if monthly_income else None
            pct_rest_bgt    = (cost / monthly_rest * 100)   if monthly_rest   else None

            row[f"{p} Monthly HH Income ($)"]          = monthly_income
            row[f"{p} Monthly Restaurant Budget ($)"]  = monthly_rest
            row[f"{p} Annual Restaurant Budget ($)"]   = annual_rest
            row[f"{p} Visits Per Month"]               = round(visits_month, 2)  if visits_month else None
            row[f"{p} Visits Per Year"]                = round(visits_year, 1)   if visits_year  else None
            row[f"{p} Cost as % of Income"]            = round(pct_income, 2)    if pct_income   else None
            row[f"{p} Cost as % of Restaurant Budget"] = round(pct_rest_bgt, 1)  if pct_rest_bgt else None
            row[f"{p} Affordable Daily"]               = visits_month is not None and visits_month >= 30
            row[f"{p} Affordable Weekly"]              = visits_month is not None and visits_month >= 4
            row[f"{p} Affordable Monthly"]             = visits_month is not None and visits_month >= 1
            row[f"{p} Affordable Quarterly"]           = visits_month is not None and visits_month >= (1 / 3)
            row[f"{p} Affordable Annually"]            = visits_month is not None and visits_month >= (1 / 12)
            row[f"{p} Affordability Category"]         = _aff_cat(pct_income)
            row[f"{p} Best Frequency Affordable"]      = _freq_label(visits_month)

        records.append(row)

    tableau_df = pd.DataFrame(records)

    dupe_count = tableau_df["place_id"].duplicated().sum()
    if dupe_count:
        print(f"  WARNING: {dupe_count} duplicate place_ids found — check source data")
    else:
        print(f"  place_id uniqueness: OK ({len(tableau_df)} unique rows)")

    print(f"  Tableau table: {len(tableau_df)} rows × {len(tableau_df.columns)} columns")
    print(f"  Columns: place_id + price tier info + {len(quintiles)} × 14 quintile metric columns")
    return tableau_df


# ── Quintile reference table (Tableau parameter mapping) ─────────────────────
def build_quintile_reference(income_df, food_df):
    """
    Small lookup table (5 rows) that maps monthly household income ranges to
    quintile affordability context.  Use this in Tableau as the source for an
    Income Parameter calculation:
        IF [User Monthly Income] <= [Income Range Max ($)] THEN [Quintile Label] …
    """
    q_income = income_df[income_df["Quintile Rank"] > 0].copy()
    q_food   = food_df[food_df["Quintile Rank"] > 0].copy()
    merged   = q_income.merge(q_food, on=["Quintile", "Quintile Rank"]).sort_values("Quintile Rank")

    records = []
    for _, row in merged.iterrows():
        qrank = int(row["Quintile Rank"])
        rng   = QUINTILE_RANGES[qrank]
        records.append({
            "Quintile Rank":                       qrank,
            "Quintile Label":                      rng[2],
            "Percentile Band":                     row["Quintile"],
            "Income Range Min ($/mth)":            rng[0],
            "Income Range Max ($/mth)":            rng[1] if rng[1] else ">$26,546",
            "Avg Monthly Household Income ($)":    row["Monthly Household Income ($)"],
            "Avg Annual Household Income ($)":     row["Annual Household Income ($)"],
            "Avg Monthly Restaurant Budget ($)":   row["Monthly Restaurants Only ($)"],
            "Avg Annual Restaurant Budget ($)":    round(row["Monthly Restaurants Only ($)"] * 12),
            "Avg Monthly Total Eating Out ($)":    row["Monthly Total Eating Out ($)"],
            "Avg Annual Total Eating Out ($)":     round(row["Monthly Total Eating Out ($)"] * 12),
            "Restaurant Budget as % of Income":    round(
                row["Monthly Restaurants Only ($)"] /
                row["Monthly Household Income ($)"] * 100, 1
            ),
        })
    return pd.DataFrame(records)


# ── Column definitions builder (all 5 tables for master.xlsx) ─────────────────
def build_column_guide(income_df, food_df):
    """
    Returns five DataFrames — one per table in the '_Definitions' sheet:
      1. restaurant_cols  — Restaurants sheet column reference
      2. affordability_cols — Household_Affordability column reference
      3. quintile_guide  — Q1-Q5 income range definitions
      4. region_postal   — Singapore region ↔ postal district mapping
      5. sentiment_ref   — Sentiment analysis categories, tiers and scores
    """
    q_income = income_df[income_df["Quintile Rank"] > 0].sort_values("Quintile Rank")
    q_food   = food_df[food_df["Quintile Rank"] > 0].sort_values("Quintile Rank")
    merged   = q_income.merge(q_food, on=["Quintile", "Quintile Rank"])

    # ── 1. Restaurant columns ─────────────────────────────────────────────────
    restaurant_cols = pd.DataFrame([
        ("place_id",                  "String",     "Unique Google Places ID. Primary join key across all tables."),
        ("Restaurant Name",           "String",     "Cleaned display name of the restaurant."),
        ("Address",                   "String",     "Full street address (Singapore postal code included where available)."),
        ("Country",                   "String",     "Always 'Singapore'."),
        ("Region",                    "String",     "Geographic region derived from postal code. See Region by Postal tab."),
        ("Price",                     "Integer 1-4","Price tier. 1=$, 2=$$, 3=$$$, 4=$$$$. Maps to Michelin price symbols."),
        ("Cuisine",                   "String",     "Primary cuisine type fetched from Google Places API."),
        ("Longitude",                 "Float",      "GPS longitude (WGS84)."),
        ("Latitude",                  "Float",      "GPS latitude (WGS84)."),
        ("Phone Number",              "String",     "Singapore number formatted as XXXX XXXX. 'No Phone Number Listed' if unavailable."),
        ("Michelin Guide Post Link",  "String",     "URL to the official Michelin Guide listing. 'Not in Michelin Guide Yet' for non-Michelin."),
        ("Google Website Link",       "String",     "Google Maps URL for the restaurant."),
        ("Michelin Award",            "String",     "Award level: 3 Stars / 2 Stars / 1 Star / Bib Gourmand / Selected Restaurants / Not Awarded Any Yet."),
        ("Facilities And Services",   "String",     "Comma-separated list of amenities from Google Places (e.g. Dine-in, Takeaway, Reservations)."),
        ("Description",               "String",     "Editorial summary from Google Places. 'No Description Available Yet' if missing."),
        ("SFA Hygiene Grade",         "String A-D", "Singapore Food Agency hygiene grade (Michelin only). A=best."),
        ("Safety Penalty",            "Integer 0-4","Numeric penalty from SFA grade. A=0, B=1, C=2, D=4."),
        ("Review Count",              "Integer",    "Number of Google reviews used in sentiment analysis."),
        ("Average Rating",            "Float 1-5",  "Mean star rating across all processed Google reviews."),
        ("value_tier",                "String",     "Dominant sentiment tier for Value. One of: excellent / good / average / poor / terrible."),
        ("value_score",               "Float 0-1",  "Model confidence score for the assigned value tier."),
        ("service_tier",              "String",     "Dominant sentiment tier for Service."),
        ("service_score",             "Float 0-1",  "Model confidence score for the assigned service tier."),
        ("taste_tier",                "String",     "Dominant sentiment tier for Taste/Food quality."),
        ("taste_score",               "Float 0-1",  "Model confidence score for the assigned taste tier."),
        ("value_tier_numeric",        "Float 1-5",  "Mean numeric score for value across all reviews (5=excellent, 1=terrible)."),
        ("service_tier_numeric",      "Float 1-5",  "Mean numeric score for service across all reviews."),
        ("taste_tier_numeric",        "Float 1-5",  "Mean numeric score for taste across all reviews."),
        ("Is Michelin",               "Boolean",    "TRUE for Michelin-listed restaurants, FALSE for non-Michelin."),
    ], columns=["Column Name", "Data Type", "Description"])

    # ── 2. Household Affordability columns ───────────────────────────────────
    affordability_cols = pd.DataFrame([
        ("place_id",                        "String",     "Join key — matches place_id in the Restaurants sheet."),
        ("Price Tier",                       "Integer 1-4","Michelin price tier (1=$  2=$$  3=$$$  4=$$$$)."),
        ("Price Tier Label",                 "String",     "Human-readable tier with estimated cost per person."),
        ("Estimated Cost Per Pax ($)",       "Integer",    "Assumed cost per person (SGD): Tier1=$20, Tier2=$60, Tier3=$120, Tier4=$250."),
        ("Q{n} Monthly HH Income ($)",       "Float",      "Average monthly household income for income group Q{n} (SGD). Same for all rows with the same Q{n}."),
        ("Q{n} Monthly Restaurant Budget ($)","Float",     "Average monthly spend at restaurants for Q{n} households. Source: SingStat HES 2023."),
        ("Q{n} Annual Restaurant Budget ($)", "Integer",   "Monthly Restaurant Budget × 12."),
        ("Q{n} Visits Per Month",            "Float",      "Visits affordable per month from restaurant budget. Formula: Monthly Budget ÷ Cost Per Pax."),
        ("Q{n} Visits Per Year",             "Float",      "Visits Per Month × 12."),
        ("Q{n} Cost as % of Income",         "Float",      "One visit as % of monthly household income. Formula: Cost Per Pax ÷ Monthly Income × 100."),
        ("Q{n} Cost as % of Restaurant Budget","Float",    "One visit as % of monthly restaurant budget."),
        ("Q{n} Affordable Daily",            "Boolean",    "TRUE if household can afford ≥ 30 visits/month (dining daily)."),
        ("Q{n} Affordable Weekly",           "Boolean",    "TRUE if household can afford ≥ 4 visits/month (dining weekly)."),
        ("Q{n} Affordable Monthly",          "Boolean",    "TRUE if household can afford ≥ 1 visit/month."),
        ("Q{n} Affordable Quarterly",        "Boolean",    "TRUE if household can afford ≥ 1 visit per quarter."),
        ("Q{n} Affordable Annually",         "Boolean",    "TRUE if household can afford ≥ 1 visit per year."),
        ("Q{n} Affordability Category",      "String",     "Very Affordable (<1% of income) / Affordable (1-3%) / Moderate (3-6%) / Expensive (6-12%) / Very Expensive (>12%)."),
        ("Q{n} Best Frequency Affordable",   "String",     "Highest sustainable visit frequency: Daily / Weekly / Monthly / Quarterly / Annually / Out of Reach."),
    ], columns=["Column Name", "Data Type", "Description"])

    # ── 3. Q1-Q5 Income Guide ────────────────────────────────────────────────
    quintile_rows = []
    for _, row in merged.iterrows():
        qrank = int(row["Quintile Rank"])
        rng   = QUINTILE_RANGES[qrank]
        income_range = "$0 – $5,607" if qrank == 1 else \
                       f"${rng[0]:,} – ${rng[1]:,}" if rng[1] else f"> ${rng[0]:,}"
        quintile_rows.append({
            "Column Prefix":                        f"Q{qrank}",
            "Label":                                rng[2],
            "Percentile Band":                      row["Quintile"],
            "Monthly Household Income Range (SGD)": income_range,
            "Avg Monthly Household Income (SGD)":   int(row["Monthly Household Income ($)"]),
            "Avg Annual Household Income (SGD)":    int(row["Annual Household Income ($)"]),
            "Avg Monthly Restaurant Budget (SGD)":  row["Monthly Restaurants Only ($)"],
            "Avg Annual Restaurant Budget (SGD)":   round(row["Monthly Restaurants Only ($)"] * 12),
            "Restaurant Budget as % of Income":     f"{round(row['Monthly Restaurants Only ($)'] / row['Monthly Household Income ($)'] * 100, 1)}%",
            "Data Source":                          "SingStat Household Expenditure Survey 2023",
        })
    quintile_guide = pd.DataFrame(quintile_rows)

    # ── 4. Region by Postal Code ─────────────────────────────────────────────
    region_postal = pd.DataFrame([
        ("D01","01–06","Central", "Raffles Place, City Hall, Marina Bay, Tanjong Pagar"),
        ("D02","07–08","Central", "Anson, Shenton Way"),
        ("D03","14–16","Central", "Alexandra, Queenstown, Tiong Bahru"),
        ("D04","09–10","Central", "Sentosa, Telok Blangah, Harbourfront"),
        ("D05","11–13","Central", "Buona Vista, West Coast, Clementi New Town"),
        ("D06","17",   "Central", "High Street, Beach Road (City Area)"),
        ("D07","18–19","Central", "Little India, Farrer Park, Rochor, Bugis"),
        ("D08","20–21","Central", "Orchard, Balmoral, Cairnhill, River Valley (north)"),
        ("D09","22–23","Central", "Orchard Road, River Valley"),
        ("D10","24–27","Central", "Bukit Timah, Holland Road, Balmoral"),
        ("D11","28–30","Central", "Newton, Novena, Thomson, Cairnhill"),
        ("D12","31–33","Central", "Balestier, Toa Payoh, Serangoon"),
        ("D13","34–37","Central", "Macpherson, Braddell"),
        ("D14","38–41","Central", "Geylang, Eunos, Paya Lebar"),
        ("D15","42–45","Central", "Katong, Joo Chiat, Amber Road, Marine Parade"),
        ("D16","46–48","East",    "Bedok, Upper East Coast, Eastwood, Kew Drive"),
        ("D17","49–50, 81","East","Loyang, Changi, Pasir Ris, Changi Airport"),
        ("D18","51–52","East",    "Tampines, Pasir Ris"),
        ("D19","53–55, 82","North-East","Serangoon Gardens, Hougang, Punggol (part)"),
        ("D20","56–57","North-East","Bishan, Ang Mo Kio"),
        ("D21","58–59","Central", "Upper Bukit Timah, Ulu Pandan, Clementi Park"),
        ("D22","60–64","West",    "Jurong, Jurong East, Jurong West"),
        ("D23","65–68","West",    "Hillview, Bukit Batok, Bukit Panjang, Choa Chu Kang"),
        ("D24","69–71","West",    "Lim Chu Kang, Tengah, Kranji (west)"),
        ("D25","72–73","North",   "Kranji, Woodgrove, Woodlands"),
        ("D26","77–78","North",   "Mandai, Upper Thomson"),
        ("D27","75–76","North",   "Yishun, Sembawang"),
        ("D28","79–80","North-East","Seletar, Punggol, Sengkang"),
    ], columns=["District", "Postal Code Prefix(es)", "Region", "Coverage Areas"])

    # ── 5. Sentiment Analysis reference ──────────────────────────────────────
    sentiment_meta = pd.DataFrame([
        ("Model",    "cross-encoder/nli-MiniLM2-L6-H768",
         "Zero-shot Natural Language Inference model from HuggingFace. "
         "Classifies free-text reviews against candidate label descriptions."),
        ("Method",   "Zero-shot classification (multi_label=True)",
         "Each review is scored against all 15 labels simultaneously. "
         "The label with the highest score within each category becomes the tier."),
        ("Input",    "Google review text (truncated to 512 chars)",
         "Reviews are fetched from the Google Places Details API (up to 5 per restaurant)."),
        ("Categories","3: Value, Service, Taste", "Three dimensions assessed per review."),
        ("Tiers",    "5 per category (15 total labels)",
         "excellent / good / average / poor / terrible for each category."),
        ("Aggregation","Mode for tier label, Mean for scores",
         "Per-restaurant tier = most common tier across all reviews. "
         "Per-restaurant score = average confidence score across all reviews."),
    ], columns=["Aspect", "Value", "Notes"])

    sentiment_tiers = pd.DataFrame([
        ("excellent", 5, "excellent value for money, very affordable and worth every cent",  "excellent service, staff are very attentive and friendly", "excellent food, absolutely delicious and outstanding"),
        ("good",      4, "good value for money, reasonably priced",                          "good service, staff are helpful and polite",               "good food, tasty and enjoyable"),
        ("average",   3, "average value for money, neither cheap nor expensive",             "average service, nothing special about the staff",         "average food, neither good nor bad"),
        ("poor",      2, "poor value for money, somewhat overpriced",                        "poor service, staff are slow or unhelpful",                "poor food, disappointing taste"),
        ("terrible",  1, "terrible value for money, extremely overpriced",                   "terrible service, rude or completely inattentive staff",   "terrible food, unpleasant or inedible"),
    ], columns=["Tier", "Score", "Value", "Service", "Taste"])

    return restaurant_cols, affordability_cols, quintile_guide, region_postal, sentiment_meta, sentiment_tiers


# ── Excel: write multiple tables on one sheet ─────────────────────────────────
def _write_definitions_sheet(wb, sections):
    """
    sections: list of (section_title, DataFrame) tuples.
    Each section is written with a styled title, bold header row, then data.
    Two blank rows separate sections.
    """
    TITLE_FILL   = PatternFill("solid", fgColor="1F4E79")
    TITLE_FONT   = Font(bold=True, color="FFFFFF", size=12)
    HEADER_FILL  = PatternFill("solid", fgColor="2E75B6")
    HEADER_FONT  = Font(bold=True, color="FFFFFF", size=10)

    ws = wb.create_sheet("_Definitions")
    current_row = 1

    for title, df in sections:
        # Section title row (full-width merged cell)
        ws.cell(row=current_row, column=1, value=title).font   = TITLE_FONT
        ws.cell(row=current_row, column=1).fill                = TITLE_FILL
        ws.cell(row=current_row, column=1).alignment           = Alignment(wrap_text=True)
        if len(df.columns) > 1:
            ws.merge_cells(start_row=current_row, start_column=1,
                           end_row=current_row,   end_column=len(df.columns))
        current_row += 1

        # Header row
        for col_idx, header in enumerate(df.columns, 1):
            cell = ws.cell(row=current_row, column=col_idx, value=header)
            cell.font  = HEADER_FONT
            cell.fill  = HEADER_FILL
            cell.alignment = Alignment(wrap_text=True)
        current_row += 1

        # Data rows
        for _, data_row in df.iterrows():
            for col_idx, val in enumerate(data_row, 1):
                ws.cell(row=current_row, column=col_idx, value=val).alignment = \
                    Alignment(wrap_text=True, vertical="top")
            current_row += 1

        current_row += 2  # blank gap between sections

    # Auto-size columns (cap at 80 chars).
    # Use getattr to safely skip MergedCell objects which have no .value attribute.
    for col_cells in ws.columns:
        max_len = max(
            (len(str(v)) if (v := getattr(c, "value", None)) else 0)
            for c in col_cells
        )
        col_letter = get_column_letter(col_cells[0].column)
        ws.column_dimensions[col_letter].width = min(max_len + 4, 80)


# ── Step 6: Save outputs ──────────────────────────────────────────────────────
def save_outputs(summary_df, food_df, aff_df, dist_df, tableau_df, quintile_ref_df,
                 restaurant_cols, affordability_cols, quintile_guide,
                 region_postal, sentiment_meta, sentiment_tiers):
    print("\nStep 6: Saving outputs")

    # ── output/ — master files only ───────────────────────────────────────────
    # Remove any stale non-master files left in output/
    stale = [
        "tableau_michelin_affordability.csv", "tableau_michelin_affordability.xlsx",
        "household_expenditure.xlsx",
        "household_income_by_quintile.csv", "household_food_spending_by_quintile.csv",
        "michelin_affordability.csv", "michelin_price_distribution.csv",
    ]
    for fname in stale:
        p = os.path.join(OUTPUT_DIR, fname)
        if os.path.exists(p):
            os.remove(p)

    # household_affordability — the Tableau join table (unique place_id)
    if not tableau_df.empty:
        aff_csv  = os.path.join(OUTPUT_DIR, "household_affordability.csv")
        aff_xlsx = os.path.join(OUTPUT_DIR, "household_affordability.xlsx")
        tableau_df.to_csv(aff_csv,  index=False, encoding="utf-8-sig")
        tableau_df.to_excel(aff_xlsx, index=False, engine="openpyxl")
        print(f"  Saved household_affordability.csv   ({len(tableau_df):,} rows × "
              f"{len(tableau_df.columns)} cols — all restaurants)")
        print(f"  Saved household_affordability.xlsx")

    # master.xlsx — Restaurants | Household_Affordability | Reviews | _Definitions
    restaurants_csv = os.path.join(OUTPUT_DIR, "restaurants.csv")
    reviews_csv     = os.path.join(OUTPUT_DIR, "reviews.csv")
    master_path     = os.path.join(OUTPUT_DIR, "master.xlsx")
    if os.path.exists(restaurants_csv) and not tableau_df.empty:
        rest_df    = pd.read_csv(restaurants_csv, dtype={"Phone Number": str},
                                 encoding="utf-8-sig")
        reviews_df = pd.read_csv(reviews_csv, encoding="utf-8-sig") if os.path.exists(reviews_csv) else pd.DataFrame()
        with pd.ExcelWriter(master_path, engine="openpyxl") as writer:
            rest_df.to_excel(writer,    sheet_name="Restaurants",            index=False)
            tableau_df.to_excel(writer, sheet_name="Household_Affordability", index=False)
            if not reviews_df.empty:
                reviews_df.to_excel(writer, sheet_name="Reviews",            index=False)
            # _Definitions sheet is built separately via openpyxl
            writer.book.create_sheet("_Definitions")   # placeholder, replaced below

        # Re-open with openpyxl to replace placeholder with styled multi-table sheet
        import openpyxl
        wb = openpyxl.load_workbook(master_path)
        if "_Definitions" in wb.sheetnames:
            del wb["_Definitions"]
        sections = [
            ("1. Restaurant Columns",                  restaurant_cols),
            ("2. Household Affordability Columns",     affordability_cols),
            ("3. Q1–Q5 Income Guide",                  quintile_guide),
            ("4. Region by Postal Code",               region_postal),
            ("5. Sentiment Analysis – Model & Method", sentiment_meta),
            ("6. Sentiment Analysis – Tier Labels",    sentiment_tiers),
        ]
        try:
            _write_definitions_sheet(wb, sections)
        except Exception as e:
            print(f"  WARNING: _Definitions sheet failed — {e}")
        wb.save(master_path)
        reviews_note = f" | Reviews: {len(reviews_df):,} rows" if not reviews_df.empty else ""
        print(f"  Saved master.xlsx  "
              f"(Restaurants: {len(rest_df):,} rows | "
              f"Household_Affordability: {len(tableau_df):,} rows (Michelin + Non-Michelin)"
              f"{reviews_note} | + _Definitions)")
        print(f"  → Join on place_id in Tableau")

    # ── BASE_DIR — reference / intermediary files ─────────────────────────────
    # household_expenditure.xlsx (4-sheet context reference)
    hhe_path = os.path.join(BASE_DIR, "household_affordability", "household_expenditure.xlsx")
    with pd.ExcelWriter(hhe_path, engine="openpyxl") as writer:
        summary_df.to_excel(writer,        sheet_name="Income_and_Food_Summary",     index=False)
        food_df.to_excel(writer,           sheet_name="Food_Spending_by_Quintile",    index=False)
        aff_df.to_excel(writer,            sheet_name="Michelin_Affordability",       index=False)
        quintile_ref_df.to_excel(writer,   sheet_name="Income_Quintile_Reference",    index=False)
        if not dist_df.empty:
            dist_df.to_excel(writer,       sheet_name="Michelin_Price_Distribution",  index=False)
    n_sheets = 4 + (0 if dist_df.empty else 1)
    print(f"  Saved household_expenditure.xlsx → base folder ({n_sheets} sheets, "
          f"reference data + quintile range mapping)")

    ref_csvs = {
        "household_income_by_quintile.csv":       summary_df[
            ["Quintile", "Quintile Rank",
             "Monthly Household Income ($)", "Annual Household Income ($)"]],
        "household_food_spending_by_quintile.csv": food_df,
        "michelin_affordability.csv":              aff_df,
        "michelin_price_distribution.csv":         dist_df,
        "income_quintile_reference.csv":           quintile_ref_df,
    }
    for fname, df in ref_csvs.items():
        if df.empty:
            continue
        df.to_csv(os.path.join(BASE_DIR, "household_affordability", fname), index=False, encoding="utf-8-sig")
        print(f"  Saved {fname} → base folder  ({len(df)} rows)")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  Household Expenditure Preprocessor")
    print("  SingStat HES 2023 × Michelin Affordability")
    print("=" * 60)

    if not os.path.exists(SOURCE):
        print(f"ERROR: source file not found:\n  {SOURCE}")
        sys.exit(1)

    xl = pd.ExcelFile(SOURCE)
    print(f"\nLoaded: {os.path.basename(SOURCE)}")

    income_df        = extract_income(xl)
    food_df          = extract_food_spending(xl)
    summary          = build_summary(income_df, food_df)
    dist_df          = extract_michelin_distribution()
    aff_df           = compute_affordability(income_df, food_df)
    tableau_df       = build_tableau_table(income_df, food_df)
    quintile_ref     = build_quintile_reference(income_df, food_df)
    (restaurant_cols, affordability_cols,
     quintile_guide, region_postal,
     sentiment_meta, sentiment_tiers) = build_column_guide(income_df, food_df)
    save_outputs(summary, food_df, aff_df, dist_df, tableau_df, quintile_ref,
                 restaurant_cols, affordability_cols, quintile_guide,
                 region_postal, sentiment_meta, sentiment_tiers)

    print("\nDone.")
