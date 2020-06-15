import requests
import pandas as pd


def save_table(url, name):
    dir = '/home/sean/NERC/ecoFloraScrape/data/'
    r = requests.get(url)
    dfs = pd.read_html(r.text)
    if len(dfs) > 0:
        saveName = dir+name+'.csv'
        dfs[0].to_csv(saveName)


def main():
    synonyms = pd.read_csv('/home/sean/NERC/ecoFloraScrape/ids.csv')
    total = synonyms['species'].size
    for index, row in synonyms.iterrows():
        url = 'http://ecoflora.org.uk/search_ecochars.php?plant_no=' + str(row['id'])
        save_table(url, str(row['species']))
        print(float(index)/float(total))

main()
