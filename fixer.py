import sys
import argparse
from argparse import ArgumentParser
import math
import re
from datetime import date
from string import Template
from itertools import islice
from types import SimpleNamespace

version = ('0.3.1')

# get the current date and put it in the correct string format
today = date.today()
date = today.strftime("%Y-%m-%d")

### command line argument parsing 
## define the argument parser
parser = ArgumentParser(description = "Fix a Cockatrice .xml file exported from MSE")
# first arg: file to be fixed
parser.add_argument('File', help = "the .xml file to fix")
# second arg: file datestamping flag
parser.add_argument('--date', '-d', dest='doDate', action='store_true', 
                    help = "datestamp the fixed file with today\'s date (default off)")
# third arg: flag for version number (exits the script if used)
parser.add_argument('--version', '-v', action='version',
                    version="fixer v" + version)
# fourth arg: what to name the output file
parser.add_argument('--outputname', '-o', dest='outputName', default='set_fixed.xml',
                    help = "what to name the output (fixed) file. Defaults to set_fixed.xml")
# fifth arg: flag for verbosity option
#parser.add_argument('--verbose', '-v', dest='Verbose', action='store_true',
                    #help = "verbose extraction and construction")


def outputInit(): ## output initialization function
    with open(outputFilename, "wt") as Out: #open the output file
        Out.write('<?xml version="1.0" encoding="UTF-8"?>\n') #write the .xml general header
        Out.write('<cockatrice_carddatabase version="4">\n') #write the Cockatrice database header
    [setEnd,setBlock] = blockExtract('sets', 0) #extract the set info block
    tags = [] #the list of info tags that the set should have
    setInfo = infoExtract(setBlock, tags) #get the set info from the block
    newBlock = setBuild(setInfo, 'set') #build the new set info block
    with open(outputFilename, "at") as Out: # write set block and <cards> tag to output file
        Out.write('    <sets>\n')
        Out.write(newBlock)
        Out.write('    </sets>\n')
        Out.write('    <cards>\n')
    return setEnd

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
    
    
    ### BEGIN TEST ###
    d['foo'] = 'bar'
    ### END TEST ###
    
    if doDate==True: d['date'] = date
    return info

def setBuild(info, blocktype): ## build a new set block using an info namespace
    block = 'test block'
    return block

def outputFin(): ## finalize the output file
    with open(outputFilename, "at") as Out:
        Out.write('\n    </cards>\n')
        Out.write('</cockatrice_carddatabase>')
    print("Successfully wrote " + outputFilename)

def main(cardsStart):

    outputFin()


### String templates for writing output

singleInfo = Template('<$tag>$info</$tag>') #template for a single pair of [tag, info]


### BEGIN TEST ###
argspace = parser.parse_args(['/Users/BrandonPlay/Documents/Eragon/Eragon Core.xml'])

### Initialize the application

## parse the supplied arguments and extract their surplus value, like a capitalist
#argspace = parser.parse_args()
inputFilename = argspace.File
outputFilename = argspace.outputName
doDate = argspace.doDate

#cardsLoc = outputInit() #conduct output initialization

#main(cardsLoc) #activate main processing
