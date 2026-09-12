"""
restaurant_region.py
============================================================
Standalone script to (re-)populate the Region column in
michelin_restaurants.csv from postal codes in the Address field,
using the same postal-code → district → region mapping as the
main preprocessing pipeline.

Also cross-references data/michelin_my_maps.csv to verify that
Cuisine values which should be "Street Food" (hawker stalls) are
flagged where they have been overridden to "Restaurant" by the
Google Places API fetch in preprocess_restaurant_data.py.

Usage:
    python restaurant_region.py
============================================================
"""

import os
import re
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MI_CSV   = os.path.join(BASE_DIR, "restaurants", "michelin_restaurants.csv")
SRC_CSV  = os.path.join(BASE_DIR, "data", "michelin_my_maps.csv")


# ── District / Region maps (matches preprocess_restaurant_data.py) ─────────────
DISTRICT_MAP = {
    '01':'D01','02':'D01','03':'D01','04':'D01','05':'D01','06':'D01',
    '07':'D02','08':'D02',
    '14':'D03','15':'D03','16':'D03',
    '09':'D04','10':'D04',
    '11':'D05','12':'D05','13':'D05',
    '17':'D06',
    '18':'D07','19':'D07',
    '20':'D08','21':'D08',
    '22':'D09','23':'D09',
    '24':'D10','25':'D10','26':'D10','27':'D10',
    '28':'D11','29':'D11','30':'D11',
    '31':'D12','32':'D12','33':'D12',
    '34':'D13','35':'D13','36':'D13','37':'D13',
    '38':'D14','39':'D14','40':'D14','41':'D14',
    '42':'D15','43':'D15','44':'D15','45':'D15',
    '46':'D16','47':'D16','48':'D16',
    '49':'D17','50':'D17','81':'D17',
    '51':'D18','52':'D18',
    '53':'D19','54':'D19','55':'D19','82':'D19',
    '56':'D20','57':'D20',
    '58':'D21','59':'D21',
    '60':'D22','61':'D22','62':'D22','63':'D22','64':'D22',
    '65':'D23','66':'D23','67':'D23','68':'D23',
    '69':'D24','70':'D24','71':'D24',
    '72':'D25','73':'D25',
    '77':'D26','78':'D26',
    '75':'D27','76':'D27',
    '79':'D28','80':'D28',
}

REGION_MAP = {
    'D01':'Central','D02':'Central','D03':'Central','D04':'Central','D05':'Central',
    'D06':'Central','D07':'Central','D08':'Central','D09':'Central','D10':'Central',
    'D11':'Central','D12':'Central','D13':'Central','D14':'Central','D15':'Central',
    'D21':'Central',
    'D16':'East','D17':'East','D18':'East',
    'D19':'North-East','D20':'North-East','D28':'North-East',
    'D25':'North','D26':'North','D27':'North',
    'D22':'West','D23':'West','D24':'West',
}


# ── Helpers ────────────────────────────────────────────────────────────────────
def _postal_to_region(postal: str) -> str:
    return REGION_MAP.get(DISTRICT_MAP.get(str(postal)[:2], ''), '')


def get_region_from_address(address) -> str:
    if not isinstance(address, str):
        return ''
    m = re.search(r'\b(\d{6})\b', address)
    return _postal_to_region(m.group(1)) if m else ''


def get_region_from_latlon(lat: float, lon: float) -> str:
    """Lat/lon bounding-box fallback (no API call required)."""
    if not (1.20 <= lat <= 1.47 and 103.62 <= lon <= 104.05):
        return ''
    if lon < 103.78:                             return 'West'
    if lat > 1.41:                               return 'North'
    if lat > 1.34 and 103.84 < lon < 103.93:    return 'North-East'
    if lon > 103.90:                             return 'East'
    return 'Central'


def assign_region(address, lat, lon) -> str:
    region = get_region_from_address(address)
    if region:
        return region
    try:
        return get_region_from_latlon(float(lat), float(lon))
    except (TypeError, ValueError):
        return ''


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    # 1. Load michelin_restaurants.csv
    df = pd.read_csv(MI_CSV, encoding='utf-8-sig', dtype=str, keep_default_na=False)
    print(f"Loaded {len(df)} rows from {MI_CSV}")

    # 2. Compute Region
    df['Region'] = df.apply(
        lambda r: assign_region(r['Address'], r.get('Latitude', ''), r.get('Longitude', '')),
        axis=1,
    )

    # 3. Ensure Region column sits immediately after Country
    cols = list(df.columns)
    if 'Region' in cols:
        cols.remove('Region')
    cols.insert(cols.index('Country') + 1, 'Region')
    df = df[cols]

    print(f"\nRegion distribution:\n{df['Region'].replace('', float('nan')).value_counts(dropna=False).to_string()}")
    blank = df['Region'].eq('').sum()
    if blank:
        print(f"\n  WARNING: {blank} row(s) could not be assigned a region.")

    # 4. Save
    df.to_csv(MI_CSV, index=False, encoding='utf-8-sig')
    print(f"\nSaved → {MI_CSV}")

    # ── Cuisine double-check ────────────────────────────────────────────────
    # The preprocessing pipeline fetches Cuisine from Google Places API,
    # which often returns "Restaurant" for hawker stalls.  The Michelin
    # source data (michelin_my_maps.csv) uses "Street Food" for those stalls.
    # Note: "Local Delights" does NOT appear in the source data — if you see
    # this value it has been added manually or via another source.
    print("\n── Cuisine double-check ────────────────────────────────────────")
    if not os.path.exists(SRC_CSV):
        print(f"  Source file not found: {SRC_CSV}  (skipping check)")
        return

    src = pd.read_csv(SRC_CSV, encoding='utf-8-sig', dtype=str, keep_default_na=False)
    # Keep only Singapore entries that are "Street Food" in the source
    src_sg = src[
        src['Location'].str.contains('Singapore', na=False) &
        src['Cuisine'].str.strip().eq('Street Food')
    ][['Name', 'Cuisine']].rename(columns={'Name': 'Restaurant Name', 'Cuisine': 'Source Cuisine'})

    merged = df[['Restaurant Name', 'Cuisine']].merge(src_sg, on='Restaurant Name', how='inner')

    mismatched = merged[merged['Cuisine'] != merged['Source Cuisine']]
    if mismatched.empty:
        print("  All 'Street Food' restaurants in the source match the processed CSV.")
    else:
        print(f"  {len(mismatched)} restaurant(s) have Cuisine overridden from 'Street Food' → '{mismatched['Cuisine'].unique().tolist()}':")
        for _, row in mismatched.iterrows():
            print(f"    • {row['Restaurant Name']:50s}  source='{row['Source Cuisine']}'  csv='{row['Cuisine']}'")
        print("\n  To restore the original Michelin cuisine labels, re-run the")
        print("  preprocess pipeline and skip Step 2 (Places API cuisine fetch),")
        print("  or manually update the Cuisine column for these rows.")


if __name__ == '__main__':
    main()
