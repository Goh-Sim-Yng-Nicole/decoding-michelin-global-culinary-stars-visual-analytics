import sys, re, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'c:/Users/gohsi/Desktop/data_preprocessing'

mi  = pd.read_csv(f'{BASE}/restaurants/michelin_restaurants.csv',  encoding='utf-8-sig', dtype=str, keep_default_na=False)
nm  = pd.read_csv(f'{BASE}/restaurants/non-michelin_restaurants.csv', encoding='utf-8-sig', dtype=str, keep_default_na=False)
src = pd.read_csv(f'{BASE}/data/michelin_my_maps.csv',  encoding='utf-8-sig', dtype=str, keep_default_na=False)

# ── Michelin source map ───────────────────────────────────────────────────────
MI_SRC_MAP = {
    'Peranakan':              'Peranakan Restaurant',
    'French':                 'French Restaurant',
    'French Contemporary':    'French Restaurant',
    'Sushi':                  'Sushi Restaurant',
    'Italian':                'Italian Restaurant',
    'European Contemporary':  'European Restaurant',
    'British Contemporary':   'European Restaurant',
    'Cantonese':              'Cantonese Restaurant',
    'Teochew, Cantonese':     'Chinese Restaurant',
    'Chinese Contemporary':   'Chinese Restaurant',
    'Ningbo':                 'Chinese Restaurant',
    'Singaporean':            'Singaporean Restaurant',
    'Innovative, Singaporean':'Singaporean Restaurant',
    'Malaysian':              'Malaysian Restaurant',
    'Thai':                   'Thai Restaurant',
    'Spanish':                'Spanish Restaurant',
    'Indian Vegetarian':      'Indian Vegetarian Restaurant',
    'South East Asian':       'Asian Restaurant',
    'Innovative':             'Contemporary Restaurant',
    'International':          'International Restaurant',
    'Contemporary':           'Contemporary Restaurant',
    'Asian Contemporary':     'Asian Restaurant',
    'Meats and Grills':       'Steak House',
}

# ── Keyword → Cuisine (priority order) ───────────────────────────────────────
RULES = [
    ('Japanese Restaurant',    [r'japanese', r'\bramen\b', r'\bsushi\b', r'yakitori', r'izakaya',
                                 r'tempura', r'\budon\b', r'\bsoba\b', r'tonkatsu', r'donburi',
                                 r'okonomiyaki', r'omakase', r'teppanyaki', r'shabu', r'sukiyaki',
                                 r'gyudon', r'teriyaki']),
    ('Italian Restaurant',     [r'italian', r'\bpizza\b', r'\bpasta\b', r'trattoria', r'osteria',
                                 r'ristorante', r'risotto', r'gelato', r'tiramisu', r'pizzeria']),
    ('French Restaurant',      [r'french', r'brasserie', r'\bbistro\b', r'croissant', r'\bcrepe\b',
                                 r'patisserie']),
    ('Korean Restaurant',      [r'korean', r'kimchi', r'bulgogi', r'bibimbap', r'\bkbbq\b',
                                 r'tteok', r'jjigae', r'galbi']),
    ('Vietnamese Restaurant',  [r'vietnamese', r'vietnam', r'\bpho\b', r'banh\s*mi', r'bun\s*cha']),
    ('Indian Restaurant',      [r'indian', r'tandoor', r'biryani', r'briyani', r'\bnaan\b',
                                 r'masala', r'tikka', r'mughal', r'punjab', r'bengali',
                                 r'south\s*indian', r'north\s*indian', r'curry\s*house']),
    ('Peranakan Restaurant',   [r'peranakan', r'nonya', r'nyonya']),
    ('Indonesian Restaurant',  [r'indonesian', r'indonesia', r'nasi\s*padang', r'\bpadang\b',
                                 r'javanese', r'soto\s*ayam', r'ayam\s*penyet']),
    ('Malay Restaurant',       [r'\bmalay\b', r'rendang', r'mee\s*goreng', r'nasi\s*goreng',
                                 r'murtabak', r'tahu\s*goreng']),
    ('Thai Restaurant',        [r'\bthai\b', r'mookata', r'pad\s*thai', r'tom\s*yum', r'som\s*tam']),
    ('Chinese Restaurant',     [r'chinese', r'cantonese', r'teochew', r'peking\s*duck', r'dim\s*sum',
                                 r'zi\s*char', r'cze\s*char', r'szechuan', r'sichuan',
                                 r'chiu\s*chow', r'hakka', r'shanghainese', r'yum\s*cha',
                                 r'hot\s*pot', r'steamboat', r'hong\s*kong\s*style']),
    ('Western Restaurant',     [r'\bwestern\b', r'steakhouse', r'steak\s*house', r'\bburger\b',
                                 r'fish\s*and\s*chips', r'smokehouse', r'rotisserie']),
    ('Seafood Restaurant',     [r'\bseafood\b', r'fish\s*head\s*curry', r'\bcrab\b', r'\blobster\b',
                                 r'oyster\s*bar']),
    ('Vegetarian Restaurant',  [r'\bvegetarian\b', r'\bvegan\b', r'plant.based']),
    ('Cafe',                   [r'\bcafe\b', r'\bcaf[eé]\b', r'bakery', r'bakehouse', r'patisserie']),
    ('Singaporean Restaurant', [r'singaporean', r'singapore\s*cuisine']),
    ('Street Food',            [r'bee\s*hoon', r'bihun', r'kway\s*teow', r'kuay\s*teow',
                                 r'char\s*kway', r'hokkien\s*mee', r'hokkien\s*noodle',
                                 r'fish\s*ball', r'fishball', r'wanton\s*mee', r'wonton\s*mee',
                                 r'wantan\s*mee', r'lor\s*mee', r'mee\s*pok', r'mee\s*kia',
                                 r'hor\s*fun', r'yong\s*tau\s*f', r'chai\s*tow', r'carrot\s*cake',
                                 r'oyster\s*omelette', r'orh\s*luak', r'chee\s*cheong',
                                 r'\brojak\b', r'economic\s*rice', r'economy\s*rice', r'econ\s*rice',
                                 r'mixed\s*rice', r'mix\s*rice', r'mixed\s*veg\s*rice',
                                 r'prawn\s*noodle', r'prawn\s*mee', r'duck\s*rice',
                                 r'braised\s*duck', r'kway\s*chap', r'\blaksa\b', r'mee\s*siam',
                                 r'mee\s*rebus', r'\bporridge\b', r'\bcongee\b',
                                 r'chicken\s*rice\b', r'nasi\s*lemak', r'roti\s*prata',
                                 r'\bprata\b', r'curry\s*puff', r'\bpopiah\b',
                                 r'ngoh\s*hiang', r'ngo\s*hiang',
                                 r'bak\s*k[uio][au]t?\s*teh', r'char\s*siu', r'\bsatay\b',
                                 r'\bsotong\b', r'fried\s*rice', r'noodle\s*soup',
                                 r'won\s*ton\s*noodle', r'bee\s*tai\s*mak',
                                 r'economic\s*bee\s*hoon']),
]

