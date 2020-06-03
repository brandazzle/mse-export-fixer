import sys
import argparse
from argparse import ArgumentParser
import re
from datetime import date
from string import Template
from itertools import islice
from types import SimpleNamespace

version = ('0.5.1')

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
                    help = "set the set release date to today\'s date (default off)")
# third arg: flag for version number (exits the script if used)
parser.add_argument('--version', '-v', action='version',
                    version="fixer v" + version)
# fourth arg: what to name the output file
parser.add_argument('--outputname ', '-o', dest='outputName', default='set_fixed.xml',
                    help = "what to name the output (fixed) file. Defaults to set_fixed.xml")
# fifth arg: flag for verbosity option
#parser.add_argument('--verbose', dest='Verbose', action='store_true',
                    #help = "verbose extraction and construction")


def outputInit():
    """Initialize the output file.

Writes the standard .xml header, the Cockatrice card database tag,
and the set info block derived from the input file.
Returns the location of the </sets> tag in the input file,
as well as the set code."""
    with open(outputFilename, "wt") as Out: #open the output file
        Out.write('<?xml version="1.0" encoding="UTF-8"?>\n') #write the .xml general header
        Out.write('<cockatrice_carddatabase version="4">\n') #write the Cockatrice database header
    [setEnd,setBlock] = blockExtract('sets', 0) #extract the set info block
    tags = ['name','longname','settype','releasedate'] #the list of info tags that the set should have
    setInfo = infoExtract(setBlock, tags) #get the set info from the block
    fixInfo = setDiagnose(setInfo) #check for missing info
    newBlock = blockBuild(fixInfo, 'set') #build the new set info block
    with open(outputFilename, "at") as Out: # write set block and <cards> tag to output file
        Out.write('    <sets>\n')
        Out.write(newBlock)
        Out.write('    </sets>\n')
        Out.write('    <cards>\n')
    return [setEnd, fixInfo.name]


def blockExtract(tag, loc):
    """Extract an entire set or card info block from the input file."""
    start = '<' + tag + '>'
    end = '</' + tag + '>' #build matchable strings for the start and end tags
    ## open the input file and search for the first string enclosed by <tag></tag>
    block = ''
    with open(inputFilename, "rt") as In:
        i = loc
        sliced = islice(In, loc, None)
        for line in sliced:
            if re.search(start, line):
                block = line
                break
            else: i=i+1
    with open(inputFilename, "rt") as In:
        sliced2 = islice(In, i, None)
        for line in sliced2:
            block = block + line
            i = i+1
            if re.search(end, line):
                break
    endLoc = i
    return [endLoc, block]


def infoExtract(block, tags): # block should be the info block string, tags should be a list of info tags
    """Extract the info from a card or set info block."""
    info = SimpleNamespace() #define the block's info as a namespace object
    d = vars(info)
    for tag in tags:
        if (tag + '>') in block: #check if the tag is present (activates for <tag> or </tag>)
            try:
                regex = regex_temp.substitute({'tag' : tag}) #form the regex string
                found = re.search(regex, block, re.S) #search for the info in the block
                d[tag] = found.group(1) #assign the extracted info to the tag in the namespace
            except AttributeError:
                print("Missing <" + tag + "> or </" + tag + "> tag")
                # will only activate if one half of the tag wrapper is present but not the other
    return info


def blockBuild(info, blocktype):
    """Build a new set or card info block using an info namespace."""
    d = vars(info)
    if blocktype=='set':
        block = setBlock_temp.substitute(d)
    if blocktype=='card':
        #block = '        <card>\n            whatever\n        </card>\n'
        block = '        <card>\n'
        block += '            ' + singleInfo.substitute({'tag' : 'name', 'info' : d['name']})
        block += '            ' + singleInfo.substitute({'tag' : 'text', 'info' : d['text']})
        block += '            <prop>\n'
        for tag in generictags:
            if hasattr(info, tag):
                infoline = singleInfo.substitute({'tag' : tag, 'info' : d[tag]})
                block += '                ' + infoline
        block += '            </prop>\n'
        block += '            <set>' + setCode + '</set>\n'
        for tag in specialtags:
            if hasattr(info, tag):
                infoline = singleInfo.substitute({'tag' : tag, 'info' : d[tag]})
                block += '            ' + infoline
        block += '        </card>\n'
    return block


