#!/usr/bin/python

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

def youtube_search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
    q=query,
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

    print video_response.get("items")[0]["snippet"]["title"]
    print video_response.get("items")[0]["statistics"]





youtube_search('happy')
