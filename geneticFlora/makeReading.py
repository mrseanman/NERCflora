import pandas as pd
import numpy as np
import nltk

porter = nltk.PorterStemmer()

def makeReading(species):
    df = pd.read_csv('/home/sean/NERCflora/geneticFlora/data.csv', sep='|').fillna('')
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
    #df with abstracts matching the regex
    good_abstracts = df[df['Abstract'].str.contains(searchRegEx)]


    #good_abstracts----------------------------------------------------------

    writeDir = currSpeciesDir+'abtractsToRead.txt'
    file = open(writeDir, 'w')

    for index, row in good_abstracts.iterrows():
        file.write(str(index)+'\n')
        file.write(row['Title']+'\n')
        file.write(row['Author']+'\n')
        file.write(str(row['Year'])+'\n')
        file.write('--------------------------------\n')
        file.write(row['Abstract']+'\n\n\n')


    #all_abstracts-----------------------------------------------------------

    writeDir = currSpeciesDir+'allAbstracts.txt'
    file = open(writeDir, 'w')

    for index, row in df.iterrows():
        file.write(str(index)+'\n')
        file.write(row['Title']+'\n')
        file.write(row['Author']+'\n')
        file.write(str(row['Year'])+'\n')
        file.write('--------------------------------\n')
        file.write(row['Abstract']+'\n\n\n')
