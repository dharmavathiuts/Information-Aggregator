import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from api_client.NewsAPIClient import NewsAPIClient
from web_scraper.scraper import WebScraper
from data_processor.processor import DataProcessor
from visualization.visualizer import visualize_article_sources

class AggregatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("News Aggregator")
        self.geometry("1000x600")
        
        # Set up backend components
        self.api_key = "ba51b60d91964d2099fef0150aa4b076"  
        self.client = NewsAPIClient(self.api_key)
        self.scraper = WebScraper(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
        self.processor = DataProcessor(self.scraper)
        self.articles = []  # Will store processed articles

        # Set up GUI components
        self.create_widgets()
    
    def create_widgets(self):
        # Frame for control buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        load_btn = ttk.Button(btn_frame, text="Load Articles", command=self.load_articles)
        load_btn.pack(side=tk.LEFT, padx=5)

        vis_btn = ttk.Button(btn_frame, text="Visualize Sources", command=self.visualize_sources)
        vis_btn.pack(side=tk.LEFT, padx=5)

        # Listbox for article titles on the left
        self.article_list = tk.Listbox(self, height=25, width=40)
        self.article_list.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.article_list.bind("<<ListboxSelect>>", self.on_article_select)
        
        # ScrolledText for displaying article content on the right
        self.content_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=60)
        self.content_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def load_articles(self):
        try:
            # Fetch top headlines (you can adjust parameters as needed)
            api_response = self.client.get_top_headlines(country="us", category="technology")
            if not api_response:
                messagebox.showerror("Error", "Failed to fetch articles from API.")
                return
            # Process articles using the data processor
            self.articles = self.processor.process(api_response)
            
            # Populate the listbox with article titles
            self.article_list.delete(0, tk.END)
            for article in self.articles:
                title = article.get("title", "No Title")
                self.article_list.insert(tk.END, title)
            
            messagebox.showinfo("Info", "Articles loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def on_article_select(self, event):
        # Display the full content of the selected article
        selected_indices = self.article_list.curselection()
        if selected_indices:
            index = selected_indices[0]
            article = self.articles[index]
            content = article.get("full_content", "No content available.")
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, content)

    def visualize_sources(self):
        # Visualize the distribution of articles by source using the visualization module
        if self.articles:
            visualize_article_sources(self.articles)
        else:
            messagebox.showinfo("Info", "Please load articles first.")

if __name__ == "__main__":
    app = AggregatorGUI()
    app.mainloop()
