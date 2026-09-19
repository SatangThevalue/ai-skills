---
name: youtube-data-extraction
description: "Fetch YouTube channel videos, metadata, and transcripts using yt-dlp and APIs."
version: 0.1.0
metadata:
  hermes:
    tags: [YouTube, Scraping, API, yt-dlp, Data-Pipeline]
    related_skills: [python-ai-video-monetization, llm-prompt-orchestration]
---

# YouTube Data Extraction Pipeline

This skill covers the methodology for extracting video metadata, channel updates, and transcripts from YouTube. It provides two distinct approaches: using the Official YouTube Data API v3 (for structured, authenticated queries) and using `yt-dlp` / `youtube-transcript-api` (for scraping without API keys). This serves as upstream data gathering for Content Evaluation, AI summarization, or competitor analysis.

## When to Use
- When you need to monitor a competitor's YouTube channel for new videos.
- When you want to extract the transcript of a video to feed into an LLM for summarization or script rewriting.
- When scraping metadata (views, likes, titles) for analytical scoring without using YouTube API quota.

## Prerequisites
- Python environment (`uv`).
- Packages: `uv pip install yt-dlp youtube-transcript-api google-api-python-client`
- (Optional) Google Cloud API Key with "YouTube Data API v3" enabled for the official route.

## How to Run
Invoke the Python scripts via the `terminal` tool. Scripts can output JSON data which is then saved to the PostgreSQL Vault.

## Quick Reference
- `yt-dlp` JSON dump: `yt-dlp -J --flat-playlist <CHANNEL_URL>`
- `youtube-transcript-api`: `YouTubeTranscriptApi.get_transcript(video_id, languages=['th', 'en'])`

## Procedure

### Method 1: The Scraping Route (`yt-dlp`)
Best for getting the latest videos from a channel without an API key.

```python
import yt_dlp
import json

def get_latest_videos(channel_url, max_results=5):
    ydl_opts = {
        'extract_flat': True,
        'playlistend': max_results,
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        
        videos = []
        for entry in info.get('entries', []):
            videos.append({
                "id": entry.get("id"),
                "title": entry.get("title"),
                "url": entry.get("url"),
                "duration": entry.get("duration"),
                "view_count": entry.get("view_count")
            })
            
        return videos

# Example: get_latest_videos("https://www.youtube.com/@SatangTheValue")
```

### Method 2: Transcript Extraction
Best for extracting the spoken words of a video to feed to an LLM (CLIProxyAPI).

```python
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_transcript(video_id):
    try:
        # Prefer Thai, fallback to English
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['th', 'en'])
        
        full_text = " ".join([item['text'] for item in transcript])
        return full_text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None
```

### Method 3: Official YouTube Data API v3
Best for robust, high-volume production systems where scraping might get blocked.
*(Requires setting `YOUTUBE_API_KEY` in `.env`)*

```python
from googleapiclient.discovery import build
import os

def get_channel_stats(channel_id):
    api_key = os.getenv("YOUTUBE_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    request = youtube.channels().list(
        part="statistics,snippet",
        id=channel_id
    )
    response = request.execute()
    return response['items'][0] if response['items'] else None
```

## Pitfalls
- **`yt-dlp` Breakage:** YouTube frequently updates its site structure to block scrapers. If `yt-dlp` suddenly throws extraction errors, update the package (`uv pip install -U yt-dlp`).
- **No Transcripts:** `youtube-transcript-api` will fail if the creator has disabled auto-generated captions or hasn't uploaded any. Always handle the exception.
- **API Quota:** The official YouTube API has a strict daily quota (usually 10,000 units). Searching for videos costs 100 units per request. Use web scraping (`yt-dlp`) for searches/lists to save quota, and reserve the API for specific stat lookups.

## Verification
Run a Python script utilizing `yt_dlp` on a public channel URL. The output should be a valid JSON array containing the titles and IDs of the channel's recent videos.