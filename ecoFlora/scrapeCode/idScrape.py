import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

url = 'http://ecoflora.org.uk/search_synonyms.php'
r = requests.get(url)
soup = bs(r.text, 'html.parser')
links = soup.find_all('a')

rows = []
for link in links:
    row = []
    href = link['href']
    if "no=" in href:
        #gets the number after no= in the hlink
        synonym = link['href'].split('no=')[1]
        row.append(str(link.text))
        row.append(str(synonym))
        rows.append(row)

df = pd.DataFrame(np.array(rows), columns=['species', 'synonym'])
df.to_csv('synonyms.csv')
