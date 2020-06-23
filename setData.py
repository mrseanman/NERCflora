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
#e.g. filterUnique(values='abc, abc', test='abc') returns True.
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
'parthenocarpic',
'insects'
]

print("\nThe available dfs are:\n-------\necoFlora\ngenFlora\nplantAtSource\nplantAtScrape\nsexChrom\n")


ecoFlora = pd.read_csv('/home/sean/NERCflora/ecoFlora/dataFlat.csv', sep='|')
genFlora = pd.read_csv('/home/sean/NERCflora/geneticFlora/data.csv', sep='|')
plantAtSource = pd.read_csv('/home/sean/NERCflora/plantAtlas/sourceData.csv', sep='|')
plantAtScrape = pd.read_csv('/home/sean/NERCflora/plantAtlas/scrapeData.csv', sep='|')
sexChrom = pd.read_csv('/home/sean/NERCflora/sexChrom/data.csv', sep='|')

poacae = pd.read_csv('/home/sean/NERCflora/plantList/poaceae.csv')
