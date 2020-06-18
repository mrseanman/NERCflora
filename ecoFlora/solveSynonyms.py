#this will solve the synonyms in the ecoFlora ids.
#method chosen is to scrape the <title> from the webpages

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import numpy as np

def getTitle(url):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    return soup.find(['title']).text

def main():
    #the url before the id
    urlStub = 'http://ecoflora.org.uk/search_species2.php?plant_no='
    idLoc = '/home/sean/NERCflora/ecoFlora/ids/ids.csv'
    df_ids = pd.read_csv(idLoc)
    ids = df_ids.id.unique()
    speciess = []

    numIds = len(ids)
    for index, id in enumerate(ids):
        url  = urlStub+str(id)
        species = getTitle(url)
        speciess.append(species)
        print(float(index)/float(numIds))

    d = {'id':ids, 'species':speciess}
    df = pd.DataFrame(d)
    df['species']=df['species'].str.lower()
    df['species']=df['species'].str.strip()
    df['species']=df['species'].str.replace(' ','_')
    df['species']=df['species'].str.replace('-','_')
    df['species']=df['species'].str.replace('.','')
    df.to_csv('idsNoSyn.csv')

main()
