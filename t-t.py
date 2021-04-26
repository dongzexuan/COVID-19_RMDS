from bs4 import BeautifulSoup, element
import time
import pandas as pd
from csv import DictWriter
import pprint
import datetime
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def init_driver(driver_type):
    if driver_type == 1:
        driver = webdriver.Firefox()
    elif driver_type == 2:
        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent = Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
        driver = webdriver.Chrome(chrome_options=options,
                                  executable_path=r'.\chromedriver.exe')
        # driver = webdriver.Chrome()
    elif driver_type == 3:
        driver = webdriver.Ie()
    elif driver_type == 4:
        driver = webdriver.Opera()
    elif driver_type == 5:
        driver = webdriver.PhantomJS()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def scroll(driver, start_date, words, lang, max_time=180):
    languages = { 1: 'en', 2: 'it', 3: 'es', 4: 'fr', 5: 'de', 6: 'ru', 7: 'zh'}
    url = "https://twitter.com/search?q="
    for w in words[:-1]:
        url += "{}%20".format(w)
    url += "{}%20".format(words[-1])
    url += "since%3A{}&".format(start_date)
    if lang != 0:
        url += "l={}&".format(languages[lang])
    url += "src=typd"
    print(url)
    driver.get(url)
    '''
    start_time = time.time()  # remember when we started
    while (time.time() - start_time) < max_time:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # print( str(time.time() - start_time) + " < " + str(max_time) )
    '''

def scrape_tweets(driver):
    try:
        tweet_divs = driver.page_source
        obj = BeautifulSoup(tweet_divs)
        content = obj.find_all("div", class_="content")
        # print(content)

        news_summaries = []
        for c in content[:10]:
            tweets = c.find("p", class_="tweet-text").strings
            tweet_text = "".join(tweets)
            tweet_text2 = c.find("p", class_="TweetTextSize js-tweet-text tweet-text").text.split('pic.twitter')[0]
            # content2 = "".join([t for t in tweet_text2.contents if type(t) == element.NavigableString]).strip()
            # print(tweet_text)
            # print("-----------")
            try:
                name = (c.find_all("strong", class_="fullname")[0].string).strip()
            except AttributeError:
                name = "Anonymous"
            date = (c.find_all("span", class_="_timestamp")[0].string).strip()
            url = 'https://twitter.com' + c.find('a', class_="tweet-timestamp").get('href')
            username = c.find_all("span", class_="username")[0].text
            try:
                img = c.find('div', class_='AdaptiveMedia-photoContainer').get('data-image-url')
            except:
                img = None
            actions = c.findAll('span', class_='ProfileTweet-actionCountForAria')
            n_comm = actions[0].text.split()[0]
            n_share = actions[1].text.split()[0]
            n_like = actions[2].text.split()[0]
            # print(tweet_text)
            record = {'tweet_url': url,
                      'name': name,
                      'username': username,
                      'published_date': date,
                      'tweet_description': tweet_text2,
                      'tweet_image': img,
                      'number_comments': n_comm,
                      'number_shares': n_share,
                      'number_likes': n_like,
                      }
            news_summaries.append(record)
        return news_summaries, len(news_summaries)
    except Exception as e:
        print("Something went wrong!")
        print(e)
        driver.quit()


def write_csv_header():
    with open("twitterData.csv", "w+") as csv_file:
        fieldnames = ['Date', 'Name', 'Tweets','Tags']
        writer = DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

def write_csv(date,tweet,name):
    with open("twitterData.csv", "a+") as csv_file:
        fieldnames = ['Date', 'Name', 'Tweets','Tags']
        writer = DictWriter(csv_file, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'Date': date,'Name': name,'Tweets': tweet})



def make_csv(data):
    l = len(data['date'])
    print("count: %d" % l)
    with open("twitterData.csv", "a+") as file:
        fieldnames = ['Date', 'Name', 'Tweets']
        writer = DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(l):
            writer.writerow({'Date': data['date'][i],
                            'Name': data['name'][i],
                            'Tweets': data['tweet'][i],
                            })


def get_all_dates(start_date, end_date):
    dates = []
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    step = timedelta(days=1)
    while start_date <= end_date:
        dates.append(str(start_date.date()))
        start_date += step

    return dates


def main():
    driver_type = 2#int(input("1) Firefox | 2) Chrome | 3) IE | 4) Opera | 5) PhantomJS\nEnter the driver you want to use: "))
    wordsToSearch = ['covid-19', 'south korea']#input("Enter the words: ").split(',')
    for w in wordsToSearch:
        w = w.strip()
    start_date = datetime.datetime.strftime(datetime.datetime.now() - timedelta(1), '%Y-%m-%d')#input("Enter the start date in (YYYY-MM-DD): ")
    end_date = '2020-03-07'#input("Enter the end date in (YYYY-MM-DD): ")

    lang = 1#int(input("0) All Languages 1) English | 2) Italian | 3) Spanish | 4) French | 5) German | 6) Russian | 7) Chinese\nEnter the language you want to use: "))
    '''
    all_dates = get_all_dates(start_date, end_date)
    print(all_dates)
    write_csv_header()
    for i in range(len(all_dates) - 1):
        driver = init_driver(driver_type)
        scroll(driver, str(all_dates[i]), str(all_dates[i + 1]), wordsToSearch, lang, max_time=0.2)
        articles, n = scrape_tweets(driver)
        df = pd.DataFrame(data=articles)
        time.sleep(5)
        print("The tweets for {} are ready!".format(all_dates[i]))
        driver.quit()
    '''
    driver = init_driver(driver_type)
    scroll(driver, start_date, wordsToSearch, lang, max_time=0.2)
    articles, n = scrape_tweets(driver)
    df = pd.DataFrame(data=articles)
    time.sleep(5)
    # print("The tweets for {} are ready!".format(all_dates[i]))
    driver.quit()


if __name__ == "__main__":
    main()