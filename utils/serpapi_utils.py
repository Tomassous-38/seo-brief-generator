from serpapi import GoogleSearch

def get_google_search_results(query, api_key, num_results=3):
    search = GoogleSearch({
        "q": query,
        "api_key": api_key
    })
    results = search.get_dict()
    urls = []
    for result in results.get("organic_results", [])[:num_results]:
        urls.append(result.get("link"))
    return urls
