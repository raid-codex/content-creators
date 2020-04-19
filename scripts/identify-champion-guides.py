#!/usr/bin/env python3

import os
import sys
import json

with open(os.getenv("GOPATH")+"/src/github.com/raid-codex/data/docs/champions/current/index.json") as file:
    champions = json.load(file)

with open(sys.argv[1]) as file:
    creator = json.load(file)
    ids_to_watch = [playlist['id']
                    for playlist in creator['youtube']['playlists']
                    if "champion-guide" in playlist.get("tags", ())]
    for video in creator['youtube']['videos']:
        if video['playlist_id'] in ids_to_watch:
            if "champion_guide" in video:
                continue
            champions_matching = [
                champion for champion in champions
                if champion['name'].lower() in video['title'].lower()
            ]
            if not champions_matching:
                continue
            match = next(reversed(sorted(champions_matching,
                                         key=lambda x: len(x['name']))))
            video['champion_guide'] = {
                'champion_slug': match['slug'],
            }

with open(sys.argv[1], "w+") as file:
    json.dump(creator, file, indent=4)
