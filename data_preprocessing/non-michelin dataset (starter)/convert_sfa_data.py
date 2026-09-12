import geopandas as gpd
import pandas as pd
import re

print("Loading SFA hygiene dataset...")

gdf = gpd.read_file("sfa_hygiene.geojson")

print("Columns:", gdf.columns)

records = []

for _, row in gdf.iterrows():

    description = str(row["Description"])

    # Extract licensee name
    name_match = re.search(r'LICENSEE_NAME</th>\s*<td>(.*?)</td>', description)

    # Extract hygiene grade
    grade_match = re.search(r'GRADE</th>\s*<td>(.*?)</td>', description)

    restaurant_name = name_match.group(1).lower().strip() if name_match else None
    hygiene_grade = grade_match.group(1).strip() if grade_match else None

    records.append({
        "restaurant_name": restaurant_name,
        "hygiene_grade": hygiene_grade,
        "latitude": row.geometry.y,
        "longitude": row.geometry.x
    })

df = pd.DataFrame(records)

# remove rows without restaurant names
df = df.dropna(subset=["restaurant_name"])

print("Total SFA establishments:", len(df))

df.to_csv("sfa_hygiene.csv", index=False)

print("Saved dataset: sfa_hygiene.csv")