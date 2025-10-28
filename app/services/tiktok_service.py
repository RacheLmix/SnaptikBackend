import requests

def get_tiktok_video(link: str):
    api_url = "https://www.tikwm.com/api/"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.1 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.tikwm.com/",
        "Origin": "https://www.tikwm.com",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(api_url, params={"url": link}, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to TikWM API: {e}")

    if response.status_code != 200:
        raise Exception(f"TikWM API returned status {response.status_code}")

    data = response.json()
    if not data.get("data"):
        raise Exception("Invalid response from TikWM API")

    video_data = data["data"]

    return {
        "title": video_data.get("title"),
        "author": video_data.get("author"),
        "play_url": video_data.get("play"),       # Không watermark
        "wmplay_url": video_data.get("wmplay"),   # Có watermark
        "music_url": video_data.get("music"),
        "cover": video_data.get("cover"),
    }
