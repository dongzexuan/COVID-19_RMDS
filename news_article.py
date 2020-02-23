import requests
import pandas as pd
from scraper.newsapi import newsapi_summaries
from scraper.google_news_scrape import scrape_news_summaries

# use newsapi
# articles = newsapi_summaries('covid')

# use scraper
kw = 'covid-19'
cities = ['beijing', 'wuHan']
articles = []
for city in cities:
    q = kw + ' ' + city
    articles += scrape_news_summaries(q, city)

df = pd.DataFrame(data=articles)
df.to_csv('news_article.csv', index=False)