def classify(name, desc=''):
    text = (name + ' ' + desc).lower()
    for cuisine, patterns in RULES:
        if any(re.search(p, text) for p in patterns):
            return cuisine
    return None

# ── 1. Michelin: source cross-reference ──────────────────────────────────────
src_sg = src[src['Location'].str.contains('Singapore', na=False)][['Url','Cuisine']].copy()
src_sg = src_sg.rename(columns={'Url':'Michelin Guide Post Link', 'Cuisine':'SrcCuisine'})
mi_rest = mi[mi['Cuisine']=='Restaurant'].copy()
merged = mi_rest.merge(src_sg, on='Michelin Guide Post Link', how='left')

mi_proposals = {}
for _, row in merged.iterrows():
    src_c = row.get('SrcCuisine','')
    mapped = MI_SRC_MAP.get(src_c)
    if not mapped:
        mapped = classify(row['Restaurant Name'], row['Description'])
    mi_proposals[row['Restaurant Name']] = (src_c, mapped or 'UNRESOLVED')

print(f'=== MICHELIN ({len(mi_proposals)} rows) ===')
for name, (src_c, new_c) in sorted(mi_proposals.items()):
    print(f'  {name:55s} {src_c:30s} -> {new_c}')

# ── 2. Non-Michelin: keyword match ────────────────────────────────────────────
nm_rest = nm[nm['Cuisine']=='Restaurant'].copy()
nm_proposals = {}
unresolved = []
for _, row in nm_rest.iterrows():
    new_c = classify(row['Restaurant Name'], row['Description'])
    nm_proposals[row['Restaurant Name']] = new_c or 'UNRESOLVED'
    if not new_c:
        unresolved.append(row['Restaurant Name'])

resolved   = {k:v for k,v in nm_proposals.items() if v != 'UNRESOLVED'}
print(f'\n=== NON-MICHELIN ({len(nm_proposals)} rows) ===')
print(f'  Resolved:   {len(resolved)}')
print(f'  Unresolved: {len(unresolved)}')
from collections import Counter
print('\nProposed distribution for resolved:')
for cuisine, cnt in Counter(resolved.values()).most_common():
    print(f'  {cuisine:40s} {cnt}')
print(f'\nUnresolved ({len(unresolved)} remain as "Restaurant"):')
for n in unresolved[:30]:
    print(f'  {n}')
if len(unresolved) > 30:
    print(f'  ... and {len(unresolved)-30} more')
