import numpy
import sys
import argparse
from argparse import ArgumentParser
import math
import re
from datetime import date
from string import Template

version = ('0.1.2')

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
                    version = 'fixer v%(version)s')
parser.add_argument('--outputname', '-o', dest='outputName',
                    help = 'what to name the output (fixed) file. Defaults to set_fixed.xml')

#get the supplied arguments out of sys.argv and parse them
rawArgs = sys.argv
args = parser.parse_args(rawArgs)

#get the current date and put it in the correct string format
today = date.today()
date = today.strftime("%Y-%m-%d")


# # # BEGIN TEST # # #
dateTest = 'Today\'s date: ' + date + '\n'
fileTest = 'Input file: ' + '\n'
doDatestampTest = 'Datestamp?' + '\n'

print dateTest
print fileTest
print doDatestampTest
# # # END TEST # # #
