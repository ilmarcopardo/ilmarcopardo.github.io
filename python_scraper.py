# File: scholar_scraper.py
import json
from scholarly import scholarly

# --- CONFIGURATION ---
AUTHOR_ID = '1XGhMwgAAAAJ' # <--- PUT YOUR ID HERE
OUTPUT_FILE = 'publications.json'

def fetch_publications():
    print(f"Fetching publications for author ID: {AUTHOR_ID}")
    
    try:
        # 1. Search for the author
        author = scholarly.search_author_id(AUTHOR_ID)
        
        # 2. Fill the author object with publication data
        print("Filling author data (this might take a moment)...")
        author = scholarly.fill(author, sections=['publications'])
        
        publications_list = []
        
        # 3. Extract relevant data from each publication
        for pub in author['publications']:
            # We fetch the 'bib' section to get the year and title accurately
            # Note: scholarly.fill(pub) would get more details but is slower/riskier for blocking
            
            title = pub['bib'].get('title', 'No Title')
            year = pub['bib'].get('pub_year', 'N/A')
            url = pub.get('pub_url', '#') # Link to the paper if available
            citation = pub.get('num_citations', 0)
            
            # Create a clean dictionary for our JSON
            pub_data = {
                "title": title,
                "year": year,
                "url": url,
                "citations": citation
            }
            publications_list.append(pub_data)
            print(f"Found: {title} ({year})")

        # 4. Sort by year (newest first)
        publications_list.sort(key=lambda x: x['year'], reverse=True)

        # 5. Save to JSON
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(publications_list, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully saved {len(publications_list)} publications to {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    fetch_publications()