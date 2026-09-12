import sys, shutil, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

# ── Load master (source of truth for place_id and canonical names) ─────────
master = pd.read_csv('output/restaurants.csv', encoding='utf-8-sig', dtype=str, keep_default_na=False)
id_map = master.set_index('Restaurant Name')[['place_id', 'Is Michelin']].to_dict('index')

def enrich(df, name_col):
    """Add place_id + Is Michelin from master; drop rows with no match."""
    df = df.copy()
    df[name_col] = df[name_col].str.strip()
    # Map place_id and Is Michelin
    df['place_id']   = df[name_col].map(lambda n: id_map.get(n, {}).get('place_id', ''))
    df['Is Michelin'] = df[name_col].map(lambda n: id_map.get(n, {}).get('Is Michelin', ''))
    before = len(df)
    dropped = df[df['place_id'] == '']['Restaurant Name'].unique().tolist()
    df = df[df['place_id'] != ''].reset_index(drop=True)
    if dropped:
        print(f'  Dropped {before - len(df)} rows (no master match): {dropped}')
    return df

# ── michelin_reviews.csv ──────────────────────────────────────────────────────
print('=== michelin_reviews.csv ===')
mi_rev = pd.read_csv('reviews/michelin_reviews.csv', encoding='utf-8-sig', dtype=str, keep_default_na=False)
mi_rev = enrich(mi_rev, 'Restaurant Name')
# Reorder: place_id first
mi_rev = mi_rev[['place_id', 'Restaurant Name', 'Google Review Ratings', 'Reviews']]
mi_rev.to_csv('reviews/michelin_reviews.csv', index=False, encoding='utf-8-sig')
print(f'  {len(mi_rev)} rows | {mi_rev["place_id"].nunique()} restaurants')

# ── non-michelin_reviews.csv ──────────────────────────────────────────────────
print('=== non-michelin_reviews.csv ===')
nm_rev = pd.read_csv('reviews/non-michelin_reviews.csv', encoding='utf-8-sig', dtype=str, keep_default_na=False)
nm_rev = enrich(nm_rev, 'Restaurant Name')
nm_rev = nm_rev[['place_id', 'Restaurant Name', 'Google Review Ratings', 'Reviews']]
nm_rev.to_csv('reviews/non-michelin_reviews.csv', index=False, encoding='utf-8-sig')
print(f'  {len(nm_rev)} rows | {nm_rev["place_id"].nunique()} restaurants')

# ── mi_review_level_sentiment.csv ─────────────────────────────────────────────
print('=== mi_review_level_sentiment.csv ===')
mi_sent = pd.read_csv('reviews/mi_review_level_sentiment.csv', encoding='utf-8-sig', dtype=str, keep_default_na=False)
mi_sent = mi_sent.rename(columns={'title': 'Restaurant Name', 'stars': 'Google Review Ratings', 'text': 'Reviews'})
mi_sent = enrich(mi_sent, 'Restaurant Name')
sent_cols = ['value_tier','value_score','service_tier','service_score',
             'taste_tier','taste_score','value_tier_numeric','service_tier_numeric','taste_tier_numeric']
mi_sent = mi_sent[['place_id', 'Restaurant Name', 'Google Review Ratings', 'Reviews'] + sent_cols]
mi_sent.to_csv('reviews/mi_review_level_sentiment.csv', index=False, encoding='utf-8-sig')
print(f'  {len(mi_sent)} rows')

# ── nm_review_level_sentiment.csv ─────────────────────────────────────────────
print('=== nm_review_level_sentiment.csv ===')
nm_sent = pd.read_csv('reviews/nm_review_level_sentiment.csv', encoding='utf-8-sig', dtype=str, keep_default_na=False)
nm_sent = nm_sent.rename(columns={'title': 'Restaurant Name', 'stars': 'Google Review Ratings', 'text': 'Reviews'})
nm_sent = enrich(nm_sent, 'Restaurant Name')
nm_sent = nm_sent[['place_id', 'Restaurant Name', 'Google Review Ratings', 'Reviews'] + sent_cols]
nm_sent.to_csv('reviews/nm_review_level_sentiment.csv', index=False, encoding='utf-8-sig')
print(f'  {len(nm_sent)} rows')

# ── all_reviews.csv ───────────────────────────────────────────────────────────
print('\n=== Building all_reviews.csv ===')
mi_all = mi_sent.copy(); mi_all['Is Michelin'] = 'True'
nm_all = nm_sent.copy(); nm_all['Is Michelin'] = 'False'
all_rev = pd.concat([mi_all, nm_all], ignore_index=True)
all_rev = all_rev[['place_id', 'Restaurant Name', 'Is Michelin',
                    'Google Review Ratings', 'Reviews'] + sent_cols]
all_rev.to_csv('reviews/all_reviews.csv', index=False, encoding='utf-8-sig')
print(f'  {len(all_rev)} total reviews | {all_rev["place_id"].nunique()} restaurants')
print(f'  Michelin: {(all_rev["Is Michelin"]=="True").sum()} | Non-Michelin: {(all_rev["Is Michelin"]=="False").sum()}')

# ── Sync to backup ────────────────────────────────────────────────────────────
print('\n=== Syncing to _backup/ ===')
copies = [
    ('reviews/michelin_reviews.csv',            '_backup/intermediary_data/reviews/michelin_reviews.csv'),
    ('reviews/non-michelin_reviews.csv',         '_backup/intermediary_data/reviews/non-michelin_reviews.csv'),
    ('reviews/mi_review_level_sentiment.csv',    '_backup/intermediary_data/reviews/mi_review_level_sentiment.csv'),
    ('reviews/nm_review_level_sentiment.csv',    '_backup/intermediary_data/reviews/nm_review_level_sentiment.csv'),
    ('reviews/all_reviews.csv',                  '_backup/intermediary_data/reviews/all_reviews.csv'),
]
for src, dst in copies:
    shutil.copy2(src, dst)
    print(f'  {src}  →  {dst}')

print('\nDone.')
