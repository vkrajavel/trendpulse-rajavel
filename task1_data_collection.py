"""Task 1: Collect live trending data from the Hacker News API (no API key needed)."""
import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

BASE_URL = "https://hacker-news.firebaseio.com/v0"
NUM_STORIES = 100
OUTPUT_FILE = "data/raw_data.csv"


def fetch_story(story_id):
    """Fetch one story; return None if the request fails."""
    try:
        resp = requests.get(f"{BASE_URL}/item/{story_id}.json", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Skipping story {story_id}: {e}")
        return None


def main():
    resp = requests.get(f"{BASE_URL}/topstories.json", timeout=10)
    resp.raise_for_status()
    story_ids = resp.json()[:NUM_STORIES]
    print(f"Fetching {len(story_ids)} trending stories...")

    with ThreadPoolExecutor(max_workers=10) as pool:
        items = list(pool.map(fetch_story, story_ids))

    rows = []
    for item in items:
        if not item:
            continue
        rows.append({
            "id": item.get("id"),
            "title": item.get("title"),
            "url": item.get("url"),
            "score": item.get("score"),
            "author": item.get("by"),
            "comments": item.get("descendants"),
            "time": item.get("time"),  # unix timestamp
            "type": item.get("type"),
        })

    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(df)} records to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
