"""Task 4: Visualise the trending data."""
import json
import os

import matplotlib
matplotlib.use("Agg")  # works without a display
import matplotlib.pyplot as plt
import pandas as pd

DATA_FILE = "data/clean_data.csv"
RESULTS_FILE = "data/analysis_results.json"
OUTPUT_DIR = "charts"


def shorten(text, n=40):
    return text if len(text) <= n else text[: n - 3] + "..."


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.read_csv(DATA_FILE)
    with open(RESULTS_FILE) as f:
        results = json.load(f)

    # 1. Top 10 stories by score
    top = pd.DataFrame(results["top_stories"])
    plt.figure(figsize=(10, 6))
    plt.barh([shorten(t) for t in top["title"]][::-1], top["score"][::-1], color="#4c72b0")
    plt.xlabel("Score")
    plt.title("Top 10 Trending Stories by Score")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/top_stories.png", dpi=150)
    plt.close()

    # 2. Top domains
    domains = results["top_domains"]
    plt.figure(figsize=(10, 6))
    plt.bar(domains.keys(), domains.values(), color="#55a868")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Number of stories")
    plt.title("Most Frequent Domains")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/top_domains.png", dpi=150)
    plt.close()

    # 3. Score vs comments
    plt.figure(figsize=(8, 6))
    plt.scatter(df["score"], df["comments"], alpha=0.6, color="#c44e52")
    plt.xlabel("Score")
    plt.ylabel("Comments")
    plt.title("Score vs Comments")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/score_vs_comments.png", dpi=150)
    plt.close()

    # 4. Top keywords
    kw = results["top_keywords"]
    plt.figure(figsize=(10, 6))
    plt.bar(kw.keys(), kw.values(), color="#8172b2")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Frequency")
    plt.title("Most Common Keywords in Titles")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/top_keywords.png", dpi=150)
    plt.close()

    print(f"Saved 4 charts to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
