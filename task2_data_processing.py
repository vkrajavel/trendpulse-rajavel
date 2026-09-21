"""Task 2: Clean and prepare the raw trending data."""
from urllib.parse import urlparse

import pandas as pd

INPUT_FILE = "data/raw_data.csv"
OUTPUT_FILE = "data/clean_data.csv"


def get_domain(url):
    if pd.isna(url):
        return "news.ycombinator.com"  # text posts have no external URL
    return urlparse(url).netloc.replace("www.", "")


def main():
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} rows")

    # Remove duplicates and rows without essential fields
    df = df.drop_duplicates(subset="id")
    df = df.dropna(subset=["title", "score", "time"])

    # Fix types and fill gaps
    df["comments"] = df["comments"].fillna(0).astype(int)
    df["score"] = df["score"].astype(int)
    df["title"] = df["title"].str.strip().str.replace(r"\s+", " ", regex=True)

    # Feature engineering
    df["posted_at"] = pd.to_datetime(df["time"], unit="s")
    df["hour"] = df["posted_at"].dt.hour
    df["domain"] = df["url"].apply(get_domain)
    df["title_length"] = df["title"].str.len()

    df = df.drop(columns=["time"]).reset_index(drop=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(df)} clean rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
