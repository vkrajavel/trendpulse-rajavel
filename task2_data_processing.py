import pandas as pd
import glob
import os

# Find the trends JSON file inside the data folder.
# This allows the script to work with the YYYYMMDD filename.
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No trends JSON file found in the data folder.")
    exit()

json_file = json_files[0]

# Load the JSON data into a Pandas DataFrame.
df = pd.read_json(json_file)

print(f"Loaded {len(df)} stories from {json_file}")


# ---------------------------------------------------------
# 1. Remove duplicate stories
# ---------------------------------------------------------
# Each story should have a unique post_id.
df = df.drop_duplicates(subset="post_id")

print(f"After removing duplicates: {len(df)}")


# ---------------------------------------------------------
# 2. Remove rows with missing important values
# ---------------------------------------------------------
# A story is not useful if it has no ID, title, or score.
df = df.dropna(subset=["post_id", "title", "score"])

print(f"After removing nulls: {len(df)}")


# ---------------------------------------------------------
# 3. Fix data types
# ---------------------------------------------------------
# Convert score and num_comments to numbers.
# Invalid values are converted to NaN.
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

# Remove rows where conversion created missing values.
df = df.dropna(subset=["score", "num_comments"])

# Convert the columns to integers.
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# ---------------------------------------------------------
# 4. Remove low-quality stories
# ---------------------------------------------------------
# Keep only stories with a score of 5 or higher.
df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")


# ---------------------------------------------------------
# 5. Clean whitespace from titles
# ---------------------------------------------------------
# Strip unnecessary spaces from the beginning and end.
df["title"] = df["title"].str.strip()


# ---------------------------------------------------------
# 6. Save the cleaned data
# ---------------------------------------------------------
output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")


# ---------------------------------------------------------
# 7. Print stories per category
# ---------------------------------------------------------
print("\nStories per category:")

category_counts = df["category"].value_counts()

print(category_counts)
