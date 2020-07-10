import pandas as pd
import numpy as np
import pprint as pp
import statistics as stat

def filtAinB(test, series):
#returns truth value array if test or any x in test is in value
    ins = []
    for value in series:
        if type(value)==str:
            if type(test)==str:
                ins.append(test in value)
            else:
                test = list(test)
                ins.append([x for x in test if x in value] != [])
        else:
            ins.append(False)

    return np.array(ins)
def uniqAinB(test, series):
#returns thruth value if test is the only value present in values
#e.g. filterUnique(values='abc, abc', tex\\\\\\\\\\\\\\\\\\\\aaaaaaaaaaaaaaaawst='abc') returns True.
#but 'abc, abc'=='abc' returns False
    insUnique = []
    for value in series:
        if type(value)==str:
            insUnique.append((test in value)
                    and
                    ([x for x in value.split(', ') if not(x==test)] == []))
        else:
            insUnique.append(False)
    return np.array(insUnique)
#expects ecoFlora df as input
#returns truth value array whether outcrossing
def outcrossing(df):
    boolsList = []
    #-------------------------------
    #Is obligatory cross acc to ecoFlora
    obligatoryCrossers = uniqAinB('obligatory cross', df['Fertilization'])
    boolsList.append(obligatoryCrossers)
    #-------------------------------
    #fix dioecous1
    dioecous2 = uniqAinB('dioecous', df['Dicliny'])
    boolsList.append(dioecous2)
    #-------------------------------
    #dichogamy
    dichogamousEnough = []
    for dichog in df['Dichogamy']:
        dichogamousEnough.append(   (dichog=='protogynous ')            or
                                    (dichog=='protandrous')             or
                                    (dichog=='markedly protandrous')    or
                                    (dichog=='markedly protogynous')    or
                                    (dichog=='entirely protandrous')    or
                                    (dichog=='entirely protogynous '))
    boolsList.append(dichogamousEnough)
    #-------------------------------
    #self incompatibility
    selfIncompatible = []
    for incomp in df['Incompatibility systems']:
        if type(incomp)==str:
            selfIncompatible.append(not('none' in incomp))
        else:
            selfIncompatible.append(False)
    boolsList.append(selfIncompatible)
    #-------------------------------
    #is poacae
    poacae = []
    for species in df['species']:
        poacae.append(species.split('_')[0]=='poa')
    #boolsList.append(poacae)
    #-----------

    boolsArray = np.array(boolsList)
    return(np.any(boolsArray, axis=0))
#np.nan is annoyingly useless as it doesnt accept str arguments
def hasInfo(series):
    r = []
    for s in series:
        r.append(type(s)==str)
    return np.array(r)
def NOTobligatorySelf(df):
    #Any thing that would impy it is not obligatory self
    #that might not imply outcrossing or mixed
    print('stub')
def cleistogamous(df):
    cleists=[]
    for cleist in df['Cleistogamy']:
        if type(cleist)==str:
            #print(cleist)
            cleists.append( cleist=='pseudo-cleistogamous'     or
                            cleist=='entirely cleistogamous'    or
                            cleist=='usually cleistogamous')
        else:
            cleists.append(False)
    return np.array(cleists)



searchStrings=[
'fertil',
'selfing',
'self fert',
'outcross',
'dioec'
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
'parthenocarpic'
]

