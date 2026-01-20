import hashlib
import json
import os

CACHE_FILE = "cache.json"

def get_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)

    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

def clear_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        print(" Cache cleared")
    else:
        print("Cache is already empty")