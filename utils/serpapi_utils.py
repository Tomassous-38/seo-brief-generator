from serpapi.google_search_results import GoogleSearch

def get_google_search_results(query, api_key, num_results=3):
    params = {
        "q": query,
        "api_key": api_key,
        "num": num_results
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    urls = []
    for result in results.get("organic_results", [])[:num_results]:
        urls.append(result.get("link"))
    return urls
