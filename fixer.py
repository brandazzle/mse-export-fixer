import numpy
import sys
import argparse
from argparse import ArgumentParser
import math
import re
from datetime import date
from string import Template

version = ('0.1.4')

#get the current date and put it in the correct string format
today = date.today()
date = today.strftime("%Y-%m-%d")

### command line argument parsing 
##define the argument parser
parser = ArgumentParser(description = 'Fix a Cockatrice .xml file exported from MSE')
#first arg: file to be fixed
parser.add_argument('File', help = 'the .xml file to fix')
#second arg: file datestamping flag
parser.add_argument('--date', '-d', dest='doDate', action='store_true', 
                    help = 'datestamp the fixed file with today\'s date (default off)')
#third arg: flag for version number (exits the script if used)
parser.add_argument('--version', '-v', action='version',
                    version='fixer v' + version)
#fourth arg: what to name the output file
parser.add_argument('--outputname', '-o', dest='outputName', default='set_fixed.xml',
                    help = 'what to name the output (fixed) file. Defaults to set_fixed.xml')

##parse the supplied arguments and extract their surplus value, like a capitalist
argspace = parser.parse_args()
inputFilename = argspace.File
outputFilename = argspace.outputName
doDate = argspace.doDate

##open the input file
infile = open(inputFilename, "r")
##open the output file in append mode
outfile = open(outputFilename, "at")
