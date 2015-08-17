#!/usr/bin/python
import scrape_top_40 as s

from datetime import datetime, date, time
from pymongo import MongoClient

client = MongoClient()
db = client.hits
cursor = db.songs.find()
for song in cursor:
    song_data = s.youtube_search(song)

    statistics = song_data["statistics"]
    statistics["time"] = datetime.now()
    song["statistics"].append(statistics)
    db.songs.save(song)
cursor.close()
