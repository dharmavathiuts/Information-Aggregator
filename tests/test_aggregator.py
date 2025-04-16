import unittest
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from api_client.NewsAPIClient import NewsAPIClient
from api_client.WeatherAPIClient import WeatherAPIClient
from web_scraper.scraper import OnThisDayScraper
from data_processor.processor import InformationAggregator

class TestNewsAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = NewsAPIClient("ba51b60d91964d2099fef0150aa4b076")

    def test_top_headlines(self):
        data = self.client.get_top_headlines(country="us", category="technology")
        self.assertIsNotNone(data)
        self.assertIn("articles", data)

class TestWeatherAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = WeatherAPIClient("ef8b843e8e4ba7daab6a544bced98daf")

    def test_get_weather(self):
        data = self.client.get_weather("London")
        self.assertIsNotNone(data)
        self.assertIn("weather", data)

class TestOnThisDayScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = OnThisDayScraper()

    def test_get_events(self):
        events = self.scraper.get_on_this_day_events()
        self.assertIsInstance(events, list)
        self.assertGreater(len(events), 0)

class TestInformationAggregator(unittest.TestCase):
    def setUp(self):
        self.aggregator = InformationAggregator("London", "us", "technology")

    def test_aggregate_info(self):
        info = self.aggregator.aggregate_info()
        self.assertIn("weather", info)
        self.assertIn("news", info)
        self.assertIn("on_this_day", info)

if __name__ == "__main__":
    unittest.main()
