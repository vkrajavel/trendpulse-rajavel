import requests
import time
import json
import os
from datetime import datetime

# Hacker News API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required User-Agent header
HEADERS = {
    "User-Agent": "TrendPulse/1.0"
}

# Keywords used to classify stories
CATEGORY_KEYWORDS = {
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


def get_category(title):
    """
    Check the title against each category's keywords.
    Matching is case-insensitive.
    """
    title_lower = title.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category

    return None


# ---------------------------------------------------------
# Step 1: Get the top 500 Hacker News story IDs
# ---------------------------------------------------------

try:
    response = requests.get(
        TOP_STORIES_URL,
        headers=HEADERS,
        timeout=10
    )
    response.raise_for_status()

    story_ids = response.json()[:500]

    print(f"Fetched {len(story_ids)} top story IDs.")

except requests.RequestException as error:
    print(f"Failed to fetch top stories: {error}")
    exit()


# ---------------------------------------------------------
# Step 2: Fetch the details of each story
# ---------------------------------------------------------

stories = []

for story_id in story_ids:
    try:
        response = requests.get(
            ITEM_URL.format(story_id),
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()
        story = response.json()

        # Ignore deleted/dead stories or stories without titles
        if not story or story.get("type") != "story":
            continue

        if not story.get("title"):
            continue

        category = get_category(story["title"])

        # Only keep stories that match one of our categories
        if category is None:
            continue

        # Store the seven fields required by the assignment
        cleaned_story = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().isoformat()
        }

        stories.append(cleaned_story)

    except requests.RequestException as error:
        # If one story fails, continue with the remaining stories
        print(f"Failed to fetch story {story_id}: {error}")
        continue


# ---------------------------------------------------------
# Step 3: Keep maximum 25 stories in each category
# ---------------------------------------------------------

selected_stories = []

for category in CATEGORY_KEYWORDS:
    category_stories = [
        story for story in stories
        if story["category"] == category
    ]

    # Keep no more than 25 stories for this category
    selected_stories.extend(category_stories[:25])

    print(
        f"{category}: "
        f"{len(category_stories[:25])} stories selected"
    )

    # Wait 2 seconds between category loops
    time.sleep(2)


# ---------------------------------------------------------
# Step 4: Create the data folder if it doesn't exist
# ---------------------------------------------------------

os.makedirs("data", exist_ok=True)


# ---------------------------------------------------------
# Step 5: Save the collected stories as JSON
# ---------------------------------------------------------

output_file = "data/trends_20240115.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(selected_stories, file, indent=4, ensure_ascii=False)


print(
    f"\nCollected {len(selected_stories)} stories. "
    f"Saved to {output_file}"
)
