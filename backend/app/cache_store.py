from cachetools import TTLCache
from typing import Optional
import threading

class CacheStore:
    def __init__(self, max_entries: int = 256, ttl_seconds: int = 300):
        self._cache = TTLCache(maxsize=max_entries, ttl=ttl_seconds)
        self._lock = threading.RLock()

    def get(self, key: str):
        with self._lock:
            return self._cache.get(key)

    def set(self, key: str, value):
        with self._lock:
            self._cache[key] = value

    def clear(self):
        with self._lock:
            self._cache.clear()

    def info(self):
        with self._lock:
            return {
                "curr_size": len(self._cache),
                "max_size": self._cache.maxsize,
                "ttl": self._cache.ttl
            }