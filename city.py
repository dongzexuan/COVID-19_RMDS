import pandas as pd
import numpy as np
from datetime import datetime

# Create a DataFrame
df1 = {
    'Subject': ['semester1', 'semester2', 'semester3', 'semester4', 'semester1',
                'semester2', 'semester3'],
    'Score': [62, 47, 55, 74, 31, 77, 85]}
df2 = {
    'Subject': ['semester4', 'semester1',
                'semester2', 'semester3'],
    'Score': [74, 31, 79, 85]}
df1 = pd.DataFrame(df1,columns=['Subject','Score'])
df1.insert(0, 'aaa', df1.Score)

url_china = 'https://raw.githubusercontent.com/BlankerL/DXY-COVID-19-Data/master/csv/DXYArea.csv'
china_df = pd.read_csv(url_china)
last_loc = china_df.loc[(china_df['provinceEnglishName'] == 'Chongqing') & (china_df['updateTime'] == '2020-03-15 11:37:10.875')].index[0]
china_df = china_df.iloc[last_loc+1:,:]
print(datetime.now().strftime("%m-%d-%Y-%H-%M-%S"))
df2 = pd.DataFrame(df2,columns=['Subject','Score'])
set_diff_df = pd.concat([df2, df1]).drop_duplicates(keep=False)
df3 = pd.DataFrame()
print(set_diff_df)