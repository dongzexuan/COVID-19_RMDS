from bs4 import BeautifulSoup, element
import time
import pandas as pd

from scraper.google_news_scrape import scrape_fbcad

file = 'cincoranch.csv'
keep_col = ['QUICKREFID', 'OADDR1', 'TOTALVALUE', 'LANDVALUE', 'IMPVALUE', 'YEARBUILT', 'LANDSIZEFT', 'TOTSQFTLVG']
grade = "RG2"

all_property = pd.read_csv(file)
filtered = all_property[keep_col]
print("total numbers: ", len(filtered))
idlist = filtered['QUICKREFID'][:20]
data = scrape_fbcad(idlist, grade)
columns = ['QUICKREFID', 'Builder', 'Link']
df = pd.DataFrame(data, columns=columns)
combine_df = pd.merge(filtered, df, on=["QUICKREFID"])
combine_df['Unit_price'] = combine_df['IMPVALUE']/combine_df['TOTSQFTLVG']
combine_df.to_excel('RG2_properties2.xlsx', index=False)
