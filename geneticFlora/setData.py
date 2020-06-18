import pandas as pd
import numpy as np
import pprint as pp
import statistics as stat

def filterIn(values, test):
    if type(values)==str:
        test = list(test)
        return [x for x in test if x in value] != []
    else:
        return False

df = pd.read_csv('/home/sean/NERCflora/geneticFlora/data.csv', sep='|')
