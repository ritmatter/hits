#!/usr/bin/python
import sys
import urllib
import json
import urllib2
from bs4 import BeautifulSoup
import requests

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyC0dXWQUJlEehLrDocc3ckY1RgNioxltig"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Get the top 40 hits as an array of strings ready for query
def get_top_40():
    page = requests.get('http://www.bigtop40.com/chart/archive/2015/33/').text
    page_soup = BeautifulSoup(page)
    uls = page_soup.select(".chart_list")

    # HTML structure slightly different for some pages
    ul = uls[0]
    lis = ul.select("li")

    queries = []
    i = 1
    for li in lis:

        if li.h3.a:
            title = li.h3.a.find(text=True, recursive=False)
        else:
            title = li.h3.find(text=True, recursive=False)
        artist = li.h3.span.text

        artist = artist.replace("by", "").strip()
        title = title.replace("by", "").strip()

        querydata = {}
        querydata['artist'] = artist
        querydata['title'] = title
        querydata['query'] = artist + " " + title
        queries.append(querydata)
        i += 1

    return queries

def youtube_search(querydata):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
    q=querydata["artist"] + " " + querydata["title"],
    part="id,snippet",
    maxResults=10,
    type="video"
    ).execute()

    video_ids = []
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.

    search_videos = []
    # Merge video ids

    for search_result in search_response.get("items", []):
        search_videos.append(search_result["id"]["videoId"])
    video_ids = ",".join(search_videos)

    video_response = youtube.videos().list(
        part="snippet,statistics",
        id=video_ids
    ).execute()

    return {
        'artist': querydata["artist"],
        'title': querydata["title"],
        'youtube_id': video_response.get("items")[0]["id"],
        'published_at': video_response.get("items")[0]["snippet"]["publishedAt"],
        'category_id': video_response.get("items")[0]["snippet"]["categoryId"],
        'statistics': video_response.get("items")[0]["statistics"]
    }
