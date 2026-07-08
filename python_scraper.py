# File: python_scraper.py
import json
import os
import time
import random
from scholarly import scholarly

# --- CONFIGURATION ---
AUTHOR_ID = '1XGhMwgAAAAJ' # <--- PUT YOUR ID HERE
OUTPUT_FILE = 'publications.json'
MAX_RETRIES = 5

def fetch_publications_with_retries(author_id):
    last_exc = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            author = scholarly.search_author_id(author_id)
            print("Filling author data (this might take a moment)...")
            author = scholarly.fill(author, sections=['publications'])
            return author.get('publications', [])
        except Exception as e:
            last_exc = e
            sleep_s = min(60, (2 ** attempt) + random.uniform(0.5, 2.5))
            print(f"[Attempt {attempt}/{MAX_RETRIES}] Scholar fetch failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(sleep_s)
    raise last_exc

def fetch_publications():
    print(f"Fetching publications for author ID: {AUTHOR_ID}")
    
    try:
        pubs = fetch_publications_with_retries(AUTHOR_ID)
        
        publications_list = []
        
        # Extract relevant data from each publication
        for pub in pubs:
            title = pub['bib'].get('title', 'No Title')
            year = pub['bib'].get('pub_year', 'N/A')
            url = pub.get('pub_url', '#') # Link to the paper if available
            citation = pub.get('num_citations', 0)
            
            # Extract venue if available (usually in 'citation', 'journal', or 'conference' within the bib dict)
            venue = pub['bib'].get('citation', pub['bib'].get('journal', pub['bib'].get('conference', '')))
            
            # Create a clean dictionary for our JSON
            pub_data = {
                "title": title,
                "year": year,
                "url": url,
                "citations": citation,
                "venue": venue
            }
            publications_list.append(pub_data)
            print(f"Found: {title} ({year}) - Venue: {venue}")

        # Sort by year (newest first)
        publications_list.sort(key=lambda x: str(x['year']), reverse=True)

        # Save to JSON
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(publications_list, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully saved {len(publications_list)} publications to {OUTPUT_FILE}")

    except Exception as e:
        print(f"Warning: Could not fetch from Google Scholar: {e}")
        if os.path.exists(OUTPUT_FILE):
            print("Keeping existing publications.json and exiting without failing workflow.")
            # Exit 0 so scheduled job doesn't fail due to transient Scholar issues
            return
        # If no fallback file exists, fail clearly
        import sys
        sys.exit("No existing publications.json available; failing run.")

if __name__ == "__main__":
    fetch_publications()