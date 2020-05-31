import numpy
import sys
import argparse
from argparse import ArgumentParser
import math
import re
from datetime import date
from string import Template

version = ('0.2.1')

# get the current date and put it in the correct string format
today = date.today()
date = today.strftime("%Y-%m-%d")

### command line argument parsing 
## define the argument parser
parser = ArgumentParser(description = 'Fix a Cockatrice .xml file exported from MSE')
# first arg: file to be fixed
parser.add_argument('File', help = 'the .xml file to fix')
# second arg: file datestamping flag
parser.add_argument('--date', '-d', dest='doDate', action='store_true', 
                    help = 'datestamp the fixed file with today\'s date (default off)')
# third arg: flag for version number (exits the script if used)
parser.add_argument('--version', '-v', action='version',
                    version='fixer v' + version)
# fourth arg: what to name the output file
parser.add_argument('--outputname', '-o', dest='outputName', default='set_fixed.xml',
                    help = 'what to name the output (fixed) file. Defaults to set_fixed.xml')

### output initialization function
def outputInit():
    # open the output file
    out = open(outputFilename, "at")
    # write the xml general header
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    # write the cockatrice xml header
    out.write('<cockatrice_carddatabase version="4">\n')
    
    # open the input file 
    
    out.close()




### String templates for output

## Tagged info templates
# template for a single pair of [tag, info]
singleinfo = Template('<$tag>$info</$tag>')




### Initialize the application

# # # BEGIN TEST # # #
argspace = parser.parse_args(['obj.xml'])
# # # END TEST # # #
    
## parse the supplied arguments and extract their surplus value, like a capitalist
#argspace = parser.parse_args()
inputFilename = argspace.File
outputFilename = argspace.outputName
doDate = argspace.doDate
outputInit()

# # # BEGIN TEST # # #
out = open(outputFilename, "r")
print out.read()
# # # END TEST # # #
