import requests
from bs4 import BeautifulSoup
import openai
import newsapi
from newsapi import NewsApiClient
from datetime import datetime

# Set your OpenAI API key
openai.api_key = "****"

# Set your NewsAPI key
newsapi = NewsApiClient(api_key='*****')

# Analyze the sentiment of a piece of text using the OpenAI API
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

# Fetch news articles using NewsAPI
from datetime import datetime, timedelta

def fetch_articles(keyword):
    response = newsapi.get_everything(q=keyword,
                                       from_param='2023-03-01T00:00:00',
                                       to=datetime.today().strftime('%Y-%m-%d'),
                                       language='en',
                                       sort_by='relevancy',
                                       page_size=100)

    articles = response['articles']
    return articles



# Analyze the sentiment of each article and summarize the week's news
def analyze_articles(keyword):
    articles = fetch_articles(keyword)
    num_articles = len(articles)
    total_sentiment = 0
    summary = ''

    for i, article in enumerate(articles):
        title = article['title']
        content = article['content']
        if content is None:
            content = article['description']

        sentiment = analyze_sentiment(content)
        rating = int(sentiment.split(' ')[0])
        text = sentiment[sentiment.find(':')+2:]

        summary += f"\n{i+1}/{num_articles}\nTitle: {title}\nText: {text}\nRating: {rating}\n"

        total_sentiment += rating

    avg_sentiment = total_sentiment / num_articles
    summary += f"\n\nAverage sentiment score: {avg_sentiment}"
    
    return summary

# Print the summary of the week's news

print(analyze_articles('bitcoin'))
