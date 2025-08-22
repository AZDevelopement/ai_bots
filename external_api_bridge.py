
import requests
from bs4 import BeautifulSoup
import feedparser

# Replace with your actual NewsAPI key
NEWS_API_KEY = "your_newsapi_key"

def fetch_newsapi_headlines(query="stocks", count=5):
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&pageSize={count}&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        return [article["title"] for article in data.get("articles", [])]
    except Exception as e:
        print("❌ NewsAPI fetch failed:", e)
        return []

def fetch_finviz_headlines():
    try:
        url = "https://finviz.com/news.ashx"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        return [a.text for a in soup.find_all("a", class_="nn-tab-link")][:10]
    except Exception as e:
        print("❌ Finviz fetch failed:", e)
        return []

def fetch_sec_filings(cik="0000320193"):  # Example: Apple Inc.
    try:
        url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=&dateb=&owner=exclude&count=10&output=atom"
        feed = feedparser.parse(url)
        return [entry["title"] for entry in feed.entries]
    except Exception as e:
        print("❌ SEC feed fetch failed:", e)
        return []

if __name__ == "__main__":
    print("📡 Testing External API Bridge...\n")
    print("📰 NewsAPI:", fetch_newsapi_headlines())
    print("🧠 Finviz:", fetch_finviz_headlines())
    print("📄 SEC:", fetch_sec_filings())
