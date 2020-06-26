import pandas as pd
import numpy as np

def familyList(family):
    family = family.lower()
    dir = '/home/sean/NERCflora/plantList/' + family + '.csv'
    dfFamilyList = pd.read_csv(dir)

df = pd.read_csv('/home/sean/NERCflora/ecoFlora/dataFlat.csv', sep='|')

def inList(series, lst):
    ins = []
    for s in series:
        ins.append(s in lst)
    return np.array(ins)

def getFamilyDf(family):
    dirStub = '/home/sean/NERCflora/plantList/'
    dir = dirStub + family + '.csv'
    return pd.read_csv(dir)

#family list in /NERCflora/plantList
listOfFams = ['poaceae', 'brassicaceae', 'compositae', 'papaveraceae']
df['family'] = np.nan

for fam in listOfFams:
    familyDf = getFamilyDf(fam)
    genuss = familyDf['Genus'].str.lower().unique()
    df.loc[inList(df['genus'],genuss),'family']=fam
