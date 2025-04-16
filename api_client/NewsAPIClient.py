import requests

class NewsAPIClient:
    """
    A client for interacting with NewsAPI.org to fetch headlines and articles.
    """
    BASE_URL = "https://newsapi.org/v2/"
    
    def __init__(self, api_key):
        self.api_key = api_key

    def get_top_headlines(self, country="us", category=None, query=None, page_size=20):
        url = f"{self.BASE_URL}top-headlines"
        params = {
            "apiKey": self.api_key,
            "country": country,
            "pageSize": page_size
        }
        if category:
            params["category"] = category
        if query:
            params["q"] = query

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching news: {response.status_code} - {response.text}")
            return None

    def get_everything(self, query, page_size=20):
        url = f"{self.BASE_URL}everything"
        params = {
            "apiKey": self.api_key,
            "q": query,
            "pageSize": page_size,
            "sortBy": "publishedAt"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching global news: {response.status_code} - {response.text}")
            return None

if __name__ == "__main__":
    API_KEY = "ba51b60d91964d2099fef0150aa4b076"
    client = NewsAPIClient(API_KEY)
    country = input("Enter country code (e.g., us, gb, de, fr): ") or "us"
    category = input("Enter news category (e.g., business, entertainment, general, health, science, sports, technology): ") or "technology"
    headlines = client.get_top_headlines(country=country, category=category)
    if headlines and headlines.get("articles"):
        print(f"Top {category.capitalize()} Headlines for {country.upper()}:")
        for article in headlines.get("articles", []):
            print(f"- {article.get('title')}")
    else:
        print(f"No top headlines found for {country.upper()} and {category}.")
        # Optionally fallback to global news:
        headlines_global = client.get_everything(query=category)
        if headlines_global and headlines_global.get("articles"):
            print(f"Global {category.capitalize()} Headlines:")
            for article in headlines_global.get("articles", [])[:5]:
                print(f"- {article.get('title')}")
        else:
            print("No articles found globally either.")
