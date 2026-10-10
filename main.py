import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Load environment variables
load_dotenv()

RATE_LIMIT_PER_HOUR = os.getenv("RATE_LIMIT_PER_HOUR", "10")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
MAX_NOTES_CHARS = int(os.getenv("MAX_NOTES_CHARS", "6000"))

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI App
app = FastAPI(
    title="Study Quiz Maker",
    description="Turn notes into multiple-choice quizzes with explanations using Claude API",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Path definitions
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Mount static files directory if it exists
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "app": "Study Quiz Maker",
        "version": "1.0.0",
        "model": CLAUDE_MODEL,
        "max_notes_chars": MAX_NOTES_CHARS,
    }


@app.get("/", response_class=HTMLResponse, tags=["Home"])
@limiter.limit(f"{RATE_LIMIT_PER_HOUR}/hour")
async def read_root(request: Request):
    """
    Root endpoint serving the initial page.
    If static/index.html exists, it serves that file; otherwise, serves a Phase 1 Hello verification page.
    """
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))

    return HTMLResponse(
        content="""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Study Quiz Maker</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      background: #0B1F23;
      color: #F6EFE3;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      text-align: center;
    }
    .card {
      background: rgba(246, 239, 227, 0.1);
      border: 1px solid rgba(246, 239, 227, 0.2);
      backdrop-filter: blur(16px);
      padding: 2.5rem 3rem;
      border-radius: 16px;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
      max-width: 520px;
    }
    h1 {
      color: #F2A33A;
      margin: 0 0 0.75rem 0;
      font-size: 2.2rem;
    }
    p {
      color: #F6EFE3;
      line-height: 1.6;
      margin: 0.5rem 0;
    }
    .badge {
      display: inline-block;
      margin-top: 1rem;
      padding: 0.35rem 0.85rem;
      background: #1F6F78;
      border-radius: 999px;
      font-size: 0.85rem;
      font-weight: 500;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>Study Quiz Maker</h1>
    <p><strong>Paste your notes. Get a quiz. Learn faster.</strong></p>
    <p>FastAPI backend initialized and ready. Phase 1 Setup complete.</p>
    <div class="badge">Backend Active &bull; Health: /health</div>
  </div>
</body>
</html>
"""
    )
