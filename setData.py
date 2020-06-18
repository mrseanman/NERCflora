import pandas as pd
import numpy as np
import pprint as pp
import statistics as stat


def filterIn(values, test):
    if type(values)==str:
        test = list(test)
        return [x for x in test if x in values] != []
    else:
        return False
vFilter = np.vectorize(filterIn, excluded=['test'])

print("\nThe available dfs are:\necoFlora\nplantAt\ngenFlora\n")
searchStrings=[
'fertil',
'selfing',
'self fert',
'outcross'
]
#ecoFlora ids with data
ecoFlora = pd.read_csv('/home/sean/NERCflora/ecoFlora/dataFlat.csv', sep='|')
ecoSynonyms = pd.read_csv('/home/sean/NERCflora/ecoFlora/ids/idsWithData.csv')
genFlora = pd.read_csv('/home/sean/NERCflora/geneticFlora/data.csv', sep='|')
plantAt = pd.read_csv('/home/sean/NERCflora/plantAtlas/data.csv', sep='|')
