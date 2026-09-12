"""
build_wordcloud_data.py
============================================================
Tokenises all_reviews.csv into a flat (place_id, word, count)
table suitable for a Tableau hierarchical word cloud.

Output: reviews/wordcloud_data.csv
Columns:
    place_id | Restaurant Name | Is Michelin |
    Google Review Ratings | word | count

Usage:
    python build_wordcloud_data.py
============================================================
"""

import sys, re, shutil
import pandas as pd
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

# ── Stop-word list ─────────────────────────────────────────────────────────────
# Standard English stop words + review-specific noise
STOP_WORDS = {
    # articles / prepositions / conjunctions
    'a','an','the','and','or','but','in','on','at','to','for','of','with',
    'by','from','as','into','through','during','before','after','above',
    'below','between','out','off','over','under','again','further','then',
    'once','about','up','down','is','am','are','was','were','be','been',
    'being','have','has','had','do','does','did','will','would','could',
    'should','may','might','shall','can','need','dare','ought','used',
    'if','because','while','although','though','since','unless','until',
    'when','where','who','which','what','that','this','these','those',
    'i','me','my','myself','we','our','ours','you','your','yours',
    'he','him','his','she','her','hers','it','its','they','them','their',
    'theirs','not','no','nor','so','yet','both','either','neither',
    'each','every','all','any','few','more','most','other','some','such',
    'than','too','very','just','also','still','even','back','much',
    'how','why','here','there','its','i\'m','it\'s','don\'t','didn\'t',
    'wasn\'t','can\'t','couldn\'t','won\'t','wouldn\'t','i\'ve','i\'ll',
    'they\'re','we\'re','you\'re','he\'s','she\'s','there\'s',
    # common review filler
    'came','come','comes','coming','went','go','goes','going','got','get',
    'gets','getting','made','make','makes','making','said','say','says',
    'saying','asked','ask','told','tell','tells','took','take','takes',
    'taking','us','time','place','one','two','three','four','five',
    'first','second','last','next','well','really','quite','pretty',
    'bit','lot','lots','little','big','small','good','great','nice',
    'bad','long','way','day','days','night','been','had',
    'ordered','order','tried','try','table','seat','seats','staff',
    'restaurant','food','place','visit','experience','overall','would',
    'recommend','definitely','definitely','singapore','sg',
}

def tokenise(text: str) -> list[str]:
    """Lowercase, strip punctuation, keep words >= 3 chars not in stop words."""
    text = text.lower()
    words = re.findall(r"[a-z]+(?:'[a-z]+)?", text)
    return [w for w in words if len(w) >= 3 and w not in STOP_WORDS]


# ── Load reviews ───────────────────────────────────────────────────────────────
print('Loading all_reviews.csv …')
df = pd.read_csv('reviews/all_reviews.csv', encoding='utf-8-sig', dtype=str, keep_default_na=False)
print(f'  {len(df):,} reviews | {df["place_id"].nunique():,} restaurants')

# ── Tokenise and count per restaurant ─────────────────────────────────────────
print('Tokenising …')
records = []
group_cols = ['place_id', 'Restaurant Name', 'Is Michelin', 'Google Review Ratings']

for keys, grp in df.groupby(group_cols, sort=False):
    place_id, name, is_michelin, rating = keys
    all_words = []
    for review in grp['Reviews']:
        all_words.extend(tokenise(review))
    for word, cnt in Counter(all_words).items():
        records.append({
            'place_id': place_id,
            'Restaurant Name': name,
            'Is Michelin': is_michelin,
            'Google Review Ratings': rating,
            'word': word,
            'count': cnt,
        })

out = pd.DataFrame(records)

# Sort: most frequent words first within each restaurant
out = out.sort_values(['place_id', 'count'], ascending=[True, False]).reset_index(drop=True)

print(f'  {len(out):,} (restaurant, word) pairs | {out["word"].nunique():,} unique words')
print(f'\nTop 20 words across all reviews:')
print(out.groupby('word')['count'].sum().nlargest(20).to_string())

# ── Save ───────────────────────────────────────────────────────────────────────
out.to_csv('reviews/wordcloud_data.csv', index=False, encoding='utf-8-sig')
print(f'\nSaved → reviews/wordcloud_data.csv')

shutil.copy2('reviews/wordcloud_data.csv', '_backup/intermediary_data/reviews/wordcloud_data.csv')
print(f'Synced → _backup/intermediary_data/reviews/wordcloud_data.csv')
print('\nDone.')
