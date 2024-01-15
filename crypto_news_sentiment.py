import requests
from bs4 import BeautifulSoup
import openai
from newsapi import NewsApiClient
from datetime import datetime

# Set your OpenAI API key.
openai.api_key = "YOUR_OPENAI_API_KEY"

# Set your NewsAPI key
newsapi = NewsApiClient(api_key='YOUR_NEWSAPI_KEY')

def analyze_sentiment(text):
    prompt = f"Analyze the sentiment of the following text related to Bitcoin and cryptocurrencies:\n\n{text}\n\nSentiment:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=20,
        n=1,
        stop=None,
        temperature=0.5,
    )
    sentiment = response.choices[0].text.strip()
    return sentiment

def fetch_articles(keyword):
    response = newsapi.get_everything(
        q=keyword,
        from_param='2023-03-01T00:00:00',
        to=datetime.today().strftime('%Y-%m-%d'),
        language='en',
        sort_by='relevancy',
        page_size=100
    )
    articles = response['articles']
    return articles

def analyze_articles(keyword):
    articles = fetch_articles(keyword)
    num_articles = len(articles)
    total_sentiment = 0
    summary = ''

    for i, article in enumerate(articles):
        title = article['title']
        content = article['content'] if article['content'] is not None else article['description']

        sentiment = analyze_sentiment(content)
        rating = int(sentiment.split(' ')[0])
        text = sentiment[sentiment.find(':')+2:]

        summary += f"\n{i+1}/{num_articles}\nTitle: {title}\nText: {text}\nRating: {rating}\n"

        total_sentiment += rating

    avg_sentiment = total_sentiment / num_articles
    summary += f"\n\nAverage sentiment score: {avg_sentiment}"
    return summary, avg_sentiment

def generate_pine_script(description, sentiment_score):
    prompt = (f"Generate a Pine Script for a MACD trading strategy on TradingView. "
              f"The strategy should adjust its sensitivity based on the following sentiment score: {sentiment_score}. "
              f"Higher sentiment scores should result in a more aggressive strategy, while lower scores in a more conservative one.\n\n"
              f"Description: {description}\n\nPine Script Code:")
    try:
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    pine_script = response.choices[0].text.strip()
    return pine_script
except Exception as e: return f"An error occurred: {e}"
def main():
keyword = 'bitcoin'
summary, avg_sentiment = analyze_articles(keyword)
print(summary) description = "MACD strategy for Bitcoin trading."
pine_script_code = generate_pine_script(description, avg_sentiment)
print("Generated Pine Script based on Sentiment:\n", pine_script_code) if name == "main":
main()