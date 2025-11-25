

# AQI City Search (Python + FastAPI + HTML CSS JS)

A simple Air Quality Index search application using the AQICN API.

## What this repo contains
- `backend/` — FastAPI backend that wraps the AQICN API and provides caching (LRU + TTL).
  - `app/` — Python app files (`main.py`, `cache_store.py`, `schemas.py`, `requirements.txt`)
  - `.env.example` — example environment variables
  - `Dockerfile` — simple image build
- `frontend/` — static frontend (vanilla HTML/CSS/JS). `index.html` and `style.css`

## Features
- Search air quality by city name using AQICN (`/api/aqi?city=CityName`)
- In-memory LRU cache with TTL to speed repeat queries
- Displays AQI, dominant pollutant, per-pollutant values, coordinates, timestamp
- Small, dependency-free frontend for easy local testing

## API used
**AQICN** (World Air Quality Index project)  
Endpoint used:


GET https://api.waqi.info/feed/{city}/?token={TOKEN}

Get a free token (for development) here: https://aqicn.org/data-platform/token/

## Running locally

### 1. Get your AQICN token
Register and get your token: https://aqicn.org/data-platform/token/

### 2. Backend
```bash
cd backend
cp .env.example .env
# Edit .env and set AQICN_TOKEN=<your_token_here>

# create a virtualenv and activate
python -m venv venv
# Windows
venv\\Scripts\\activate
# macOS / Linux
source venv/bin/activate

pip install -r app/requirements.txt

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


API endpoint: http://127.0.0.1:8000/api/aqi?city=Delhi

FastAPI docs: http://127.0.0.1:8000/docs

3. Frontend

Option A — open file:

Open frontend/index.html in your browser (works without server).

Option B — serve static:

cd frontend
python -m http.server 5500
# open http://127.0.0.1:5500

Configuration

.env variables:

AQICN_TOKEN — required

CACHE_MAX_ENTRIES — default 256

CACHE_TTL_SECONDS — default 300

Notes and suggestions

For production, protect the token and restrict CORS.

To scale cache across instances, replace in-memory cache with Redis.


License

MIT


---

# 5) One-commit push (if you haven’t committed yet)
If you want the repo to show **one commit** that contains the entire project structure (as requested), run these commands from project root:

```bash
git init
git add .
git commit -m "Initial commit: AQI Search project (FastAPI backend + frontend)"
# add remote (replace username)
git remote add origin https://github.com/<USERNAME>/aqi-search.git
git branch -M main
git push -u origin main
