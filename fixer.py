import sys
import argparse
from argparse import ArgumentParser as argParse
import math
import re
import pandas as pd
from datetime import date
import tkinter as tk
from tkinter import filedialog

version = ('0.1')

#Set defaults for option variables
doDateReplace = True

#



#get the current date
today = date.today()
#check if the set should be datestamped
if len(sys.argv) >= 2:
    date = today.strftime("%Y-%m-%d")
    doDateReplace = True
    else doDateReplace = False

#
#BEGIN PROCEDURE
#

#first find the set definition and fix it.



#then for each card (a string of text beginning in <card> and ending in </card>)

#follow these steps:


#first, split into chunks of info that can be manipulated together


def cardInfo(info):


    
    return name, text, props, setInfo

#function for a
def addLine():
    outFile = 1
