# Nex Music — Website Starter

A responsive Flask website with a dark neon-green interface. It validates HTTPS YouTube links and can request video metadata. It does **not** download or convert media in this starter.

## Run locally (Windows)

1. Install Python 3.11 or newer.
2. Open a terminal in this folder.
3. Create a virtual environment (optional but recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Run:

   ```powershell
   python app.py
   ```

6. Open http://127.0.0.1:5000

## Deploy publicly with Render

1. Upload this folder to a GitHub repository.
2. In Render, create a new Web Service and connect the repository.
3. Render can detect `render.yaml`, or set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app --workers 2 --threads 4 --timeout 60`
4. Deploy, then open the public `onrender.com` URL provided by Render.

## Notes

- The app is a starter, not a production media downloader.
- Use media tools only for content you own or have permission to download; follow YouTube's terms and applicable copyright law.
- Public metadata extraction can be rate-limited or blocked by the source platform.
- Before operating at scale, add request rate limits, caching, monitoring, and appropriate abuse protection.
