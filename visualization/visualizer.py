import matplotlib.pyplot as plt

def visualize_news_sources(news_data):
    """
    Plots a horizontal bar chart of news sources and the number of articles.
    """
    if not news_data or not news_data.get("articles"):
        print("No news data available for visualization.")
        return

    sources_count = {}
    for article in news_data["articles"]:
        source = article.get("source", {}).get("name", "Unknown")
        sources_count[source] = sources_count.get(source, 0) + 1

    sources = list(sources_count.keys())
    counts = list(sources_count.values())

    plt.figure(figsize=(10, 6))
    plt.barh(sources, counts, color="#1976d2")
    plt.xlabel("Number of Articles")
    plt.title("News Sources Distribution")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # For demonstration purposes
    sample_news_data = {
        "articles": [
            {"source": {"name": "CNN"}, "title": "Article 1"},
            {"source": {"name": "BBC"}, "title": "Article 2"},
            {"source": {"name": "CNN"}, "title": "Article 3"},
            {"source": {"name": "Reuters"}, "title": "Article 4"}
        ]
    }
    visualize_news_sources(sample_news_data)
