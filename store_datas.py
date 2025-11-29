import MySQLdb
from bs4 import BeautifulSoup
import requests
import json
import os

# Connect to your WordPress/MariaDB database
conn = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    passwd="",
    db="videohub_db",
    charset="utf8mb4"
)
cursor = conn.cursor()

print("✅ Connected to videohub_db!")

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS wp_xhamster_videos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    link TEXT,
    thumbnail TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
print("✅ Table wp_xhamster_videos is ready!")

# ✅ Load your JSON file here
json_path = "xHamsterVideo.json"
if not os.path.exists(json_path):
    print("❌ xHamsterVideo.json not found!")
    exit(1)

with open(json_path, "r", encoding="utf-8") as f:
    videos = json.load(f)

print(f"📦 Loaded {len(videos)} videos from JSON file")

# ✅ Insert into database (skip duplicates)
inserted = 0
for video in videos:
    title = (video.get("title") or "").strip()
    link = (video.get("link") or "").strip()
    thumbnail = (video.get("thumbnail") or "").strip()

    if not title or not link:
        continue  # skip incomplete entries

    # Avoid duplicates: check by link
    cursor.execute("SELECT COUNT(*) FROM wp_xhamster_videos WHERE link=%s", (link,))
    exists = cursor.fetchone()[0]
    if exists:
        print(f"⚠️ Skipping duplicate: {title}")
        continue

    cursor.execute(
        "INSERT INTO wp_xhamster_videos (title, link, thumbnail) VALUES (%s, %s, %s)",
        (title, link, thumbnail)
    )
    inserted += 1

# ✅ Commit and close
conn.commit()
cursor.close()
conn.close()

print(f"🎬 Done! Inserted {inserted} new videos into wp_xhamster_videos ✅")
