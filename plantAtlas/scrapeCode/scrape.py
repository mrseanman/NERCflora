import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

def getAccounts(species):
    urlStub = 'https://www.brc.ac.uk/plantatlas/plant/'
    formattedSpecies = species.lower()
    formattedSpecies = formattedSpecies.replace('sens.', 's')
    formattedSpecies = formattedSpecies.replace('lat.', 'l')
    formattedSpecies = formattedSpecies.replace('p.x', 'p-x')
    formattedSpecies = formattedSpecies.replace(' .x', '-x')
    formattedSpecies = formattedSpecies.replace('subsp.', 'subsp ')
    formattedSpecies = formattedSpecies.replace(' ', '-')
    formattedSpecies = formattedSpecies.replace('(', '')
    formattedSpecies = formattedSpecies.replace(')', '')
    formattedSpecies = formattedSpecies.replace('.', '')

    url = urlStub+formattedSpecies
    r = requests.get(url)

    ecology = ''
    status = ''
    trends = ''
    worldDist = ''

    if r.status_code == 200:
        soup = bs(r.text, features='lxml')
        panes = soup.find_all(class_="pane-content")
        text = panes[0].text

        ecology = subStr(text, '  Ecology  ', '  Status  ')
        status = subStr(text, '  Status  ', '  Trends  ')
        trends = subStr(text, '  Trends  ', '  World Distribution  ')
        worldDist = subStr(text, '  World Distribution  ', 'Link to interactive map')

        ecology = ecology.strip()
        status = status.strip()
        trends = trends.strip()
        worldDist = worldDist.strip()
        worldDist = worldDist.replace("\n", "")
    return ecology, status, trends, worldDist


def subStr(str, start, end):
    startNum = str.find(start)
    endNum = str.find(end)
    return str[startNum+len(start):endNum]

df = pd.read_csv('/home/sean/NERCflora/plantAtlas/raw/PLANTATT_19_Nov_08.csv', sep='|')

totalRows = len(df['species'])
badUrls = []

dfScrape = pd.DataFrame({'species':[],'ecology':[], 'status':[],'trends':[], 'world distribution':[]})

for index, row in df.iterrows():

    species = row['species']
    ecology, status, trends, worldDist = getAccounts(species)
    dfScrape = dfScrape.append({'species':species ,
                'ecology':ecology,
                'status':status,
                'trends':trends,
                'world distribution':worldDist},
                ignore_index=True)
    print(species)
    print(float(index)/float(totalRows))
