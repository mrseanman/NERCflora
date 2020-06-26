import pandas as pd
import numpy as np
import copy

def outcrossing(df):
    boolsList = []
    #-------------------------------
    #Is obligatory cross acc to ecoFlora
    obligatoryCrossers = uniqAinB('obligatory cross', df['Fertilization'])
    boolsList.append(obligatoryCrossers)
    #-------------------------------
    insectsFert = uniqAinB('insects', df['Fertilization'])
    boolsList.append(insectsFert)
    #-------------------------------
    selfSterileFert = filtAinB('self sterile', df['Fertilization'])
    boolsList.append(selfSterileFert)
    #------------------------------
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

def hasInfo(series):
    r = []
    for s in series:
        r.append(type(s)==str)
    return np.array(r)

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

def assign3(fdf):
    df = copy.deepcopy(fdf)
    df['_fertMode3'] = np.nan

    outcrossBool = outcrossing(df)
    cleistogamousBool = cleistogamous(df)
    apomicticBool = uniqAinB('apomictic', df['Fertilization'])
    mixedBool = filtAinB(['cross and self',
                            'cross or automatic self',
                            'normally cross',
                            'normally self'],
                            df['Fertilization'])
    selfBool = cleistogamousBool | apomicticBool
    mixedBool = mixedBool | (outcrossBool & selfBool)
    selfBool = selfBool & ~mixedBool & ~outcrossBool
    outcrossBool = outcrossBool & ~mixedBool

    #check
    #print(selfBool.sum() + mixedBool.sum() + outcrossBool.sum())
    #print('should eq')
    #print((selfBool | mixedBool | outcrossBool).sum())

    df['_fertMode3'] = np.nan
    df.loc[outcrossBool, '_fertMode3'] = 'outcrossing'
    df.loc[selfBool, '_fertMode3'] = 'selfing'
    df.loc[mixedBool, '_fertMode3'] = 'mixed'

    return df

def assign5(fdf):
    df = copy.deepcopy(fdf)
    outcrossBool = outcrossing(df)
    cleistogamousBool = cleistogamous(df)
    apomicticBool = uniqAinB('apomictic', df['Fertilization'])
    normCrossBool = filtAinB('normally cross', df['Fertilization'])
    normSelfBool = filtAinB('normally self', df['Fertilization'])
    mixedBool = filtAinB(['cross and self',
                            'cross or automatic self',],
                            df['Fertilization'])

    selfBool = cleistogamousBool | apomicticBool
    normCrossBool = normCrossBool | (outcrossBool & mixedBool)
    normSelfBool = normSelfBool | (selfBool & mixedBool)
    mixedBool = mixedBool | (mixedBool & (selfBool | normSelfBool | normCrossBool | outcrossBool))
    mixedBool = mixedBool | (outcrossBool & selfBool)

    outcrossBool = outcrossBool & ~(selfBool | mixedBool | normSelfBool | normCrossBool)
    selfBool = selfBool & ~(normSelfBool | mixedBool | normCrossBool | outcrossBool)
    normCrossBool = normCrossBool & ~(selfBool | mixedBool | normSelfBool | outcrossBool)
    normSelfBool = normSelfBool & ~(selfBool | mixedBool | normCrossBool | outcrossBool)

    #print(selfBool.sum() + normSelfBool.sum() +  mixedBool.sum() + normCrossBool.sum() +  outcrossBool.sum())
    #print('should eq')
    #print((selfBool | normSelfBool | mixedBool | normCrossBool | outcrossBool).sum())

    df['_fertMode5'] = np.nan
    df.loc[selfBool, '_fertMode5'] = 'selfing'
    df.loc[normSelfBool, '_fertMode5'] = 'normally self'
    df.loc[mixedBool, '_fertMode5'] = 'mixed'
    df.loc[normCrossBool, '_fertMode5'] = 'normally cross'
    df.loc[outcrossBool, '_fertMode5'] = 'outcrossing'

    return df

def main():
    ecoFlora = pd.read_csv('/home/sean/NERCflora/ecoFlora/dataFlat.csv', sep='|')
    ecoFlora = assign3(ecoFlora)
    ecoFlora = assign5(ecoFlora)
    breakpoint()

ecoFlora = pd.read_csv('/home/sean/NERCflora/ecoFlora/dataFlat.csv', sep='|')
ecoFlora = assign3(ecoFlora)
ecoFlora = assign5(ecoFlora)
