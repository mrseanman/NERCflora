import pandas as pd
import numpy as np
import copy
from formData import uniqAinB, filtAinB, hasInfo
ecoFlora = pd.read_csv('/home/sean/NERCflora/formFinal/finalFlat.csv', sep='|')
plantAt = pd.read_csv('/home/sean/NERCflora/plantAtlas/sourceData.csv', sep='|')
