#!/usr/bin/python
import scrape_top_40 as s

from datetime import datetime, date, time
from pymongo import MongoClient

client = MongoClient()
db = client.hits

querydata = s.get_top_40()
for entry in querydata:
    entry_data = s.youtube_search(entry)

    statistics = entry_data["statistics"]
    statistics["time"] = datetime.now()
    entry_data["statistics"] = []
    entry_data["statistics"].append(statistics)
    db.songs.insert_one(entry_data)
