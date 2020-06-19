import pandas as pd
import numpy as np
import pprint as pp
import statistics as stat

def getDfFromCSV(species):
    dataDir = '/home/sean/NERCflora/ecoFlora/data/'
    dir = dataDir+species+'.csv'
    df = pd.read_csv(dir)
    return df


def setAllDf():
    #returns dictionary of {speciesName: dataFrame} pairs
    idDir = '/home/sean/NERCflora/ecoFlora/ids/idsNoSyn.csv'
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

def fertScore(fertVals):
    #1 is outcrossing 0 is selfing
    scoreDict = {
    'apomictic':0.0,
    'cross and self':0.5,
    'cross or automatic self':0.4,
    'no seed produced in britain':-1.0,
    'normally cross': 0.7,
    'normally self':0.3,
    'obligatory cross':1.0,
    'viviparous':0.5
    }

    scores = [scoreDict[value] for value in fertVals]
    mean = stat.mean(scores)
    std = stat.stdev(scores)
    return mean, std

def incompScore():
    print('stub')

def flatten(dfDatas):
    #forming a list of all attributes
    allAttr = set([])
    for species, df in dfDatas.items():
        allAttr.update(set(df['Name']))

    #initialise flattened df
    df = pd.DataFrame(data = { 'species':list(dfDatas.keys()) })
    for attr in allAttr:
        df[attr] = seriesFromAttr(dfDatas, attr)

    return df

def seriesFromAttr(dfDatas, attr):
    series = []
    for species, df in dfDatas.items():
        if attr in df['Name'].values:
            matchingDf = df[df['Name']==attr]
            values = ', '.join(sorted(list(matchingDf['Value'])))
        else:
            values = np.nan
        series.append(values)
    return pd.Series(series)


def appendNan(df, species):
    newDf = df
    maxIndex = max(df.index.tolist())
    newRowDat = {}
    for key in newDf.keys():
        newRowDat.update({key:np.nan})

    newRow = pd.DataFrame(data = newRowDat, index=[maxIndex+1])
    newRow['species'] = species
    newDf = newDf.append(newRow)
    return newDf

def main():
    dfDatas = setAllDf()
    dfFlat = flatten(dfDatas)


    #initialises a df with species as a column
    dfDataBySpec = pd.DataFrame(data = { 'species':list(dfDatas.keys()) })
    dfDataBySpec





    #print(dfDatas['capsella_bursa_pastoris'])
    valsDict_Incomp = scanAllDfs(dfDatas, 'Incompatibility systems')
    valsDict_Fert = scanAllDfs(dfDatas, 'Fertilization')
    speciesWithBoth = []
    for species, value in valsDict_Fert.items():
        if species in valsDict_Incomp.keys():
            speciesWithBoth.append(species)

    #for each species turns the list of values in to a comma separated string
    #each list of values must be alphabetically arranged first
    stringDict_Fert = {}
    stringDict_Incomp = {}
    for species, value in valsDict_Fert.items():
        stringDict_Fert[species] = ', '.join(set(sorted(value)))

    for species, value in valsDict_Incomp.items():
        stringDict_Incomp[species] = ', '.join(set(sorted(value)))




    unique_Fert = set(stringDict_Fert.values())
    unique_Incomp = set(stringDict_Incomp.values())
    pp.pprint(unique_Fert)
    pp.pprint(unique_Incomp)


    #strong



    breakpoint()
    #pp.pprint(float(len(speciesWithBoth))/float(len(dfDatas)))
    #pp.pprint(speciesValsDict)
    #pp.pprint(float(len(speciesValsDict))/float(len(dfDatas)))



df = pd.read_csv('/home/sean/NERCflora/ecoFlora/dataFlat.csv', sep='|')
dfIds = pd.read_csv('/home/sean/NERCflora/ecoFlora/ids/ids.csv')
dfIdNoSyn = pd.read_csv('/home/sean/NERCflora/ecoFlora/ids/idsNoSyn.csv')
dfIdsWithDataNoSyn = pd.read_csv('/home/sean/NERCflora/ecoFlora/ids/idsWithDataNoSyn.csv')
specWithoutData = [x for x in dfIdNoSyn.species.unique() if not(x in df.species.unique())]
