import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import ttk, messagebox
from data_processor.processor import InformationAggregator
from visualization.visualizer import visualize_news_sources
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import io

# Allowed values for dynamic input
COUNTRIES = ["us", "gb", "de", "fr", "ca", "au", "in", "jp", "cn", "ke"]
NEWS_CATEGORIES = ["general", "business", "entertainment", "health", "science", "sports", "technology"]
# Cities per country for the weather (adjust as desired)
CITIES = {
    "us": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "gb": ["London", "Birmingham", "Manchester", "Liverpool", "Leeds"],
    "de": ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"],
    "fr": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"],
    "ca": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
    "au": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
    "in": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai"],
    "jp": ["Tokyo", "Osaka", "Nagoya", "Sapporo", "Fukuoka"],
    "cn": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu"],
    "ke": ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]
}

class AggregatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Information Aggregator")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f5f5f5")
        
        # Tabs for information and visualization
        self.tab_control = ttk.Notebook(root)
        self.info_tab = ttk.Frame(self.tab_control)
        self.visualization_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.info_tab, text="Information")
        self.tab_control.add(self.visualization_tab, text="Visualization")
        self.tab_control.pack(expand=True, fill="both")
        
        # Input for Information Tab
        ttk.Label(self.info_tab, text="Country:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.country_menu = ttk.Combobox(self.info_tab, values=COUNTRIES, state="readonly")
        self.country_menu.current(0)
        self.country_menu.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(self.info_tab, text="City:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.city_menu = ttk.Combobox(self.info_tab, state="readonly")
        self.city_menu.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(self.info_tab, text="News Category:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.category_menu = ttk.Combobox(self.info_tab, values=NEWS_CATEGORIES, state="readonly")
        self.category_menu.current(0)
        self.category_menu.grid(row=2, column=1, padx=10, pady=5)
        
        # Button to fetch aggregated info
        self.fetch_button = ttk.Button(self.info_tab, text="Get Aggregated Info", command=self.fetch_info)
        self.fetch_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        # Text widget to display results
        self.result_text = tk.Text(self.info_tab, wrap=tk.WORD, width=60, height=20, font=("Helvetica", 10), bg="#FFFFFF")
        self.result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Weather icon label
        self.weather_icon_label = ttk.Label(self.info_tab)
        self.weather_icon_label.grid(row=4, column=2, padx=10, pady=10)
        
        # Visualization area on Visualization Tab
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_tab)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")
        
        # Update city options based on country
        self.country_menu.bind("<<ComboboxSelected>>", self.update_city_menu)
        self.update_city_menu()

    def update_city_menu(self, event=None):
        country = self.country_menu.get()
        cities = CITIES.get(country, [])
        self.city_menu.config(values=cities)
        if cities:
            self.city_menu.set(cities[0])
        else:
            self.city_menu.set("")

    def fetch_info(self):
        city = self.city_menu.get().strip()
        country = self.country_menu.get().strip()
        category = self.category_menu.get().strip()
        if not city:
            messagebox.showerror("Input Error", "Please select a city.")
            return
        aggregator = InformationAggregator(city, country, category)
        info = aggregator.aggregate_info()
        output = (f"{info.get('weather','')}\n\n"
                  f"{info.get('news','')}\n\n"
                  f"{info.get('on_this_day','')}")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, output)
        self.update_weather_icon(info.get("weather_icon"))
        self.plot_news_sources(info.get("news_data"))

    def update_weather_icon(self, icon_code):
        from PIL import Image, ImageTk  # Import here to avoid issues if PIL is not used elsewhere
        if icon_code:
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            response = requests.get(icon_url)
            if response.status_code == 200:
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((80, 80), resample=Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.weather_icon_label.config(image=photo)
                self.weather_icon_label.image = photo
            else:
                self.weather_icon_label.config(text="No Icon")
        else:
            self.weather_icon_label.config(text="No Icon")

    def plot_news_sources(self, news_data):
        if news_data and news_data.get("articles"):
            self.ax.clear()
            sources_count = {}
            for article in news_data.get("articles", []):
                source = article.get("source", {}).get("name", "Unknown")
                sources_count[source] = sources_count.get(source, 0) + 1
            sources = list(sources_count.keys())
            counts = list(sources_count.values())
            self.ax.barh(sources, counts, color="#1976d2")
            self.ax.set_xlabel("Number of Articles")
            self.ax.set_title("News Sources Distribution")
            self.canvas.draw()
        else:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "No news data available", ha="center", va="center")
            self.canvas.draw()

def main():
    root = tk.Tk()
    app = AggregatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
