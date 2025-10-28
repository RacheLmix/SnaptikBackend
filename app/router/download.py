from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
import requests
from app.services.tiktok_service import get_tiktok_video

router = APIRouter()

def resolve_short_link(url: str) -> str:
    """
    Nếu TikTok URL là short link (tiktok.com/abc123), resolve về full URL.
    """
    try:
        response = requests.get(url, allow_redirects=False, timeout=10)
        # Nếu có redirect 301/302 → lấy location
        if response.status_code in [301, 302]:
            return response.headers.get("location", url)
        return url
    except Exception:
        # fallback nếu request fail
        return url


@router.get("/download")
def download_video(url: str = Query(..., description="TikTok video URL")):
    try:
        full_url = resolve_short_link(url)
        data = get_tiktok_video(full_url)
        return {
            "status": "success",
            "data": {
                "title": data.get("title"),
                "author": data.get("author"),
                "cover": data.get("cover"),
                "download_url": data.get("play_url"),  # link video không watermark
                "music_url": data.get("music_url")      # link nhạc (nếu cần)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/download/file")
def download_video_file(url: str = Query(..., description="TikTok video URL")):
    try:
        full_url = resolve_short_link(url)
        data = get_tiktok_video(full_url)
        video_url = data.get("play_url")

        if not video_url:
            raise HTTPException(status_code=404, detail="Video URL not found")

        video_response = requests.get(video_url, stream=True)
        if video_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching video stream")

        return StreamingResponse(
            video_response.iter_content(chunk_size=1024 * 1024),
            media_type="video/mp4",
            headers={"Content-Disposition": f"attachment; filename=video.mp4"}
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
