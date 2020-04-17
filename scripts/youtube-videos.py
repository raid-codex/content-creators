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
        if not next_token:
            break
    return videos


def is_good_video(video):
    title = video.get("snippet").get("title")
    if title == "7 Signs You're Going To Be Successful":
        return False
    elif title == "Finding The ULTIMATE Twitch Stream Camera":
        return False
    elif title == "What's the biggest mistake in content marketing?":
        return False
    elif title == "Private video":
        return False
    return True


with open(sys.argv[1]) as file:
    data = json.load(file)
    videos = []
    for playlist in data['youtube']['playlists']:
        from_playlist = get_videos_from_playlist(playlist_id=playlist['id'])
        videos += [{
            "title": video.get("snippet", {}).get("title"),
            "published_at": video.get("snippet", {}).get("publishedAt"),
            "id": video.get("snippet", {}).get("resourceId", {}).get("videoId"),
            "playlist_id": playlist['id'],
        } for video in from_playlist if is_good_video(video)]
    data['youtube']['videos'] = sorted(videos,
                                       key=lambda x: x['published_at'], reverse=True)

with open(sys.argv[1], "w+") as file:
    json.dump(data, file, indent=4)
