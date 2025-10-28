import requests

def get_tiktok_video(link: str):
    """
    Gọi TikWM API qua proxy để Render không bị chặn IP.
    Trả về thông tin video TikTok không watermark.
    """
    proxy_url = "https://api.codetabs.com/v1/proxy?quest="
    api_url = f"https://www.tikwm.com/api/?url={link}"

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
        response = requests.get(proxy_url + api_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to TikWM API (proxy): {e}")

    try:
        data = response.json()
    except ValueError:
        raise Exception("Invalid JSON response from TikWM API")

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
