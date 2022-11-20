import csv
import os

basedir = r'C:\Users\William\Documents'

indir1 = os.path.join(basedir, 'Ancestry_Mom')                      # what directory Will source files come from
indir2 = os.path.join(basedir, 'Ancestry_Dad')                       # what directory Dad source files come from
outdir = os.path.join(basedir, 'Comparisons')

countWill = os.path.join(indir1, 'MomCountFile.csv')              # the complete path of Will Count csv file to read 
countDad = os.path.join(indir2, 'DadCountFile.csv')               # the complete path of Dad Count csv file to read 

inWillCountFile = os.path.join(outdir, 'CountsInMomandDad.csv')          # the name of the output file of counts in Will not Dad

# the columns you want selected
fieldsToSelect = ['surname', 'given', 'dob', 'count']
outFields = ['surname', 'given', 'dob', 'count']


with open(countWill, 'rb') as willCount, open(countDad, 'rb') as dadCount, open(inWillCountFile, 'wb') as inWill:
    theWReader = csv.DictReader(willCount)
    theDReader = csv.DictReader(dadCount)

    theWillWriter = csv.DictWriter(inWill, outFields)
    
    dReaderDict = {}
    wReaderDict = {}

    for row in theDReader:
        dReaderDict[(row['surname'], row['given'], row['dob'])] = row['count']

    # Get set of keys from the dReaderDict
    dadUserSet = dReaderDict.viewkeys()

    for row in theWReader:
        wReaderDict[(row['surname'], row['given'], row['dob'])] = row['count']

    # Get set of keys from the wReaderDict
    willUserSet = wReaderDict.viewkeys()

    # Now make your sets that you want to output using set operations from the two sets above.

    # To do set difference (IF user in WReader is not in DReader then output as inWill)
    willButNotDadKeySet = willUserSet & dadUserSet

   
    # Finally, output your results by fetching the values from your dictionaries
    for theKey in willButNotDadKeySet:
        theRow = {'surname':theKey[0],'given':theKey[1],'dob':theKey[2],'count':wReaderDict[theKey]}
        theWillWriter.writerow(theRow)
        