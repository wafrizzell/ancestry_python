import csv
from collections import Counter
import os
import re

basedir = r'C:\Users\William\Documents'

indir = os.path.join(basedir, 'Ancestry_Mom')                      # what directory source files come from
outdir = indir

ancestorsCsvFile = os.path.join(indir, 'a_Jean_Gibson.csv')            # the complete path of ancestor csv file to read 
memberCsvFile = os.path.join(indir, 'm_Jean_Gibson.csv')               # the complete path of member csv file to read 
treeGedFile = os.path.join(indir, 'BylFamilyTree.ged')   # the complete path of tree GED file to read 

dnaMatchfile = os.path.join(outdir, 'DNAMatches.csv')          # the name of the output file
treeMatchFile = os.path.join(outdir, 'DirectTreeMatches.csv')       # the name of the count file

theRegex = re.compile('[12][0-9]{3}')

# the columns you want selected
fieldsToSelect = ['starred', 'note', 'range', 'confidence','sharedCM','sharedSegments','private','people']
outDnaMatchFields = ['starred', 'user', 'profileurl', 'note', 'range', 'confidence','sharedCM','sharedSegments','private','people']
outTreeMatchFields = ['user','profileurl','surname', 'given', 'birthdateAncestor','birthdateGED']
theURLLookup = {}
thebDateLookup = {}
convertState = 0
increment = lambda x: (x + 1) % 4 
birthdate = ''

with open(treeGedFile, 'r') as theInputGed:
    lineNumber = -1
    for row in theInputGed:
        lineNumber = lineNumber + 1
        if convertState == 0:
            if ' INDI' in row:
                convertState = increment(convertState)
        if convertState == 1:
            if 'BIRT' in row:
                convertState = increment(convertState)
        elif convertState == 2:
            if 'DATE' not in row:
                convertState = 0
            else:
                dateList = row.split(' ')
                birthdate = ' '.join(dateList[2:]).strip()
                convertState = increment(convertState)
        elif convertState == 3:
            if 'NAME' in row:
                nameList = row[7:].split(r'/')
                if len(nameList) < 2:
                    print "Missing surname at line " + str(lineNumber)
                    convertState = 0
                    continue
                thebDateLookup[(nameList[0].lower().strip(), nameList[1].lower().strip())] = birthdate
                convertState = increment(convertState)

with open(memberCsvFile, 'rb') as theInputURLRF, open(dnaMatchfile, 'wb') as dnaMatch:
    theRReader = csv.DictReader(theInputURLRF)
    theDnaWriter = csv.DictWriter(dnaMatch, outDnaMatchFields)
    for row in theRReader:
        theUser = row['name'] + '_' + row['admin'] + '_ANC'
        theURLLookup[theUser] = row['profileurl']
        theOutRow = {key: row[key] for key in fieldsToSelect}
        theOutRow['user'] = theUser
        theOutRow['profileurl'] = row['profileurl']
        theDnaWriter.writerow(theOutRow)

with open(ancestorsCsvFile, 'rb') as theInputAncestors, open(treeMatchFile, 'wb') as treeMatch:
    theAReader = csv.DictReader(theInputAncestors)
    theTreeMatchWriter = csv.DictWriter(treeMatch, outTreeMatchFields)
    for row in theAReader:
        lookupKey = (row['given'].lower().strip(), row['surname'].lower().strip()) 
        theUser = row['name'] + '_' + row['admin'] + '_ANC'
        if lookupKey in thebDateLookup: # and theUser in theURLLookup:
            baMatch = theRegex.search(row['birthdate'])
            geMatch = theRegex.search(thebDateLookup[lookupKey])
            if baMatch and geMatch and baMatch.group() == geMatch.group():
                theOutRow = {}
                theOutRow['birthdateAncestor'] = row['birthdate']
                theOutRow['birthdateGED'] = thebDateLookup[lookupKey]
                theOutRow['surname'] = lookupKey[1]
                theOutRow['given'] = lookupKey[0]
                theOutRow['user'] = theUser
                theOutRow['profileurl'] = theURLLookup.get(theUser, 'Not Found')
                theTreeMatchWriter.writerow(theOutRow)

