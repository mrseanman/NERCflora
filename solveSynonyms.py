import pandas as pd
def solveSyn(speciesSeries, dfEcoIds, dfEcoNoSyn):
    returnSer = []
    for species in speciesSeries:
        if species in dfEcoIds.species.unique():
            id = dfEcoIds[ dfEcoIds['species']==species].iloc[0]['id']
            speciesSynFor = dfEcoNoSyn[ dfEcoNoSyn['id'] == id].iloc[0]['species']
            returnSer.append(speciesSynFor)
        else:
            returnSer.append(species)


    return pd.Series(returnSer)


dfEcoIds = pd.read_csv('/home/sean/NERCflora/ecoFlora/ids/ids.csv')
dfEcoNoSyn = pd.read_csv('/home/sean/NERCflora/ecoFlora/ids/idsNoSyn.csv')
dfPlantAt = pd.read_csv('/home/sean/NERCflora/plantAtlas/data.csv', sep='|')
dfGenFlora = pd.read_csv('/home/sean/NERCflora/geneticFlora/data.csv', sep='|')

dfPlantAtSynSolv = dfPlantAt
dfPlantAtSynSolv['species'] = solveSyn(dfPlantAtSynSolv['species'], dfEcoIds, dfEcoNoSyn)
dfGenFloraSynSolv = dfGenFlora
dfGenFloraSynSolv['species'] = solveSyn(dfGenFloraSynSolv['species'], dfEcoIds, dfEcoNoSyn)

dfPlantAtSynSolv.to_csv('plantAtDataSynSolv.csv', index=False, sep='|')
dfGenFloraSynSolv.to_csv('genFloraDataSynSolv.csv', index=False, sep='|')
