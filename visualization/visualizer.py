import matplotlib.pyplot as plt
from collections import Counter

def visualize_article_sources(processed_articles):
    """
    Creates a bar chart showing the distribution of articles by news source.

    :param processed_articles: List of article dictionaries.
           Each article is expected to have a "source" key with a sub-key "name".
    """
    # Extract the news source names from the articles
    sources = [article.get("source", {}).get("name", "Unknown") for article in processed_articles]
    
    # Count the occurrences of each source using Counter
    source_counts = Counter(sources)
    
    # Debug: Print the computed counts (optional)
    print("Article Counts per Source:", source_counts)
    
    # Create a bar chart using matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(source_counts.keys(), source_counts.values(), color='skyblue')
    plt.xlabel("News Sources")
    plt.ylabel("Number of Articles")
    plt.title("Distribution of Articles by Source")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # For testing purposes, use a simulated list of processed articles.
    # In practice, you'll obtain this list from your Data Processor.
    sample_articles = [
        {"source": {"name": "IGN"}, "title": "Article 1"},
        {"source": {"name": "My Nintendo News"}, "title": "Article 2"},
        {"source": {"name": "IGN"}, "title": "Article 3"},
        {"source": {"name": "CNET"}, "title": "Article 4"},
        {"source": {"name": "IGN"}, "title": "Article 5"},
        {"source": {"name": "Polygon"}, "title": "Article 6"},
        {"source": {"name": "CNET"}, "title": "Article 7"}
    ]
    visualize_article_sources(sample_articles)
