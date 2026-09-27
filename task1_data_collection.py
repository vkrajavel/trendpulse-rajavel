import requests
import time
import json
import os
from datetime import datetime

# HackerNews API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Identify our script to the API
headers = {"User-Agent": "TrendPulse/1.0"}

# Keywords used to assign stories to categories
categories = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game", "book",
        "show", "award", "streaming"
    ]
}

# Step 1: Fetch the top 500 story IDs
try:
    response = requests.get(
        TOP_STORIES_URL,
        headers=headers,
        timeout=10
    )
    response.raise_for_status()
    story_ids = response.json()[:500]
except requests.RequestException as e:
    print(f"Failed to fetch top stories: {e}")
    story_ids = []

# Fetch details for each story
stories = []

for story_id in story_ids:
    try:
        response = requests.get(
            ITEM_URL.format(story_id),
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        story = response.json()

        # Only process stories that have a title
        if story and story.get("title"):
            stories.append(story)

    except requests.RequestException as e:
        print(f"Failed to fetch story {story_id}: {e}")
        continue

# Step 2: Assign stories to categories
collected_stories = []
used_story_ids = set()

for category, keywords in categories.items():

    category_count = 0

    for story in stories:

        # Stop after collecting 25 stories for this category
        if category_count >= 25:
            break

        story_id = story.get("id")

        # Do not use the same story in multiple categories
        if story_id in used_story_ids:
            continue

        title = story.get("title", "")
        title_lower = title.lower()

        # Check whether the title contains a category keyword
        if any(keyword.lower() in title_lower for keyword in keywords):

            collected_stories.append({
                "post_id": story_id,
                "title": title,
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", ""),
                "collected_at": datetime.now().isoformat()
            })

            used_story_ids.add(story_id)
            category_count += 1

    # Wait 2 seconds between category loops
    if category != list(categories.keys())[-1]:
        time.sleep(2)

# Step 3: Create the data folder if it does not exist
os.makedirs("data", exist_ok=True)

# Create filename using today's date
date_string = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{date_string}.json"

# Save collected stories to JSON
with open(filename, "w", encoding="utf-8") as file:
    json.dump(collected_stories, file, indent=2, ensure_ascii=False)

# Print the final result
print(
    f"Collected {len(collected_stories)} stories. "
    f"Saved to {filename}"
)
