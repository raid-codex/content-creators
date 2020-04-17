update_youtube:
	python3 scripts/youtube-videos.py docs/$(CREATOR).json

identify_champion_guides:
	python3 scripts/identify-champion-guides.py docs/$(CREATOR).json
