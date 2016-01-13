'''This module scrape heroes' attributes from website'''

import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

url = 'http://dota2.gamepedia.com/Table_of_hero_attributes'
d2 = requests.get(url)
soup = BeautifulSoup(d2.content)
table = soup.find('table', attrs={'class': 'wikitable'})
headings = [th.get_text().strip() for th in table.find("tr").find_all("th")]
datasets = []
att = []

for row in table.find_all("tr")[1:]:
    datasets.append([td.get_text().strip() for td in row.find_all("td")])

    for td in row.find_all('td')[1:2]:
        for a in td.find_all('a'):
            att.append(a['title'])

datasets_np = np.array(datasets)
datasets_np = np.array(datasets)
datasets_np[:, 1] = att
df = pd.DataFrame(datasets_np, columns=headings)
# Arc Warden is not in the patch I studied
# df = df[df['HERO'] != 'Arc Warden']
df.to_csv('file/hero_attributes', sep='t')