def makeReading(species, good_abstracts, good_descriptions):
    dfGenFlora = pd.read_csv('/home/sean/NERCflora/geneticFlora/data.csv', sep='|').fillna('')
    dfPlantAtScrape = pd.read_csv('/home/sean/NERCflora/plantAtlas/scrapeData.csv', sep='|').fillna('')
    exampleSpecies = 'agrostis_curtisii'

    searchStrings=[
    'fertiliz',
    'fertilis',
    'selfing',
    'outcrossing',
    'dichog',
    'dioec',
    'diclin',
    'incompatib',
    'cleistog',
    'cross',
    'self'
    ]

    #to make the regex case insensitive
    case_ins='(?i)'
    #final regex searches for contains any of searchStrings case insensitive
    searchRegEx=case_ins+'|'.join(searchStrings)
    #dfGenFlora with abstracts matching the regex
    good_abstracts = good_abstracts[good_abstracts['species']==species]
    good_descriptions = good_descriptions[good_descriptions['species']==species]

    #print(good_descriptions.shape)
    #print(good_abstracts.shape)

    writeDir = '/home/sean/NERCflora/_reading/species/' + species + '.txt'
    file = open(writeDir, 'w')


    file.write('------------- Description -------------------\n')
    file.write('#plantat website\n')
    descriptionList = list(good_descriptions['ecology'])
    if len(descriptionList)>0:
        file.write(descriptionList[0] + '\n\n\n')



    #good_abstracts----------------------------------------------------------
    file.write('------------- Matching Abstracts -------------------\n')
    for index, row in good_abstracts.iterrows():
        file.write(str(index)+'\n')
        file.write('#'+row['title']+'\n')
        file.write('#'+row['author']+'\n')
        file.write('#'+str(row['year'])+'\n')
        file.write('--------------------------------\n')
        file.write(row['abstract']+'\n\n\n')


    #all_abstracts-----------------------------------------------------------
    file.write('------------- All Abstracts -------------------\n')
    for index, row in dfGenFlora[dfGenFlora['species']==species].iterrows():
        file.write(str(index)+'\n')
        file.write('#'+row['title']+'\n')
        file.write('#'+row['author']+'\n')
        file.write('#'+str(row['year'])+'\n')
        file.write('--------------------------------\n')
        file.write(row['abstract']+'\n\n\n')

    file.close()

print("\nThe available dfs are:\n-------\necoFlora\ngenFlora\nplantAtSource\nplantAtScrape\nsexChrom\n")


ecoFlora = pd.read_csv('/home/sean/NERCflora/ecoFlora/dataFlat.csv', sep='|')
genFlora = pd.read_csv('/home/sean/NERCflora/geneticFlora/data.csv', sep='|')
plantAtSource = pd.read_csv('/home/sean/NERCflora/plantAtlas/sourceData.csv', sep='|')
plantAtScrape = pd.read_csv('/home/sean/NERCflora/plantAtlas/scrapeData.csv', sep='|')
sexChrom = pd.read_csv('/home/sean/NERCflora/sexChrom/data.csv', sep='|')

poacae = pd.read_csv('/home/sean/NERCflora/plantList/poaceae.csv')

badEco = ecoFlora[ ~(   hasInfo(ecoFlora['Fertilization'])  |
                        cleistogamous(ecoFlora)             |
                        outcrossing(ecoFlora)               )]

goodEco = ecoFlora[ (   hasInfo(ecoFlora['Fertilization'])  |
                        cleistogamous(ecoFlora)             |
                        outcrossing(ecoFlora)               )]



searchStrings=[
'fertiliz',
'fertilis',
'selfing',
'outcrossing',
'dichog',
'dioec',
'diclin',
'incompatib',
'cleistog',
'cross',
'self'
]

listOfFams = ['poaceae', 'brassicaceae', 'compositae', 'papaveraceae']
poaceae = ecoFlora[ecoFlora['family']=='poaceae']
brassicaceae = ecoFlora[ecoFlora['family']=='brassicaceae']
compositae = ecoFlora[ecoFlora['family']=='compositae']
papaveraceae = ecoFlora[ecoFlora['family']=='papaveraceae']

usefulFields = [
'Range: 1. european countries where native',
'Chromosome number(s): 1. number',
'Seed/ovule ratio',
'Pollen/ovule ratio',
'Inbreeding (%)',
'Rarity Status',
'Typical abundance where naturally occurring',
'Heavy metal resistance',
'Seed production: 1. maximum (/flower)',
'Seed production: 2. typical range (/flower)',
'Seed production: 3. typical range (/plant)',
'Dispersal agent',
'Northern Limit in Britain',
'British distribution (post 1949 records)',
'Typical abundance where naturally occurring'
]

#to make the regex case insensitive
case_ins='(?i)'
#final regex searches for contains any of searchStrings case insensitive
searchRegEx=case_ins+'|'.join(searchStrings)
#dfGenFlora with abstracts matching the regex
good_abstracts = genFlora[genFlora.fillna('')['abstract'].str.contains(searchRegEx)]
good_descriptions = plantAtScrape[plantAtScrape.fillna('')['ecology'].str.contains(searchRegEx)]

speciesWithInfo = set(good_descriptions.species.unique()).union(set(good_abstracts.species.unique()))
readingSpecies = set(genFlora.species.unique()).union(set(plantAtScrape.species.unique()))
readingSpecies = set(badEco.species.unique()).intersection(readingSpecies)
readingSpecies = list(readingSpecies.intersection(speciesWithInfo))
