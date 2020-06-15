import pandas as pd
import numpy as np
import pprint as pp

def getDfFromCSV(species):
    dataDir = '/home/sean/NERCflora/ecoFlora/data/'
    dir = dataDir+species+'.csv'
    df = pd.read_csv(dir)
    return df


def setAllDf():
    #returns dictionsary of {speciesName: dataFrame} pairs
    idDir = '/home/sean/NERCflora/ecoFlora/idsWithData.csv'
    dfIds = pd.read_csv(idDir)
    dfDatas = {}
    for index, row in dfIds.iterrows():
        species = row['species']
        dfDatas.update( {species:getDfFromCSV(species)} )

    return dfDatas

def scanAllDfs(dfs, key):
    #Finds all df in dfs for which there is a row where df['Name'] == key
    #Returns list of dictionary
    #[{species1: [value11, value12...]}, {species2, [value21]}....]
    #hopefully there is just one value

    speciesValsDict = {}
    for species, df in dfs.items():
        if key in df['Name'].values:
            matchingDf = df[df['Name']==key]
            values = list(matchingDf['Value'])
            speciesValsDict.update({species:values})

    return speciesValsDict


def main():
    dfDatas = setAllDf()
    #print(dfDatas['capsella_bursa_pastoris'])
    valsDict_Incomp = scanAllDfs(dfDatas, 'Incompatibility systems')
    valsDict_Fert = scanAllDfs(dfDatas, 'Fertilization')
    speciesWithBoth = []
    for species, value in valsDict_Fert.items():
        if species in valsDict_Incomp.keys():
            speciesWithBoth.append(species)

    pp.pprint(float(len(speciesWithBoth))/float(len(dfDatas)))
    #pp.pprint(speciesValsDict)
    #pp.pprint(float(len(speciesValsDict))/float(len(dfDatas)))

main()
