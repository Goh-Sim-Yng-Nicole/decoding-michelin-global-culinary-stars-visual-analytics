"""
preprocess_restaurant_data.py
=============================================================
Full preprocessing pipeline for restaurant data.

NON-MICHELIN pipeline  (non-michelin_restaurant_(Original).csv → non-michelin_restaurants.csv)
  Step 1  : Load original CSV
  Step 2  : Remove rows with empty rating or review_count
  Step 3  : Drop unused columns (is_michelin, avg_sentiment, total_reviews)
  Step 4  : Fetch Address from Google Places API (formattedAddress)
  Step 5  : Add Country = "Singapore"
  Step 6  : Fetch price_level from Google Places API (priceLevel)
  Step 7  : Remove rows still missing price_level
  Step 8  : Remove rows missing address
  Step 9  : Format restaurant name  (title-case + @ / - location in brackets)
  Step 10 : Restructure columns to target schema
  Step 11 : Populate fixed values (Michelin Guide Post Link, Michelin Award, Safety Penalty)
  Step 12 : Fetch Cuisine, Phone, Google Maps URL, Facilities & Services, Description  (Places API)
  Step 13 : Map Region from postal code  → district → region
  Step 14 : Remove Malaysia restaurants
  Step 15 : Sort A-Z by Restaurant Name
  Step 16 : Clean restaurant names (encoding, CJK, unit#, @, Pte Ltd)
  Step 17 : Fill blank Phone Numbers with "No Phone Number Listed"
  Step 18 : Save as UTF-8 with BOM  (utf-8-sig)

MICHELIN pipeline  (data/michelin_my_maps.csv → michelin_restaurants.csv)
  Step 0  : Bootstrap from SOURCE_MI_CSV if michelin_restaurants.csv is missing
              (maps Name/Address/Price/Award/Cuisine/Description/etc. from source;
               place_id column left blank — fill via a separate Places lookup step)
  Step 1  : Load CSV
  Step 2  : Fetch / refresh Cuisine and Facilities & Services  (Places API)
  Step 3  : Fetch / fill Phone Numbers  (Places API)
  Step 4  : Clean phone format  (strip country code → 8-digit  XXXX XXXX)
  Step 5  : Map Region from postal code
  Step 6  : Clean restaurant names (encoding, CJK, unit#)
  Step 7  : Fill blank Phone Numbers with "No Phone Number Listed"
  Step 8  : Save as UTF-8 with BOM  (utf-8-sig)

Progress files are saved after every batch of API calls so the script
can be safely interrupted and resumed without re-fetching completed rows.

COMBINE step  (runs after both pipelines)
  Merges michelin_restaurants.csv + non-michelin_restaurants.csv into
  output/restaurants.csv and output/restaurants.xlsx.
=============================================================
"""

import json
import os
import re
import sys
import time
import urllib.error
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

# ── Configuration ─────────────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
API_KEY         = os.environ.get('GOOGLE_PLACES_API_KEY', '')

ORIGINAL_CSV    = f"{BASE_DIR}/non-michelin_restaurant_(Original).csv"
NM_OUT          = f"{BASE_DIR}/restaurants/non-michelin_restaurants.csv"
MI_CSV          = f"{BASE_DIR}/restaurants/michelin_restaurants.csv"
SOURCE_MI_CSV   = os.path.join(BASE_DIR, "data", "michelin_my_maps.csv")

# Progress files  (allow resuming without re-hitting the API)
ADDR_PROG       = f"{BASE_DIR}/pp_address_progress.json"
PRICE_PROG      = f"{BASE_DIR}/pp_price_progress.json"
DETAILS_PROG    = f"{BASE_DIR}/pp_details_progress.json"
MI_DETAILS_PROG = f"{BASE_DIR}/pp_mi_details_progress.json"
MI_PLACEID_PROG = f"{BASE_DIR}/pp_mi_placeid_progress.json"

SAVE_EVERY      = 50       # checkpoint every N API calls
API_DELAY       = 0.05     # seconds between requests (~20 req/s)


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════

