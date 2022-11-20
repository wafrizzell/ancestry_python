import csv
import sys
from collections import Counter
import os
import re

def matchCheck(targetName,surname,givenName,dob):
        tmpFlag = targetName[0].lower() == surname.lower() and targetName[1].lower() == givenName.lower() and targetName[2].lower() == dob.lower()
        return tmpFlag


basedir = r'C:\Users\william'

theRegex = re.compile('[12][0-9]{3}')

indir = os.path.join(basedir, r'Documents\Ancestry_Dad')                      # what directory source files come from
outdir = os.path.join(basedir, r'Documents\Comparisons')                     # what directory you want destination files to go

theInputFile = os.path.join(indir, 'a_Carl_Carlton.csv')         # the complete path of csv file to read 

surname = ""
givenName = ""
dob = ""
outfile = ''

numArgs = len(sys.argv)
if numArgs < 4:
    print("Must specify surname, given, date or year of birth, (in quotes if a field contains spaces.")
    exit(1)
else:
    surname = sys.argv[1]
    givenName = sys.argv[2]
    paramMatch = theRegex.search(sys.argv[3])
    dob = paramMatch.group()
    outfile = os.path.join(outdir, surname + '_' + givenName + '_' + dob + '_count.csv')


# the columns you want selected
fieldsToSelect = ['surname','given','birthdate','name','admin']   
outFieldsToSelect = ['userFile1', 'user1ProfileURL', 'userFile2', 'user2ProfileURL'] + fieldsToSelect
nameCountFields = ['surname', 'given', 'birthyear', 'count']
mapNameAdminToCounter = {}
totalCount = Counter()

with open(outfile, 'wb') as outF, open(theInputFile, 'rb') as theInputF:
    writer = csv.DictWriter(outF, nameCountFields)
    theReader = csv.DictReader(theInputF)
    writer.writeheader()
    for row in theReader:
        nameAdmin = (row['name'].strip(), row['admin'].strip())
        theResult = theRegex.search(row['birthdate'].strip())
        if not theResult or not row['surname'] or not row['given']:
            #print('Invalid info in row for ' + str(row))
            continue

        targetName = (row['surname'].strip(), row['given'].strip(), theResult.group())

        if nameAdmin not in mapNameAdminToCounter:
            mapNameAdminToCounter[nameAdmin] = [False,Counter()]

        if matchCheck(targetName,surname,givenName,dob):
            #print('Found query string.')
            mapNameAdminToCounter[nameAdmin][0] = True

        theCounter = mapNameAdminToCounter[nameAdmin][1]

        theCounter[targetName] += 1

    for theNameAdmin in mapNameAdminToCounter.viewkeys():
        #print(str(totalCount))
        #print(str(mapNameAdminToCounter[theNameAdmin][1]))
        if mapNameAdminToCounter[theNameAdmin][0]:
            #print('Adding in new counter.')
            totalCount = totalCount + mapNameAdminToCounter[theNameAdmin][1]
        
    for ci in totalCount.most_common(500):
        #print(str(ci))
        writer.writerow({'surname':ci[0][0], 'given':ci[0][1], 'birthyear':ci[0][2], 'count':ci[1]})


