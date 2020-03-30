#!/usr/bin/env python3

import os
import sys
import json

from apiclient.discovery import build
from apiclient.errors import HttpError

youtube = build("youtube", "v3", developerKey=os.getenv("GOOGLE_API_KEY"))


def get_videos_from_playlist(playlist_id):
    args = {
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": 50,
    }
    next_token = ""
    videos = []
    while 42:
        kwargs = {}
        kwargs.update(args)
        if next_token:
            kwargs["pageToken"] = next_token
        response = youtube.playlistItems().list(**kwargs).execute()
        next_token = response.get("nextPageToken")
        items = response.get("items")
        if not items:
            break
        videos += items
        if len(items) != 50:
            break
    return videos


with open(sys.argv[1]) as file:
    data = json.load(file)
    videos = []
    for playlist in data['youtube']['playlists']:
        videos += get_videos_from_playlist(playlist_id=playlist['id'])
    data['youtube']['videos'] = sorted([{
        "title": video.get("snippet", {}).get("title"),
        "published_at": video.get("snippet", {}).get("publishedAt"),
        "id": video.get("snippet", {}).get("resourceId", {}).get("videoId"),
    } for video in videos], key=lambda x: x['published_at'], reverse=True)

print(json.dumps(data))
