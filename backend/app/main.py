import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import httpx
from .cache_store import CacheStore
from .schemas import AQIResponse

load_dotenv()
AQICN_TOKEN =os.getenv("AQICN_TOKEN")
CACHE_MAX = int(os.getenv("CACHE_MAX_ENTRIES", "256"))
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "300"))

cache = CacheStore(max_entries=CACHE_MAX, ttl_seconds=CACHE_TTL)

app = FastAPI(title="AQI Search Service", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AQICN_BASE = "https://api.waqi.info/feed/{city}/?token={token}"

async def fetch_vendor(city: str):
    url = AQICN_BASE.format(city=city, token=AQICN_TOKEN)
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url)
        return resp.json()

@app.get("/api/aqi", response_model=AQIResponse)
async def get_aqi(city: str = Query(..., min_length=1)):
    key = city.strip().lower()
    cached = cache.get(key)
    if cached:
        cached["source_status"] = "cache"
        return cached

    if not AQICN_TOKEN:
        raise HTTPException(500, "AQICN_TOKEN missing")

    vendor = await fetch_vendor(city)

    if vendor.get("status") != "ok":
        raise HTTPException(404, str(vendor.get("data")))

    data = vendor.get("data", {})

    response_obj = {
        "source_status": "vendor",
        "city": {
            "name": data.get("city", {}).get("name"),
            "url": data.get("city", {}).get("url"),
            "geo": data.get("city", {}).get("geo"),
        },
        "aqi": data.get("aqi"),
        "dominentpol": data.get("dominentpol"),
        "iaqi": data.get("iaqi"),
        "time": data.get("time", {}).get("s"),
        "raw_vendor_response": data
    }

    cache.set(key, response_obj)
    return response_obj

@app.get("/api/_cache/info")
def cache_info():
    return cache.info()

@app.post("/api/_cache/clear")
def cache_clear():
    cache.clear()
    return {"status": "cleared"}