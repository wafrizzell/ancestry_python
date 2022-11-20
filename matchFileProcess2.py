import csv
from collections import Counter
import os

basedir = r'C:\Users\William\Documents'

indir = os.path.join(basedir, 'Ancestry_Dad')                      # what directory source files come from
outdir = os.path.join(basedir, 'Ancestry_Dad')                     # what directory you want destination files to go

theInputFile = os.path.join(indir, 'DadMatchList.csv')         # the complete path of csv file to read 
theURLFile = os.path.join(indir, 'm_Carl_Carlton.csv')          # the complete path of URL match file to read 

outfile = os.path.join(outdir, 'DadMatchFiltered.csv')          # the name of the output file
occurrencefile = os.path.join(outdir, 'DadCountFile.csv')       # the name of the count file


# the columns you want selected
fieldsToSelect = ['Surname1','Given1','Birth Date1','Birth Place1', 'Death Date1', 'Death Place1']   
outFieldsToSelect = ['userFile1', 'user1ProfileURL', 'userFile2', 'user2ProfileURL'] + fieldsToSelect
nameCountFields = ['Surname1','Given1','Birth Date1', 'count']
theURLLookup = {}
theCountOfNames = Counter()

with open(theURLFile, 'rb') as theInputURLRF:
    theRReader = csv.DictReader(theInputURLRF)
    for row in theRReader:
        theURLLookup[row['name'] + '_' + row['admin'] + '_ANC'] = row['profileurl']
with open(outfile, 'wb') as outF, open(theInputFile, 'rb') as theInputF:
    writer = csv.DictWriter(outF, outFieldsToSelect)
    theReader = csv.DictReader(theInputF)
    writer.writeheader()
    for row in theReader:
        processFile1 = theURLLookup.get(row['File1'], "Not Found")
        processFile2 = theURLLookup.get(row['File2'], "Not found")
        if processFile1 != processFile2:
            theOutRow = {key: row[key] for key in fieldsToSelect}
            theOutRow['userFile1'] = row['File1']
            theOutRow['user1ProfileURL'] = processFile1
            theOutRow['userFile2'] = row['File2']
            theOutRow['user2ProfileURL'] = processFile2
            writer.writerow(theOutRow)
            theCountOfNames[(row['Surname1'],row['Given1'],row['Birth Date1'])] += 1
with open(occurrencefile, 'wb') as theoccurRF:
    theOWriter = csv.DictWriter(theoccurRF, nameCountFields)
    for ci in theCountOfNames.most_common():
        theOWriter.writerow({'Surname1':ci[0][0],'Given1':ci[0][1],'Birth Date1':ci[0][2], 'count':ci[1]})