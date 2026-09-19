import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import json

def get_channel_videos(channel_url, max_results=5):
    """
    Scrapes the latest video metadata from a YouTube channel using yt-dlp.
    """
    print(f"🔍 Fetching latest {max_results} videos from {channel_url}...")
    ydl_opts = {
        'extract_flat': True,
        'playlistend': max_results,
        'quiet': True
    }
    
    try:
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
            print(f"✅ Found {len(videos)} videos.")
            return videos
    except Exception as e:
        print(f"❌ Error scraping channel: {e}")
        return []

def extract_transcript(video_id):
    """
    Extracts the transcript of a YouTube video (prefers Thai, then English).
    """
    print(f"📝 Extracting transcript for video ID: {video_id}...")
    try:
        # Prefer Thai, fallback to English
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['th', 'en'])
        
        full_text = " ".join([item['text'] for item in transcript_list])
        print("✅ Transcript extracted successfully.")
        return full_text
    except Exception as e:
        print(f"❌ Error fetching transcript: {e}")
        return None

if __name__ == "__main__":
    # Example Usage:
    # 1. Get videos from a channel
    # target_channel = "https://www.youtube.com/@SatangTheValue"
    # recent_videos = get_channel_videos(target_channel, max_results=2)
    # print(json.dumps(recent_videos, indent=2, ensure_ascii=False))
    
    # 2. Extract transcript from the first video
    # if recent_videos:
    #     vid_id = recent_videos[0]['id']
    #     transcript = extract_transcript(vid_id)
    #     if transcript:
    #         print(f"\\nSnippet: {transcript[:200]}...")
    
    print("Use this as an imported module: `from youtube_pipeline import get_channel_videos, extract_transcript`")