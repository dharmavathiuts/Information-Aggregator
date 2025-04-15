import requests

class NewsAPIClient:
    """
    A client for interacting with NewsAPI.org to fetch headlines and articles.
    """
    BASE_URL = "https://newsapi.org/v2/"

    def __init__(self, api_key):
        """
        Initialize the NewsAPIClient with an API key.

        :param api_key: Your NewsAPI API key as a string.
        """
        self.api_key = api_key

    def get_top_headlines(self, country="us", category=None, query=None, page_size=20):
        """
        Fetch top headlines based on given parameters.

        :param country: The 2-letter country code (default is "us").
        :param category: News category (e.g., 'technology', 'sports') if applicable.
        :param query: Keywords or a search query.
        :param page_size: Number of results to return per page.
        :return: A dictionary parsed from the JSON response containing news data.
        """
        url = f"{self.BASE_URL}top-headlines"
        params = {
            "apiKey": self.api_key,
            "country": country,
            "pageSize": page_size,
        }

        if category:
            params["category"] = category
        if query:
            params["q"] = query

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            return None

    def get_everything(self, query, page_size=20):
        """
        Fetch all available articles that match the query.

        :param query: Keywords or search terms.
        :param page_size: Number of articles to return per page.
        :return: A dictionary parsed from the JSON response containing news articles.
        """
        url = f"{self.BASE_URL}everything"
        params = {
            "apiKey": self.api_key,
            "q": query,
            "pageSize": page_size,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            return None


if __name__ == "__main__":
    # Use your provided API key directly (for testing purposes).
    api_key = "apiba51b60d91964d2099fef0150aa4b076"
    client = NewsAPIClient(api_key)
    
    # Example: Fetch top headlines in the technology category.
    headlines = client.get_top_headlines(country="us", category="technology")
    if headlines:
        print("Top Technology Headlines:")
        for article in headlines.get("articles", []):
            print(f"- {article.get('title')}")
