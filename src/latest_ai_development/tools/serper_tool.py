import os
import requests

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_URL = "https://google.serper.dev/search"

def serper_search(query: str, num_results: int = 5):
    payload = {
        "q": query,
        "num": num_results
    }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(SERPER_URL, json=payload, headers=headers, timeout=10)
    response.raise_for_status()

    return response.json()
