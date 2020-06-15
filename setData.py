import pandas as pd

print("\nThe available dfs are:\ndf_ecoIds\ndf_plantAt\ndf_genFlora\n")

#ecoFlora ids with data
df_ecoIds = pd.read_csv('/home/sean/NERCflora/ecoFlora/idsWithData.csv')
df_genFlora = pd.read_csv('/home/sean/NERCflora/geneticFlora/data.csv', sep='|')
df_plantAt = pd.read_csv('/home/sean/NERCflora/plantAtlas/data.csv', sep='|')
