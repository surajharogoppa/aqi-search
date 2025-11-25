from pydantic import BaseModel
from typing import Optional, Dict, Any

class CityMeta(BaseModel):
    name: str
    url: Optional[str] = None
    geo: Optional[list] = None

class AQIResponse(BaseModel):
    source_status: str
    city: CityMeta
    aqi: Optional[int]
    dominentpol: Optional[str]
    iaqi: Optional[Dict[str, Any]]
    time: Optional[str]
    raw_vendor_response: Optional[Dict[str, Any]] = None