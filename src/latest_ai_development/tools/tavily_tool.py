import os
from tavily import TavilyClient

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=TAVILY_API_KEY)

def tavily_search(query: str, max_results: int = 5):
    response = client.search(
        query=query,
        max_results=max_results,
        include_answer=True,
        include_raw_content=False
    )
    return response
