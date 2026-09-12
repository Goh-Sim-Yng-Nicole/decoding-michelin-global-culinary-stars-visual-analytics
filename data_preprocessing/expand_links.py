import pandas as pd
import requests
import concurrent.futures
import time
import os
import warnings

# Suppress requests dependency warnings
warnings.filterwarnings("ignore", category=UserWarning)

def expand_url(short_url, session, cache):
    if not isinstance(short_url, str) or "maps.app.goo.gl" not in short_url:
        return short_url
    
    if short_url in cache:
        return cache[short_url]
    
    try:
        # Use HEAD request to follow redirects without downloading the full page content
        response = session.head(short_url, allow_redirects=True, timeout=10)
        long_url = response.url
        cache[short_url] = long_url
        return long_url
    except Exception as e:
        print(f"Error expanding {short_url}: {e}")
        return short_url  # Return original if failed

def process_file(file_path):
    print(f"Processing {file_path}...")
    
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        print(f"Unsupported file type: {file_path}")
        return

    # Identify columns containing shortened links
    target_columns = []
    for col in df.columns:
        # Check first 100 rows for shortened links
        sample = df[col].head(100).astype(str)
        if sample.str.contains("maps.app.goo.gl").any():
            target_columns.append(col)
    
    if not target_columns:
        print(f"No shortened links found in {file_path}. Checked columns: {df.columns.tolist()}")
        return

    print(f"Found target columns: {target_columns}")
    
    cache = {}
    session = requests.Session()
    # Add a user agent to avoid being blocked
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    for col in target_columns:
        urls = df[col].unique().tolist()
        short_urls = [u for u in urls if isinstance(u, str) and "maps.app.goo.gl" in u]
        print(f"Found {len(short_urls)} unique shortened URLs in column '{col}'")
        
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_url = {executor.submit(expand_url, url, session, cache): url for url in short_urls}
            
            count = 0
            for future in concurrent.futures.as_completed(future_to_url):
                count += 1
                if count % 50 == 0:
                    elapsed = time.time() - start_time
                    avg_time = elapsed / count
                    remaining = (len(short_urls) - count) * avg_time
                    print(f"Processed {count}/{len(short_urls)} ({count/len(short_urls)*100:.1f}%) in {elapsed:.1f}s. Est. remaining: {remaining:.1f}s")
        
        # Apply the expanded URLs back to the dataframe
        df[col] = df[col].map(lambda x: cache.get(x, x))

    # Save the updated file
    if file_path.endswith('.xlsx'):
        df.to_excel(file_path, index=False)
    elif file_path.endswith('.csv'):
        df.to_csv(file_path, index=False)
    
    print(f"Successfully updated {file_path}")

if __name__ == "__main__":
    files_to_process = [
        "data_preprocessing/output/master.xlsx",
        "data_preprocessing/output/restaurants.xlsx",
        "data_preprocessing/output/restaurants.csv",
        "data_preprocessing/data/michelin_my_maps.csv"
    ]
    
    for f in files_to_process:
        if os.path.exists(f):
            process_file(f)
        else:
            print(f"File not found: {f}")
