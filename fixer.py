import sys
import argparse
from argparse import ArgumentParser
import re
from datetime import date
from string import Template
from itertools import islice
from types import SimpleNamespace

version = ('0.3.3')

# get the current date and put it in the correct string format
today = date.today()
date = today.strftime("%Y-%m-%d")

### command line argument parsing 
## define the argument parser
parser = ArgumentParser(description = "Fix a Cockatrice .xml file exported from MSE")
# first arg: file to be fixed
parser.add_argument('File', help = "path to the .xml file to fix")
# second arg: file datestamping flag
parser.add_argument('--date', '-d', dest='doDate', action='store_true', 
                    help = "datestamp the fixed file with today\'s date (default off)")
# third arg: flag for version number (exits the script if used)
parser.add_argument('--version', '-v', action='version',
                    version="fixer v" + version)
# fourth arg: what to name the output file
parser.add_argument('--outputname ', '-o', dest='outputName', default='set_fixed.xml',
                    help = "what to name the output (fixed) file. Defaults to set_fixed.xml")
# fifth arg: flag for verbosity option
#parser.add_argument('--verbose', '-v', dest='Verbose', action='store_true',
                    #help = "verbose extraction and construction")


def outputInit(): ## output initialization function
    with open(outputFilename, "wt") as Out: #open the output file
        Out.write('<?xml version="1.0" encoding="UTF-8"?>\n') #write the .xml general header
        Out.write('<cockatrice_carddatabase version="4">\n') #write the Cockatrice database header
    [setEnd,setBlock] = blockExtract('sets', 0) #extract the set info block
    tags = ['name','longname','settype','releasedate'] #the list of info tags that the set should have
    setInfo = infoExtract(setBlock, tags) #get the set info from the block
    fixInfo = setDiagnose(setInfo) #check for missing info
    newBlock = setBuild(fixInfo, 'set') #build the new set info block
    with open(outputFilename, "at") as Out: # write set block and <cards> tag to output file
        Out.write('    <sets>\n')
        Out.write(newBlock)
        Out.write('    </sets>\n')
        Out.write('    <cards>\n')
    return [setEnd, fixInfo.name]

def blockExtract(tag, loc): ## extracts an entire block (set or card)
    start = '<' + tag + '>'
    end = '</' + tag + '>' #build matchable strings for the start and end tags
    ## open the input file and search for the first string enclosed by <tag></tag>
    with open(inputFilename, "rt") as In:
        i = loc
        for line in islice(In, loc, None):
            if re.search(start, line):
                block = line
                break
            else: i=i+1
        for line in islice(In, loc, None):
            block = block + line
            i = i+1
            if re.search(end, line):
                break
        end = i
    return [end,block]

def infoExtract(block, tags): ## extract the info from a set block
    # block should be the info block string, tags should be a list of info tags
    info = SimpleNamespace() #define the block's info as a namespace object
    d = vars(info)
    for tag in tags:
        if tag in block: #check if the tag is present
            i = 1
            # search block for string of form <tag>info</tag>
            #val = 'the info string'# extract info from string
            #d[tag] = val #assign info to the appropriate tag in the namespace
    ### BEGIN TEST ###
    d['name'] = "TST"
    d['longname'] = "Test Set"
    d['settype'] = "Glorious"
    ### END TEST ###
    return info

def setBuild(info, blocktype): ## build a new set block using an info namespace
    if blocktype=='set':
        block = setBlock_temp.substitute(vars(info))
    if blocktype=='card':
        block = 'whatever'
    return block

def outputFin(): ## finalize the output file
    with open(outputFilename, "at") as Out:
        Out.write('\n    </cards>\n')
        Out.write('</cockatrice_carddatabase>')
    print("Successfully wrote " + outputFilename)


def main(cardsStart): ## The main program loop, for fixing cards

    outputFin()


def setDiagnose(info): ## detect missing set info, set to defaults if noncritical, else send message
    d = vars(info)
    if not hasattr(info, 'settype'): d['settype'] = 'Custom' #default set type due to assumed usage
    if not doDate: #then check if there's already an assigned date
        if not hasattr(info, 'releasedate'): d['releasedate'] = date #assign current date as default
    else: d['releasedate'] = date #set date if datestamping was on
    if not hasattr(info, 'longname'):
        d['longname'] = ' '
        print("Set has no name")
    if not hasattr(info, 'name'):
        d['name'] = ' '
        print("Set has no set code")
    return info

def cardDiagnose(info): ## detect missing critical card info
    whatever=1

### String templates

singleInfo = Template('<$tag>$info</$tag>') #output template for a single pair of [tag, info]
setBlock_temp = Template('        <set>\n' +
                         '            <name>$name</name>\n' +
                         '            <longname>$longname</longname>\n' +
                         '            <settype>$settype</settype>\n' +
                         '            <releasedate>$releasedate</releasedate>\n' +
                         '        </set>\n') #output template for a set info block
regex_temp = Template('<$tag>(.+?)</$tag>') #template for the regex string for finding info for a given tag


### BEGIN TEST ###
#argspace = parser.parse_args(['/Users/BrandonPlay/Documents/Eragon/testset.xml', '-o /Users/BrandonPlay/Documents/Eragon/set_fixed.xml'])
### END TEST ###

### Initialize the application

## parse the supplied arguments and extract their surplus value, like a capitalist
argspace = parser.parse_args()
inputFilename = argspace.File
outputFilename = argspace.outputName
doDate = argspace.doDate

[cardsLoc, setName] = outputInit() #conduct output initialization,
# retrieving card info location and set name into global variables

main(cardsLoc) #activate main processing starting at start of card info
