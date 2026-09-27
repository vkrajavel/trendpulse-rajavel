import pandas as pd
import glob
import os

# Find the latest JSON file from the data folder
json_files = glob.glob("data/trends_*.json")
json_file = sorted(json_files)[-1]

# Load the JSON data
df = pd.read_json(json_file)

print(f"Loaded {len(df)} stories from {json_file}")

# Remove duplicate post IDs
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# Remove rows with missing important values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Convert score and number of comments to integers
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

# Remove rows that became invalid after conversion
df = df.dropna(subset=["score", "num_comments"])

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove stories with a score below 5
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Remove extra spaces from titles
df["title"] = df["title"].str.strip()

# Save the cleaned data
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# Show number of stories in each category
print("\nStories per category:")
print(df["category"].value_counts())
