import requests

def get_tiktok_video(link: str):
    api_url = "https://www.tikwm.com/api/"
    response = requests.get(api_url, params={"url": link})
    if response.status_code != 200:
        raise Exception("Error connecting to TikWM API")

    data = response.json()
    if not data.get("data"):
        raise Exception("Invalid response from TikWM API")

    video_data = data["data"]
    return {
        "title": video_data.get("title"),
        "author": video_data.get("author"),
        "play_url": video_data.get("play"),
        "wmplay_url": video_data.get("wmplay"),
        "music_url": video_data.get("music"),
        "cover": video_data.get("cover"),
    }
