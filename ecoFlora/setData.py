import pandas as pd
import numpy as np
import pprint as pp
import statistics as stat

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

def filterIn(values, test):
    if type(values)==str:
        test = list(test)
        return [x for x in test if x in values] != []
    else:
        return False

def numVals(values):
    if type(values)==str:
        return len(set(values.split(', ')))
    else:
        return 0



df = pd.read_csv('/home/sean/NERCflora/ecoFlora/dataFlat.csv', sep='|')
vFilter = np.vectorize(filterIn)
vNumVals = np.vectorize(numVals)
