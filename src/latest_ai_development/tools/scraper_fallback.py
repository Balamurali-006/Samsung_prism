import requests
from bs4 import BeautifulSoup

def fallback_scrape(url: str, timeout: int = 10) -> str:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts & styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    clean_text = " ".join(text.split())

    return clean_text
