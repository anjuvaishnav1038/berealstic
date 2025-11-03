import requests

def web_search(query: str):
    """
    Performs a simple web search using DuckDuckGo's Instant Answer API.
    Returns a short text summary if available.
    """
    print(f"Searching web for: {query}")
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_redirect": "1", "no_html": "1"}
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data.get("AbstractText"):
            return data["AbstractText"]
        elif data.get("RelatedTopics"):
            for topic in data["RelatedTopics"]:
                if isinstance(topic, dict) and "Text" in topic:
                    return topic["Text"]

        return "No relevant web data found."
    except Exception as e:
        print(" Web search error:", e)
        return "Web search unavailable at the moment."

