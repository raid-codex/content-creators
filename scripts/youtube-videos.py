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
    elif title == "Private video" or title == "Deleted video":
        return False
    return True


with open(sys.argv[1]) as file:
    data = json.load(file)
    old_videos = {video['id']: video for video in data['youtube'].get('videos', [])}
    videos = []
    for playlist in data['youtube']['playlists']:
        from_playlist = get_videos_from_playlist(playlist_id=playlist['id'])
        for video in from_playlist:
            if not is_good_video(video):
                continue
            id = video.get("snippet", {}).get("resourceId", {}).get("videoId")
            if old_videos.get(id):
                continue
            else:
                d = {
                    "title": video.get("snippet", {}).get("title"),
                    "published_at": video.get("snippet", {}).get("publishedAt"),
                    "id": id,
                    "playlist_id": playlist['id'],
                }
                print(f"new video: {d['title']}")
                old_videos[id] = d
    data['youtube']['videos'] = sorted(old_videos.values(),
                                       key=lambda x: x['published_at'], reverse=True)

with open(sys.argv[1], "w+") as file:
    json.dump(data, file, indent=4)
