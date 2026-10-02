import os
import re
from urllib.parse import urlparse

from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

YOUTUBE_HOSTS = {
    "youtube.com", "www.youtube.com", "m.youtube.com",
    "youtu.be", "www.youtube-nocookie.com"
}

def valid_youtube_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
        return (
            parsed.scheme == "https"
            and (parsed.hostname or "").lower() in YOUTUBE_HOSTS
            and parsed.path not in ("", "/")
        )
    except Exception:
        return False

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/info")
def video_info():
    data = request.get_json(silent=True) or {}
    url = str(data.get("url", "")).strip()

    if not valid_youtube_url(url):
        return jsonify({"error": "Please enter a valid HTTPS YouTube video URL."}), 400

    # Metadata only: no downloading. Use only for content you own or have permission to use.
    try:
        opts = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "skip_download": True,
            "socket_timeout": 15,
            "extractor_retries": 1,
            "retries": 1,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            "title": info.get("title") or "Untitled video",
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "channel": info.get("channel") or info.get("uploader") or "Unknown channel",
            "webpage_url": info.get("webpage_url") or url,
        })
    except Exception:
        return jsonify({
            "error": "Could not load video information. It may be unavailable or restricted. Please try another URL."
        }), 422

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # Local development only. Production should use gunicorn and keep debug disabled.
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
