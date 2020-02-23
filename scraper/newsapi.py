import requests


def newsapi_summaries(q, start=None, sort=None):
    apikey = 'apiKey=4252de891ec04dd5bdb5554b8b7a9ad5'
    query = 'q=' + q + '&'
    url = 'http://newsapi.org/v2/top-headlines?' + query
    if start is not None:
        start = 'from=' + start + '&'
        url += start
    if sort is not None:
        sort = 'sortBy=' + sort + '&'
        url += sort
    url += apikey

    r = requests.get(url)
    articles = r.json()['articles']
    return articles
