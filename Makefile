update_youtube:
	python3 scripts/youtube-videos.py docs/$(CREATOR).json | python -m json.tool > /tmp/creator.json
	mv /tmp/creator.json docs/$(CREATOR).json