def outputFin():
    """Finalize the output file.

Writes the Cockatrice card database end tag to the output file.
Displays a success message, using the set code if it exists."""
    with open(outputFilename, "at") as Out:
        Out.write('\n    </cards>\n')
        Out.write('</cockatrice_carddatabase>')
    if setCode == ' ': #if the set had no name, meaning diagnostics set the name to a whitespace string
        endMessage = "Successfully wrote " + outputFilename
    else:
        endMessage = "Successfully wrote " + outputFilename + " for set " + setCode
    print(endMessage)


def main(cardsLoc):
    """Fix all card info blocks and write them to the output file."""
    nextCard = cardsLoc
    with open(inputFilename, "rt") as In:
        file = In.read()
        cardcount = file.count('<card>')
    cardnum = 1
    while cardnum <= cardcount:
        [nextCard,cardblock] = blockExtract('card', nextCard)
        cardInfo = infoExtract(cardblock, cardtags)
        fixInfo = cardDiagnose(cardInfo, cardnum)
        if DFC_check(fixInfo):
            newBlock = DFC_process(fixInfo)
        else:
            info = secondaryInfo(fixInfo)
            newBlock = blockBuild(info, 'card')
        with open(outputFilename, "at") as Out:
            Out.write(newBlock)
        cardnum = cardnum + 1

def setDiagnose(info):
    """Detect missing set info.

Sets noncritical info (date and set type) to defaults.
Sends messages for missing set name and set code."""
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


def cardDiagnose(info, cardNumber):
    """Detect missing critical card info."""
    return info


def DFC_check(info):
    """Check if a card is double-faced."""
    if '//' in info.type:
        isDFC = True
    else:
        isDFC = False
    return isDFC


def secondaryInfo(info):
    """Process additional card info from extracted info."""
    return info


def cmc(manacost):
    """Determine a card's converted mana cost."""
    pass


def color(manacost, cardtext):
    """Determine a card's color."""
    pass


def coloridentity(manacost, cardtext):
    """Determine a card's color identity."""
    pass


def token(cardtext):
    """Determine tokens to associate."""
    pass


def dual_check(info):
    """Check if a card is a dual card."""
    if '//' in info.name:
        isDual = True
    else:
        isDual = False
    return isDual


def DFC_process(info):
    """Process double-faced card info."""
    block = 'placeholder'
    return block


### String templates

singleInfo = Template('<$tag>$info</$tag>\n') #output template for a single pair of [tag, info]

setBlock_temp = Template('        <set>\n' +
                         '            <name>$name</name>\n' +
                         '            <longname>$longname</longname>\n' +
                         '            <settype>$settype</settype>\n' +
                         '            <releasedate>$releasedate</releasedate>\n' +
                         '        </set>\n') #output template for a set info block

# template for the regex string for finding info for a given tag
regex_temp = Template('<$tag>(.+?)</$tag>')


### Global lists

colors = ['R','W','G','U','B'] #list of mana colors for determining card color or color identity

# list of possible card info tags
cardtags = ['name','text','layout','side','type','maintype','manacost','cmc','colors','coloridentity',
            'pt','loyalty','related','reverse-related','token','tablerow','cipt','upsidedown']
# list of generic card info tags, i.e. those that go in the <prop> tag block
generictags = ['layout','side','type','maintype','manacost','cmc','colors',
               'coloridentity','pt','loyalty']
# tags that go between </prop> and </card>
specialtags = ['related','reverse-related','token','tablerow','cipt','upsidedown']


### BEGIN TEST ###
argspace = parser.parse_args(['/Users/BrandonPlay/Documents/Eragon/testset.xml'])
### END TEST ###

### Initialize the application

## parse the supplied arguments and extract their surplus value, like a capitalist
#argspace = parser.parse_args()
inputFilename = argspace.File
outputFilename = argspace.outputName
doDate = argspace.doDate

[cardsLoc, setCode] = outputInit() #conduct output initialization,
# retrieving card info start location and set code into global variables

main(cardsLoc) #activate main processing starting at start of card info

outputFin() #finalize the output file