# ── Progress file helpers ─────────────────────────────────────────────────────
def load_progress(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_progress(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


# ── Google Places API v1 ──────────────────────────────────────────────────────
def _places_request(place_id, field_mask):
    url = f"https://places.googleapis.com/v1/places/{place_id}"
    req = urllib.request.Request(url, headers={
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': field_mask,
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {'_error': e.code}
    except Exception as e:
        return {'_error': str(e)}


def fetch_address(place_id):
    """Return formatted address string from Places API."""
    data = _places_request(place_id, 'formattedAddress')
    addr = data.get('formattedAddress', '')
    # Strip trailing ", Singapore" if present (we add Country separately)
    addr = re.sub(r',?\s*Singapore\s*$', '', addr).strip()
    return addr


def fetch_price_level(place_id):
    """Return price level 1-4 (None if unavailable)."""
    data = _places_request(place_id, 'priceLevel')
    level_map = {
        'PRICE_LEVEL_INEXPENSIVE': 1.0,
        'PRICE_LEVEL_MODERATE':    2.0,
        'PRICE_LEVEL_EXPENSIVE':   3.0,
        'PRICE_LEVEL_VERY_EXPENSIVE': 4.0,
    }
    raw = data.get('priceLevel', '')
    return level_map.get(raw)


def fetch_details(place_id):
    """Fetch cuisine, phone, maps URL, facilities, description in one call."""
    field_mask = ','.join([
        'primaryTypeDisplayName', 'types',
        'nationalPhoneNumber',
        'websiteUri', 'googleMapsUri',
        'editorialSummary',
        'dineIn', 'delivery', 'takeout', 'reservable',
        'outdoorSeating', 'liveMusic',
        'servesBeer', 'servesWine', 'servesCocktails', 'servesCoffee',
        'paymentOptions', 'accessibilityOptions',
    ])
    data = _places_request(place_id, field_mask)

    result = {
        'Cuisine': '', 'Phone Number': '', 'Google Website Link': '',
        'Facilities And Services': '', 'Description': '',
    }
    if '_error' in data:
        return result

    # Cuisine
    ptdn = data.get('primaryTypeDisplayName', {})
    result['Cuisine'] = ptdn.get('text', '') if ptdn else ''
    if not result['Cuisine']:
        skip = {'point_of_interest', 'establishment', 'food', 'store'}
        for t in data.get('types', []):
            if t not in skip:
                result['Cuisine'] = t.replace('_', ' ').title()
                break

    # Phone
    result['Phone Number'] = data.get('nationalPhoneNumber', '')

    # Google Maps URL (strip internal tracking param)
    gmap = data.get('googleMapsUri', '')
    if '&g_mp=' in gmap:
        gmap = gmap[:gmap.index('&g_mp=')]
    result['Google Website Link'] = gmap or data.get('websiteUri', '')

    # Description
    ed = data.get('editorialSummary', {})
    result['Description'] = ed.get('text', '') if ed else ''

    # Facilities
    fac = []
    if data.get('dineIn'):          fac.append('Dine-in')
    if data.get('takeout'):         fac.append('Takeaway')
    if data.get('delivery'):        fac.append('Delivery')
    if data.get('reservable'):      fac.append('Reservations')
    if data.get('outdoorSeating'):  fac.append('Outdoor seating')
    if data.get('liveMusic'):       fac.append('Live music')
    if data.get('servesBeer'):      fac.append('Beer')
    if data.get('servesWine'):      fac.append('Wine')
    if data.get('servesCocktails'): fac.append('Cocktails')
    if data.get('servesCoffee'):    fac.append('Coffee')
    pay = data.get('paymentOptions', {})
    if pay:
        if pay.get('acceptsCashOnly'):       fac.append('Cash only')
        elif pay.get('acceptsCreditCards'):  fac.append('Credit cards')
        if pay.get('acceptsNfc'):            fac.append('NFC payments')
    acc = data.get('accessibilityOptions', {})
    if acc and acc.get('wheelchairAccessibleEntrance'):
        fac.append('Wheelchair accessible')
    result['Facilities And Services'] = ','.join(fac)

    return result


# ── Region mapping ────────────────────────────────────────────────────────────
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

def _postal_to_region(postal):
    return REGION_MAP.get(DISTRICT_MAP.get(str(postal)[:2], ''), '')

def get_region_from_address(address):
    if not isinstance(address, str):
        return ''
    m = re.search(r'\b(\d{6})\b', address)
    return _postal_to_region(m.group(1)) if m else ''

def get_region_from_latlon(lat, lon):
    """Fallback region from lat/lon bounding boxes."""
    if not (1.20 <= lat <= 1.47 and 103.62 <= lon <= 104.05):
        return ''
    if lon < 103.78:                                    return 'West'
    if lat > 1.41:                                      return 'North'
    if lat > 1.34 and 103.84 < lon < 103.93:            return 'North-East'
    if lon > 103.90:                                    return 'East'
    return 'Central'

def get_region_via_geocode(lat, lon):
    """Reverse-geocode lat/lon via Google to get postal code → region."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={API_KEY}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
        for result in data.get('results', []):
            for comp in result.get('address_components', []):
                if 'postal_code' in comp.get('types', []):
                    postal = comp['long_name']
                    if len(postal) == 6:
                        return _postal_to_region(postal)
    except Exception:
        pass
    return ''

def assign_region(address, lat, lon):
    region = get_region_from_address(address)
    if region:
        return region
    region = get_region_via_geocode(lat, lon)
    if region:
        return region
    return get_region_from_latlon(lat, lon)


# ── Malaysia detection ────────────────────────────────────────────────────────
def is_malaysia(address, lon):
    if lon < 103.62:
        return True
    if not isinstance(address, str):
        return False
    addr_lower = address.lower()
    if any(kw in addr_lower for kw in [
        'malaysia', 'johor', 'iskandar', 'gelang patah',
        'puteri harbour', 'medini', 'darul ta',
    ]):
        return True
    m = re.search(r'\bSingapore\s+(\d{5})\b', address)
    if m and m.group(1)[:2] in {'79', '80', '81', '82'}:
        return True
    if re.search(r'\b(79|80|81|82)\d{3}\b', address) and not re.search(r'\b\d{6}\b', address):
        return True
    return False


# ── Restaurant name formatting ────────────────────────────────────────────────
def _title_case(s):
    """Title-case that handles apostrophes correctly."""
    s = s.lower()
    return re.sub(r"(?:^|(?<=[^a-zA-Z']))([a-z])", lambda m: m.group().upper(), s)

def format_restaurant_name(name):
    """Apply title-case and move @ / - location suffix into brackets."""
    if not isinstance(name, str):
        return name
    name = name.strip()
    if '@' in name:
        at_idx = name.rfind('@')
        name_part = name[:at_idx].strip().rstrip('-').strip()
        loc_part  = name[at_idx + 1:].strip()
        formatted = f"{name_part} (@{loc_part})" if loc_part else name_part
    elif ' - ' in name:
        dash_idx  = name.index(' - ')
        name_part = name[:dash_idx].strip()
        loc_part  = name[dash_idx + 3:].strip()
        formatted = f"{name_part} ({loc_part})" if loc_part else name_part
    else:
        formatted = name
    return _title_case(formatted)


# ── Restaurant name cleaning ──────────────────────────────────────────────────
def fix_encoding(text):
    """Fix mojibake: UTF-8 bytes incorrectly decoded as Latin-1."""
    if not isinstance(text, str):
        return text
    try:
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        try:
            return text.encode('latin-1', errors='ignore').decode('utf-8', errors='ignore')
        except Exception:
            return text

def clean_name(name):
    """Fix encoding, remove CJK, unit numbers, @, Pte Ltd, tidy whitespace."""
    if not isinstance(name, str):
        return name
    original = name
    name = fix_encoding(name)
    # Remove CJK characters
    name = re.sub(
        r'[\u2E80-\u2EFF\u3000-\u303F\u3040-\u30FF'
        r'\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF'
        r'\uFF00-\uFFEF\U00020000-\U0002A6DF]',
        '', name,
    )
    # Remove unit numbers  e.g. #01-11, #B2-03
    name = re.sub(r'#[A-Za-z]?\d+[A-Za-z]?-\d+[A-Za-z]?\s*', '', name)
    # Remove @ symbol
    name = name.replace('@', '')
    # Remove Pte Ltd / Pte. Ltd. variants
    name = re.sub(r'\(?\bPte\.?\s*Ltd\.?\)?', '', name, flags=re.IGNORECASE)
    # Remove empty brackets
    name = re.sub(r'\(\s*\)', '', name)
    # Strip and collapse whitespace
    name = re.sub(r'^[\s.·•,\-]+', '', name)
    name = re.sub(r'[\s.·•]+$', '', name)
    name = re.sub(r'\s{2,}', ' ', name)
    return name.strip() or original


# ── Phone number helpers ──────────────────────────────────────────────────────
def clean_phone(value):
    """Strip country code, format as XXXX XXXX (8 digits) or blank."""
    if pd.isna(value) or str(value).strip() in ('', 'nan'):
        return ''
    digits = re.sub(r'[\s\+\-]', '', str(value))
    if len(digits) == 10 and digits.startswith('65'):
        digits = digits[2:]
    if len(digits) == 8 and digits[0] in '36789':
        return digits[:4] + ' ' + digits[4:]
    return ''

def fill_phone(series):
    """Replace blank / invalid phones with placeholder."""
    blank = series.isna() | series.astype(str).str.strip().isin(['', 'nan', 'No Phone Number Listed'])
    result = series.copy()
    result[blank] = 'No Phone Number Listed'
    return result


# ══════════════════════════════════════════════════════════════════════════════
#  NON-MICHELIN PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
def run_non_michelin():
    print("\n" + "="*60)
    print("NON-MICHELIN PIPELINE")
    print("="*60)

    # ── Step 1: Load original ─────────────────────────────────────────────────
    print("\nStep 1: Load original CSV")
    df = pd.read_csv(ORIGINAL_CSV, encoding='utf-8')
    print(f"  Loaded {len(df)} rows, columns: {list(df.columns)}")

    # ── Step 2: Remove rows with empty rating / review_count ──────────────────
    print("\nStep 2: Remove rows with empty rating or review_count")
    df = df.dropna(subset=['rating', 'review_count']).reset_index(drop=True)
    print(f"  Remaining: {len(df)} rows")

    # ── Step 3: Drop unused columns ───────────────────────────────────────────
    print("\nStep 3: Drop unused columns (is_michelin, avg_sentiment, total_reviews)")
    for col in ['is_michelin', 'avg_sentiment', 'total_reviews']:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    # ── Step 4: Fetch addresses from Places API ───────────────────────────────
    print("\nStep 4: Fetch addresses from Google Places API")
    addr_prog = load_progress(ADDR_PROG)
    missing   = [pid for pid in df['place_id'] if pid not in addr_prog]
    print(f"  Already have: {len(addr_prog)}, to fetch: {len(missing)}")
    for i, pid in enumerate(missing):
        addr_prog[pid] = fetch_address(pid)
        if (i + 1) % SAVE_EVERY == 0:
            save_progress(addr_prog, ADDR_PROG)
            print(f"    [{i+1}/{len(missing)}] saved checkpoint")
        time.sleep(API_DELAY)
    save_progress(addr_prog, ADDR_PROG)
    df['Address'] = df['place_id'].map(addr_prog).fillna('')
    print(f"  Addresses filled: {(df['Address'] != '').sum()}/{len(df)}")

    # ── Step 5: Add Country ───────────────────────────────────────────────────
    print("\nStep 5: Add Country = 'Singapore'")
    df['Country'] = 'Singapore'

    # ── Step 6: Fill price_level from Places API ──────────────────────────────
    print("\nStep 6: Fetch price_level from Google Places API")
    price_prog = load_progress(PRICE_PROG)
    missing    = [pid for pid in df['place_id']
                  if pid not in price_prog
                  and (pd.isna(df.loc[df['place_id'] == pid, 'price_level']).all()
                       or str(df.loc[df['place_id'] == pid, 'price_level'].values[0]).strip() in ('', 'nan'))]
    print(f"  Already have: {len(price_prog)}, to fetch: {len(missing)}")
    for i, pid in enumerate(missing):
        price_prog[pid] = fetch_price_level(pid)
        if (i + 1) % SAVE_EVERY == 0:
            save_progress(price_prog, PRICE_PROG)
            print(f"    [{i+1}/{len(missing)}] saved checkpoint")
        time.sleep(API_DELAY)
    save_progress(price_prog, PRICE_PROG)

    def resolve_price(row):
        existing = row['price_level']
        if pd.notna(existing) and str(existing).strip() not in ('', 'nan'):
            return float(existing)
        fetched = price_prog.get(row['place_id'])
        return float(fetched) if fetched is not None else None

    df['price_level'] = df.apply(resolve_price, axis=1)
    print(f"  Rows with price_level: {df['price_level'].notna().sum()}/{len(df)}")

    # ── Step 7: Remove rows missing price_level ───────────────────────────────
    print("\nStep 7: Remove rows with no price_level")
    df = df.dropna(subset=['price_level']).reset_index(drop=True)
    print(f"  Remaining: {len(df)} rows")

    # ── Step 8: Remove rows missing address ───────────────────────────────────
    print("\nStep 8: Remove rows with no address")
    df = df[df['Address'].str.strip() != ''].reset_index(drop=True)
    print(f"  Remaining: {len(df)} rows")

    # ── Step 9: Format restaurant name ───────────────────────────────────────
    print("\nStep 9: Format restaurant name (title-case + location brackets)")
    df['restaurant_name'] = df['restaurant_name'].apply(format_restaurant_name)

    # ── Step 10: Restructure columns ──────────────────────────────────────────
    print("\nStep 10: Restructure to target column schema")
    df = df.rename(columns={
        'restaurant_name': 'Restaurant Name',
        'price_level':     'Price',
        'hygiene_grade':   'SFA Hygiene Grade',
        'michelin_award':  'Michelin Award',
    })
    df['Cuisine']                = ''
    df['Phone Number']           = ''
    df['Michelin Guide Post Link'] = 'Not in Michelin Guide Yet'
    df['Google Website Link']    = ''
    df['Facilities And Services'] = ''
    df['Description']            = ''

    target_cols = [
        'place_id', 'Restaurant Name', 'Address', 'Country',
        'Price', 'Cuisine', 'Longitude', 'Latitude',
        'Phone Number', 'Michelin Guide Post Link', 'Google Website Link',
        'Michelin Award', 'Facilities And Services', 'Description',
        'SFA Hygiene Grade', 'matched_sfa_name',
    ]
    target_cols = [c for c in target_cols if c in df.columns]
    df = df[target_cols]

    # ── Step 11: Populate fixed values ────────────────────────────────────────
    print("\nStep 11: Populate fixed values")
    df['Michelin Award'] = df['Michelin Award'].fillna('Not Awarded Any Yet')
    df['Michelin Award'] = df['Michelin Award'].replace('', 'Not Awarded Any Yet')

    penalty_map = {'A': 0, 'B': 1, 'C': 2, 'D': 4}
    df['Safety Penalty'] = df['SFA Hygiene Grade'].map(penalty_map)

    # ── Step 12: Fetch Cuisine, Phone, Maps URL, Facilities, Description ───────
    print("\nStep 12: Fetch details from Google Places API")
    det_prog = load_progress(DETAILS_PROG)
    missing  = [pid for pid in df['place_id'] if pid not in det_prog]
    print(f"  Already have: {len(det_prog)}, to fetch: {len(missing)}")
    for i, pid in enumerate(missing):
        det_prog[pid] = fetch_details(pid)
        if (i + 1) % SAVE_EVERY == 0:
            save_progress(det_prog, DETAILS_PROG)
            pct = (len(det_prog) / len(df['place_id'].unique())) * 100
            print(f"    [{i+1}/{len(missing)}] {pct:.1f}% done — saved checkpoint")
        time.sleep(API_DELAY)
    save_progress(det_prog, DETAILS_PROG)

    for col in ['Cuisine', 'Phone Number', 'Google Website Link',
                'Facilities And Services', 'Description']:
        df[col] = df['place_id'].map(
            lambda pid, c=col: det_prog.get(pid, {}).get(c, '')
        )

    # ── Step 13: Add Region column ────────────────────────────────────────────
    print("\nStep 13: Map Region from postal code / geocode / lat-lon")
    df['Region'] = df.apply(
        lambda r: assign_region(r['Address'], r['Latitude'], r['Longitude']), axis=1
    )
    # Insert Region after Country
    cols = list(df.columns)
    cols.remove('Region')
    cols.insert(cols.index('Country') + 1, 'Region')
    df = df[cols]
    print(f"  Region distribution:\n{df['Region'].replace('', float('nan')).value_counts(dropna=False).to_string()}")

    # ── Step 14: Remove Malaysia restaurants ──────────────────────────────────
    print("\nStep 14: Remove Malaysia restaurants")
    before = len(df)
    df = df[~df.apply(lambda r: is_malaysia(r['Address'], r['Longitude']), axis=1)]
    df = df[df['Region'].replace('', float('nan')).notna()].reset_index(drop=True)
    print(f"  Removed {before - len(df)} rows → {len(df)} remaining")

    # ── Step 15: Sort A-Z ─────────────────────────────────────────────────────
    print("\nStep 15: Sort A-Z by Restaurant Name")
    df = df.sort_values('Restaurant Name', key=lambda s: s.str.lower()).reset_index(drop=True)

    # ── Step 16: Clean restaurant names ──────────────────────────────────────
    print("\nStep 16: Clean restaurant names")
    df['Restaurant Name'] = df['Restaurant Name'].apply(clean_name)

    # ── Step 17: Fill blank phones ────────────────────────────────────────────
    print("\nStep 17: Fill blank Phone Numbers")
    df['Phone Number'] = fill_phone(df['Phone Number'].astype(str))
    blank_filled = (df['Phone Number'] == 'No Phone Number Listed').sum()
    print(f"  Filled {blank_filled} blank phones")

    # ── Step 18: Save ─────────────────────────────────────────────────────────
    print(f"\nStep 18: Save → {NM_OUT}")
    df.to_csv(NM_OUT, index=False, encoding='utf-8-sig')
    print(f"  Saved {len(df)} rows, {len(df.columns)} columns")
    print(f"  Columns: {list(df.columns)}")


# ══════════════════════════════════════════════════════════════════════════════
#  MICHELIN PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
def run_michelin():
    print("\n" + "="*60)
    print("MICHELIN PIPELINE")
    print("="*60)

    # ── Step 0: Bootstrap from source if target CSV is absent ─────────────────
    if not os.path.exists(MI_CSV):
        print("\nStep 0: michelin_restaurants.csv not found — bootstrapping from source")
        if not os.path.exists(SOURCE_MI_CSV):
            raise FileNotFoundError(
                f"Source not found: {SOURCE_MI_CSV}\n"
                "Place michelin_my_maps.csv in the data/ folder and retry."
            )
        src = pd.read_csv(SOURCE_MI_CSV, encoding='utf-8')
        sg  = src[src['Location'] == 'Singapore'].copy().reset_index(drop=True)
        print(f"  Source rows (Singapore): {len(sg)}")

        price_map = {'$': 1, '$$': 2, '$$$': 3, '$$$$': 4}

        def _fmt_phone(val):
            if pd.isna(val):
                return ''
            digits = str(int(val))
            if digits.startswith('65') and len(digits) == 10:
                digits = digits[2:]
            if len(digits) == 8 and digits[0] in '36789':
                return digits[:4] + ' ' + digits[4:]
            return ''

        df0 = pd.DataFrame({
            'place_id':               '',
            'Restaurant Name':        sg['Name'].str.strip(),
            'Address':                sg['Address'].str.replace(
                                          r',?\s*Singapore\s*$', '', regex=True
                                      ).str.strip(),
            'Country':                'Singapore',
            'Region':                 '',
            'Price':                  sg['Price'].map(price_map),
            'Cuisine':                sg['Cuisine'].fillna(''),
            'Longitude':              sg['Longitude'],
            'Latitude':               sg['Latitude'],
            'Phone Number':           sg['PhoneNumber'].apply(_fmt_phone),
            'Michelin Guide Post Link': sg['Url'].fillna(''),
            'Google Website Link':    sg['WebsiteUrl'].fillna(''),
            'Michelin Award':         sg['Award'].fillna(''),
            'Facilities And Services': sg['FacilitiesAndServices'].fillna(''),
            'Description':            sg['Description'].fillna(''),
            'SFA Hygiene Grade':      'A',
            'Safety Penalty':         0,
        })
        df0.to_csv(MI_CSV, index=False, encoding='utf-8-sig')
        print(f"  Bootstrap saved: {len(df0)} rows → {os.path.basename(MI_CSV)}")
        print("  NOTE: place_id column is empty — run a Places API lookup to fill it "
              "before Steps 2-3 can enrich data.")

    # ── Step 1: Load ──────────────────────────────────────────────────────────
    print("\nStep 1: Load michelin_restaurants.csv")
    df = pd.read_csv(MI_CSV, dtype={'Phone Number': str})
    print(f"  Loaded {len(df)} rows")

    # ── Step 2: Refresh Cuisine and Facilities from Places API ────────────────
    print("\nStep 2: Fetch / refresh Cuisine and Facilities & Services")
    field_mask_cf = ','.join([
        'primaryTypeDisplayName', 'types',
        'dineIn', 'delivery', 'takeout', 'reservable',
        'outdoorSeating', 'liveMusic',
        'servesBeer', 'servesWine', 'servesCocktails', 'servesCoffee',
        'paymentOptions', 'accessibilityOptions',
    ])
    mi_prog = load_progress(MI_DETAILS_PROG)
    missing = [pid for pid in df['place_id'] if pid not in mi_prog]
    print(f"  Already have: {len(mi_prog)}, to fetch: {len(missing)}")
    for i, pid in enumerate(missing):
        mi_prog[pid] = _places_request(pid, field_mask_cf)
        if (i + 1) % SAVE_EVERY == 0:
            save_progress(mi_prog, MI_DETAILS_PROG)
        time.sleep(API_DELAY)
    save_progress(mi_prog, MI_DETAILS_PROG)

    def parse_cuisine(data):
        ptdn = data.get('primaryTypeDisplayName', {})
        c = ptdn.get('text', '') if ptdn else ''
        if not c:
            skip = {'point_of_interest', 'establishment', 'food', 'store'}
            for t in data.get('types', []):
                if t not in skip:
                    return t.replace('_', ' ').title()
        return c

    def parse_facilities(data):
        fac = []
        if data.get('dineIn'):          fac.append('Dine-in')
        if data.get('takeout'):         fac.append('Takeaway')
        if data.get('delivery'):        fac.append('Delivery')
        if data.get('reservable'):      fac.append('Reservations')
        if data.get('outdoorSeating'):  fac.append('Outdoor seating')
        if data.get('liveMusic'):       fac.append('Live music')
        if data.get('servesBeer'):      fac.append('Beer')
        if data.get('servesWine'):      fac.append('Wine')
        if data.get('servesCocktails'): fac.append('Cocktails')
        if data.get('servesCoffee'):    fac.append('Coffee')
        pay = data.get('paymentOptions', {})
        if pay:
            if pay.get('acceptsCashOnly'):       fac.append('Cash only')
            elif pay.get('acceptsCreditCards'):  fac.append('Credit cards')
            if pay.get('acceptsNfc'):            fac.append('NFC payments')
        acc = data.get('accessibilityOptions', {})
        if acc and acc.get('wheelchairAccessibleEntrance'):
            fac.append('Wheelchair accessible')
        return ','.join(fac)

    for idx, row in df.iterrows():
        data = mi_prog.get(row['place_id'], {})
        df.at[idx, 'Cuisine']                = parse_cuisine(data)
        df.at[idx, 'Facilities And Services'] = parse_facilities(data)

    # ── Step 3: Fetch phone numbers ───────────────────────────────────────────
    print("\nStep 3: Fetch missing phone numbers")
    blank_mask = df['Phone Number'].isna() | df['Phone Number'].str.strip().isin(['', 'nan', 'No Phone Number Listed'])
    print(f"  Blank phones: {blank_mask.sum()}")
    for idx, row in df[blank_mask].iterrows():
        data = _places_request(row['place_id'], 'nationalPhoneNumber')
        df.at[idx, 'Phone Number'] = data.get('nationalPhoneNumber', '')
        time.sleep(API_DELAY)

    # ── Step 4: Clean phone format ────────────────────────────────────────────
    print("\nStep 4: Clean phone format → 8-digit XXXX XXXX")
    df['Phone Number'] = df['Phone Number'].apply(clean_phone)

    # ── Step 5: Add / refresh Region ──────────────────────────────────────────
    print("\nStep 5: Map Region from postal code")
    df['Region'] = df['Address'].apply(get_region_from_address)
    if 'Region' not in df.columns or df.columns.tolist().index('Region') != df.columns.tolist().index('Country') + 1:
        cols = list(df.columns)
        if 'Region' in cols:
            cols.remove('Region')
        cols.insert(cols.index('Country') + 1, 'Region')
        df = df[cols]
    print(f"  {df['Region'].value_counts().to_string()}")

    # ── Step 6: Clean restaurant names ───────────────────────────────────────
    print("\nStep 6: Clean restaurant names")
    df['Restaurant Name'] = df['Restaurant Name'].apply(clean_name)

    # ── Step 7: Fill blank phones ─────────────────────────────────────────────
    print("\nStep 7: Fill blank Phone Numbers")
    df['Phone Number'] = fill_phone(df['Phone Number'].astype(str))

    # ── Step 8: Save ──────────────────────────────────────────────────────────
    print(f"\nStep 8: Save → {MI_CSV}")
    df.to_csv(MI_CSV, index=False, encoding='utf-8-sig')
    print(f"  Saved {len(df)} rows, {len(df.columns)} columns")


# ══════════════════════════════════════════════════════════════════════════════
#  COMBINE: merge both datasets into output/
# ══════════════════════════════════════════════════════════════════════════════
def rebuild_output():
    print("\n" + "="*60)
    print("COMBINE: Rebuilding output/restaurants.csv + .xlsx")
    print("="*60)
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    mi = pd.read_csv(MI_CSV,  dtype={'Phone Number': str}, encoding='utf-8-sig')
    nm = pd.read_csv(NM_OUT,  dtype={'Phone Number': str}, encoding='utf-8-sig')
    mi['Is Michelin'] = True
    nm['Is Michelin'] = False
    master = pd.concat([mi, nm], ignore_index=True)

    # Fill empty descriptions
    mask = master['Description'].isna() | (master['Description'].str.strip() == '')
    master.loc[mask, 'Description'] = 'No Description Available Yet'

    out_csv  = os.path.join(OUTPUT_DIR, "restaurants.csv")
    out_xlsx = os.path.join(OUTPUT_DIR, "restaurants.xlsx")
    master.to_csv(out_csv,  index=False, encoding='utf-8-sig')
    master.to_excel(out_xlsx, index=False, engine='openpyxl')
    print(f"  Saved {len(master)} rows ({len(mi)} Michelin + {len(nm)} Non-Michelin)")
    print(f"  → {out_csv}")
    print(f"  → {out_xlsx}")


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    run_non_michelin()
    run_michelin()
    rebuild_output()
    print("\n✓ All pipelines complete.")
