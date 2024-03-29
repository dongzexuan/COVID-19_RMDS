import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from random import randint


def scrape_news_summaries(s, location):
    time.sleep(randint(0, 2))  # setup a limit
    s = s + ' ' + location
    r = requests.get("http://www.google.com/search?q="+s+"&tbm=nws")
    content = r.content
    news_summaries = []
    soup = BeautifulSoup(content, "html.parser")
    st_divs = soup.findAll("div", {"class": "ZINbbc xpd O9g5cc uUPGi"})

    for st_div in st_divs:
        source = st_div.find("div", {"class": "BNeawe UPmit AP7Wnd"}).text
        title = st_div.find("div", {"class": "BNeawe vvjwJb AP7Wnd"}).text
        url = st_div.find('a').attrs['href'].replace('/url?q=', '').split('&')[0]

        publishtime = st_div.find("div", {"class": "BNeawe s3v9rd AP7Wnd"}).text.split(' · ')[0]
        content = st_div.find("div", {"class": "BNeawe s3v9rd AP7Wnd"}).text.split(' · ')[1]
        record = {'source': source,
                  'title': title,
                  'content': content,
                  'url': url,
                  'publishTime': publishtime,
                  }
        news_summaries.append(record)
    return news_summaries, len(news_summaries)


def scrape_fbcad(idlist, classCD):
    # idlist = ['R407361']
    data = []
    for RefID in idlist:
        time.sleep(randint(0, 2))  # setup a limit
        url = "https://esearch.fbcad.org/Property/View/" + RefID

        try:
            df_list = pd.read_html(url)
            grade = df_list[3]["Class CD"][0]
            if grade == classCD:
                deed_df = df_list[6].dropna(subset=['Grantor'])
                builder = deed_df['Grantor'].tolist()[-1]
                new_row = [RefID, builder, url]
                data.append((new_row))
        except:
            continue

    return data

