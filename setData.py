import pandas as pd
import numpy as np
import pprint as pp
import statistics as stat

def filterIn(values, test):
#returns truth value if test or any x in test is in value
#useful when numpy vectorized and used to filter dfs
    if type(values)==str:
        if type(test)==str:
            return test in values
        elif type(test)==list:
            return [x for x in test if x in values] != []
    else:
        return False
vFilter = np.vectorize(filterIn, excluded=['test'])

def filterUnique(values, test):
#returns thruth value if test is the only value present in values
#e.g. filterUnique(values='abc, abc', test='abc') returns True.
#but 'abc, abc'=='abc' returns False
    if type(values)==str:
        return ((test in values)
                and
                ([x for x in values.split(', ') if not(x==test)] == []))
    else:
        return False
vFilterUniq = np.vectorize(filterUnique)

searchStrings=[
'fertil',
'selfing',
'self fert',
'outcross'
]
#relating to ecoFlora['Fertilization']
allFert = [
'apomictic',
'cross and self',
'cross or automatic self',
'no seed produced in Britain',
'normally cross',
'normally self',
'obligatory cross',
'viviparous',
'insects',
'self sterile',
'parthenocarpic',
'insects'
]

print("\nThe available dfs are:\n-------\necoFlora\ngenFlora\nplantAtSource\nplantAtScrape\nsexChrom\n")
ecoFlora = pd.read_csv('/home/sean/NERCflora/ecoFlora/dataFlat.csv', sep='|')
genFlora = pd.read_csv('/home/sean/NERCflora/geneticFlora/data.csv', sep='|')
plantAtSource = pd.read_csv('/home/sean/NERCflora/plantAtlas/sourceData.csv', sep='|')
plantAtScrape = pd.read_csv('/home/sean/NERCflora/plantAtlas/scrapeData.csv', sep='|')
sexChrom = pd.read_csv('/home/sean/NERCflora/sexChrom/data.csv', sep='|')
