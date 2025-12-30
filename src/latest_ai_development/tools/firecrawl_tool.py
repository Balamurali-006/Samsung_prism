import os
import requests

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
FIRECRAWL_URL = "https://api.firecrawl.dev/v1/scrape"

def firecrawl_scrape(url: str):
    payload = {
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": True
    }

    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(FIRECRAWL_URL, json=payload, headers=headers, timeout=20)
    response.raise_for_status()

    return response.json()
