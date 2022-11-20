import csv
import os

basedir = r'C:\Users\William\Documents'

indir1 = os.path.join(basedir, 'Ancestry_Will')                      # what directory Will source files come from
indir2 = os.path.join(basedir, 'Ancestry_Mom')                       # what directory Dad source files come from
outdir = os.path.join(basedir, 'Comparisons')

matchesWill = os.path.join(indir1, 'DNAMatches.csv')              # the complete path of Will matches csv file to read 
matchesDad = os.path.join(indir2, 'DNAMatches.csv')               # the complete path of Dad matches csv file to read 

inWillMatchFile = os.path.join(outdir, 'MatchesInWillNotMom.csv')          # the name of the output file of matches in Will not Dad
inDadMatchFile = os.path.join(outdir, 'MatchesInMomNotWill.csv')         # the name of the count file of matches in Dad not Will
inBothMatchFile = os.path.join(outdir, 'MatchesBothWillandMom.csv')                 # the name of the count file of matches in both

# the columns you want selected
fieldsToSelect = ['starred', 'user', 'profileurl', 'note', 'range', 'confidence','sharedCM','sharedSegments','private','people']
outFields = ['starred', 'user', 'profileurl', 'note', 'range', 'confidence','sharedCM','sharedSegments','private','people']


with open(matchesWill, 'rb') as willMatches, open(matchesDad, 'rb') as dadMatches, open(inWillMatchFile, 'wb') as inWill, open(inDadMatchFile, 'wb') as inDad, open(inBothMatchFile, 'wb') as inBoth:
    theWReader = csv.DictReader(willMatches)
    theDReader = csv.DictReader(dadMatches)

    theWillWriter = csv.DictWriter(inWill, outFields)
    theDadWriter = csv.DictWriter(inDad, outFields)
    theBothWriter = csv.DictWriter(inBoth, outFields)

    dReaderDict = {}
    wReaderDict = {}

    for row in theDReader:
        dReaderDict[row['user']] = row

    # Get set of keys from the dReaderDict
    dadUserSet = dReaderDict.viewkeys()

    for row in theWReader:
        wReaderDict[row['user']] = row

    # Get set of keys from the wReaderDict
    willUserSet = wReaderDict.viewkeys()

    # Now make your sets that you want to output using set operations from the two sets above.

    # To do set difference (IF user in WReader is not in DReader then output as inWill)
    willButNotDadKeySet = willUserSet - dadUserSet

    # Set difference but the other direction (IF user in DReader is not in WReader the output as inDad)
    dadButNotWillKeySet = dadUserSet - willUserSet

    # To do set intersection (IF user in WReader is in (== user) in DReader then output as inBoth)
    bothKeySet = dadUserSet & willUserSet

    # Finally, output your results by fetching the values from your dictionaries
    for theKey in willButNotDadKeySet:
        theWillWriter.writerow(wReaderDict[theKey])

    for theKey in dadButNotWillKeySet:
        theDadWriter.writerow(dReaderDict[theKey])

    for theKey in bothKeySet:
        theBothWriter.writerow(dReaderDict[theKey])

