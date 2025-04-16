import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from api_client.NewsAPIClient import NewsAPIClient
from api_client.WeatherAPIClient import WeatherAPIClient
from web_scraper.scraper import OnThisDayScraper

class InformationAggregator:
    """
    Aggregates information from news, weather, and "On This Day" events.
    """
    def __init__(self, city, country, news_category):
        self.city = city
        self.country = country
        self.news_category = news_category
        self.news_client = NewsAPIClient("ba51b60d91964d2099fef0150aa4b076")
        self.weather_client = WeatherAPIClient("ef8b843e8e4ba7daab6a544bced98daf")
        self.on_this_day_scraper = OnThisDayScraper()

    def aggregate_info(self):
        info = {}
        # Weather info
        weather_data = self.weather_client.get_weather(self.city)
        if weather_data:
            desc = weather_data["weather"][0]["description"]
            temp = weather_data["main"]["temp"]
            info["weather"] = f"Weather in {self.city}: {desc}, {temp}°C"
        else:
            info["weather"] = "Weather data not available."

        # News info: try top-headlines first, then fallback to global 'everything'
        news_data = self.news_client.get_top_headlines(country=self.country, category=self.news_category)
        if not (news_data and news_data.get("articles")):
            # Fallback: use the global "everything" endpoint using the news category as query
            news_data = self.news_client.get_everything(query=self.news_category)
        if news_data and news_data.get("articles"):
            articles = news_data["articles"]
            headlines = [article["title"] for article in articles[:5]]
            info["news"] = "Top News Headlines:\n" + "\n".join(headlines)
            info["news_data"] = news_data  # For visualization
        else:
            info["news"] = "News data not available."
            info["news_data"] = None

        # On This Day events
        events = self.on_this_day_scraper.get_on_this_day_events()
        if events:
            info["on_this_day"] = "On This Day:\n" + "\n".join(events)
        else:
            info["on_this_day"] = "No events found."

        return info

if __name__ == "__main__":
    city = input("Enter city: ") or "London"
    country = input("Enter country code (e.g., us, gb, de, fr): ") or "us"
    category = input("Enter news category (e.g., general, business, entertainment, health, science, sports, technology): ") or "technology"
    aggregator = InformationAggregator(city, country, category)
    aggregated_info = aggregator.aggregate_info()
    for key, value in aggregated_info.items():
        print(f"{key.upper()}:")
        print(value)
        print("-" * 40)
