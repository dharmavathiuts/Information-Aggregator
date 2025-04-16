import requests
from bs4 import BeautifulSoup

class OnThisDayScraper:
    """
    Scrapes "On This Day" events from Wikipedia's main page.
    """
    def __init__(self, url="https://en.wikipedia.org/wiki/Main_Page"):
        self.url = url

    def get_on_this_day_events(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            events = soup.select("#mp-otd ul li")
            event_texts = [event.get_text(strip=True) for event in events[:5]]
            return event_texts
        else:
            print(f"Error fetching events: {response.status_code}")
            return []

if __name__ == "__main__":
    scraper = OnThisDayScraper()
    events = scraper.get_on_this_day_events()
    for ev in events:
        print(ev)
