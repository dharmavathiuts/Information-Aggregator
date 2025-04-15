import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from web_scraper.scraper import WebScraper
from api_client.NewsAPIClient import NewsAPIClient

class DataProcessor:
    """
    Processes and merges data from the News API and web scraper.
    """

    def __init__(self, scraper: WebScraper):
        """
        Initialize with an instance of the WebScraper.

        :param scraper: An instance of the WebScraper class.
        """
        self.scraper = scraper

    def merge_article_data(self, api_articles: list) -> list:
        """
        For each article from the API, fetch the full article content using the web scraper
        and add it as a new key in the article dictionary.

        :param api_articles: List of article dictionaries from the API.
        :return: List of article dictionaries with an added "full_content" field.
        """
        processed_articles = []
        for article in api_articles:
            url = article.get("url")
            # Scrape the full article content if URL is valid
            scraped_content = self.scraper.scrape_article(url) if url else None
            # Use scraped content if available; otherwise, fallback to API's "content" field if it exists
            article["full_content"] = scraped_content if scraped_content else article.get("content")
            processed_articles.append(article)
        return processed_articles

    def remove_duplicates(self, articles: list) -> list:
        """
        Remove duplicate articles based on the title.

        :param articles: List of article dictionaries.
        :return: List of unique articles.
        """
        seen_titles = set()
        unique_articles = []
        for article in articles:
            title = article.get("title")
            if title and title not in seen_titles:
                unique_articles.append(article)
                seen_titles.add(title)
        return unique_articles

    def process(self, api_response: dict) -> list:
        """
        Process the raw API response: merge article data and remove duplicates.

        :param api_response: Raw API response containing articles.
        :return: List of processed article dictionaries.
        """
        articles = api_response.get("articles", [])
        # Merge data from API with full article content from the web scraper
        merged_articles = self.merge_article_data(articles)
        # Remove duplicate articles
        unique_articles = self.remove_duplicates(merged_articles)
        return unique_articles


if __name__ == "__main__":
    # Example usage for testing the Data Processor module

    # Use your NewsAPI API key
    api_key = "ba51b60d91964d2099fef0150aa4b076"
    client = NewsAPIClient(api_key)
    
    # Fetch top headlines for a category (e.g., technology)
    api_response = client.get_top_headlines(country="us", category="technology")
    
    # Initialize the web scraper (set a common user agent)
    scraper = WebScraper(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    
    # Initialize DataProcessor with the scraper instance
    processor = DataProcessor(scraper)
    
    # Process the API response to merge and clean articles
    processed_articles = processor.process(api_response)
    
    # Display results: Print article title and first 200 characters of the full content for a quick check
    print("Processed Articles:")
    for article in processed_articles:
        title = article.get("title")
        content_snippet = article.get("full_content", "")[:200]  # show first 200 characters
        print(f"Title: {title}")
        print(f"Content Snippet: {content_snippet}")
        print("-" * 80)
