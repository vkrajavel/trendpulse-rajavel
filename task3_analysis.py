"""Task 3: Analyse the cleaned trending data."""
import json
import re
from collections import Counter

import pandas as pd

INPUT_FILE = "data/clean_data.csv"
OUTPUT_FILE = "data/analysis_results.json"

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "is",
    "are", "how", "why", "what", "you", "your", "i", "it", "at", "by", "from",
    "this", "that", "be", "as", "we", "my", "not", "show", "hn", "ask", "new",
}


def main():
    df = pd.read_csv(INPUT_FILE, parse_dates=["posted_at"])

    top_stories = (df.nlargest(10, "score")[["title", "score", "comments", "domain"]]
                   .to_dict("records"))
    top_domains = df["domain"].value_counts().head(10).to_dict()
    avg_score_by_hour = df.groupby("hour")["score"].mean().round(1).to_dict()

    words = []
    for title in df["title"]:
        words += [w for w in re.findall(r"[a-zA-Z]{3,}", title.lower()) if w not in STOPWORDS]
    top_keywords = dict(Counter(words).most_common(15))

    results = {
        "total_stories": int(len(df)),
        "average_score": round(df["score"].mean(), 2),
        "median_score": float(df["score"].median()),
        "average_comments": round(df["comments"].mean(), 2),
        "score_comments_correlation": round(df["score"].corr(df["comments"]), 3),
        "average_title_length": round(df["title_length"].mean(), 1),
        "top_stories": top_stories,
        "top_domains": top_domains,
        "avg_score_by_hour": avg_score_by_hour,
        "top_keywords": top_keywords,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print("=== TrendPulse Analysis ===")
    print(f"Stories analysed : {results['total_stories']}")
    print(f"Average score    : {results['average_score']}")
    print(f"Average comments : {results['average_comments']}")
    print(f"Score/comment correlation: {results['score_comments_correlation']}")
    print(f"Top domains      : {list(top_domains)[:5]}")
    print(f"Top keywords     : {list(top_keywords)[:8]}")
    print(f"Saved results to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
