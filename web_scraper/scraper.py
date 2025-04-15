import requests
from bs4 import BeautifulSoup

class WebScraper:
    """
    A web scraper using BeautifulSoup to extract article content.
    """
    def __init__(self, user_agent=None):
        self.headers = {"User-Agent": user_agent} if user_agent else {}

    def fetch_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Error fetching page. Status code: {response.status_code}")
        except Exception as e:
            print("Exception occurred while fetching the page:", e)
        return None

    def extract_article_content(self, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            article_tag = soup.find('article')
            paragraphs = article_tag.find_all('p') if article_tag else soup.find_all('p')
            content = "\n".join([para.get_text().strip() for para in paragraphs if para.get_text().strip()])
            return content
        except Exception as e:
            print("Exception occurred during HTML parsing:", e)
            return ""

    def scrape_article(self, url):
        html = self.fetch_page(url)
        if html:
            return self.extract_article_content(html)
        return None

if __name__ == "__main__":
    scraper = WebScraper(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    test_url = "https://www.pushsquare.com/news/2025/04/ps5-price-increases-announced-by-sony-affect-uk-europe-and-more"  # a valid article URL from your API output
    article_content = scraper.scrape_article(test_url)
    if article_content:
        print("Article content extracted (first 1000 characters):")
        print(article_content[:1000])
    else:
        print("Failed to extract article content.")
