import sys
import argparse
from argparse import ArgumentParser
import math
import re
from datetime import date
from string import Template
from itertools import islice
from types import SimpleNamespace

version = ('0.2.2')

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
#fifth arg: flag for verbosity option
parser.add_argument('--verbose', '-v', dest='Verbose', action='store_true',
                    help = "verbose extraction and construction")


def outputInit(): ## output initialization function
    with open(outputFilename, "wt") as Out: #open the output file
        Out.write('<?xml version="1.0" encoding="UTF-8"?>\n') #write the .xml general header
        Out.write('<cockatrice_carddatabase version="4">\n') #write the Cockatrice database header
    [setEnd,setBlock] = blockExtract('sets', 0)
    tags = [] #the list of info tags that the set should have
    setInfo = infoExtract(setBlock, tags) #get the set info from the block
    newBlock = blockBuild(setInfo, 'set') #build the new set info block
    with open(outputFilename, "at") as Out:
        Out.write('    <sets>\n')
        Out.write(newBlock)
        Out.write('    </sets>\n')
    ### BEGIN TEST ###
    print('Extracted block: ' + setBlock)
    print('Set info: ' + setInfo)
    print('New block: ' + newBlock)
    ### END TEST ###
    return setEnd

def blockExtract(tag, loc): ## extracts an entire block (set or card)
    start = '<' + tag + '>'
    end = '</' + tag + '>' #Build matchable strings for the start and end tags
    ## open the input file and search for the first string enclosed by <tag></tag>
    with open(inputFilename, "rt") as In:
        i = loc
        for line in islice(In, loc, None):
            if re.search(start, line):
                block = line
                break
            else i=i+1
        for line in islice(In, loc, None):
            block = block + line
            if re.search(end, line):
                break
            else i=i+1
        end = i-1
    return [end,block]

def infoExtract(block, tags): ## extract the data from a block (set or card)
    info = types.SimpleNamespace(foo=bar) #define the block's info as a namespace object
    return info

def blockBuild(info, blocktype): ## build a new block using an info namespace
    block = 'test block'
    return block

### String templates for writing output

## Tagged info templates
singleInfo = Template('<$tag>$info</$tag>') #template for a single pair of [tag, info]




### Initialize the application
    
## parse the supplied arguments and extract their surplus value, like a capitalist
argspace = parser.parse_args()
inputFilename = argspace.File
outputFilename = argspace.outputName
doDate = argspace.doDate
outputInit()

# # # BEGIN TEST # # #

# # # END TEST # # #























# # # BEGIN TEST # # #

# # # END TEST # # #

