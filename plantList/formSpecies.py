import pandas as pd

def familyList(family):
    family = family.lower()
    dir = '/home/sean/NERCflora/plantList/' + family + '.csv'
    dfFamilyList = pd.read_csv(dir)
    
