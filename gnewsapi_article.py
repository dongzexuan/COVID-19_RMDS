import requests
import pandas as pd
from scraper.newsapi import gnewsapi_summaries
from scraper.google_news_scrape import scrape_news_summaries


def get_query(q, city):
    if type(q) == type([]):
        query = ' '.join(q + [city])
    elif type(q) == type('string'):
        query = q + ' ' + city
    else:
        query = 'error'
    return query


def get_city(cities):
    if type(cities) == type([]):
        pass
    elif type(cities) == type('string'):
        cities = cities.split(',')
    else:
        cities = 'error'
    return cities


# use newsapi
def use_gnews_api(kw, cities, articles):
    city_list = get_city(cities)
    for city in city_list:
        query = get_query(kw, city)
        articles += gnewsapi_summaries(query)
    df = pd.DataFrame(data=articles)
    df.to_csv('gnews_article.csv', index=False)


# use scraper
def use_scraper(kw, cities, articles):
    for city in cities:
        q = kw + ' ' + city
        articles += scrape_news_summaries(q, city)

    df = pd.DataFrame(data=articles)
    df.to_csv('news_article.csv', index=False)

kw = 'covid-19'
# cities = ['beijing', 'wuHan']
cities = 'beijing, wuHan'

articles = []

use_gnews_api(kw, cities, articles)
