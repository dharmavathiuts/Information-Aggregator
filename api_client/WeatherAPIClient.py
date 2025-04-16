import requests

class WeatherAPIClient:
    """
    A client for interacting with OpenWeatherMap to fetch current weather.
    """
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching weather: {response.status_code} - {response.text}")
            return None

if __name__ == "__main__":
    API_KEY = "ef8b843e8e4ba7daab6a544bced98daf"
    client = WeatherAPIClient(API_KEY)
    city = input("Enter city: ") or "London"
    data = client.get_weather(city)
    if data:
        print(data)
