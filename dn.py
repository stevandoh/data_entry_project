import os
import sys
import pdfplumber

from collections import OrderedDict
from PyPDF2 import PdfFileReader


def getfiles():
    return [file for root, dirs, files in os.walk(os.path.abspath(os.getcwd())) for file in files if
            file.endswith(".pdf".lower())]

def readini(fname):
    # Instruction(s) to read an .ini file go here (and/or below)...

def getformfields(obj, tree=None, retval=None, fileobj=None):
    # Check resource: How to extract PDF fields from a filled-out form in Python

# fn is the name of the file to analyze...
def getfields(fn):
    # Do something here...
    fields = getformfields(pdf)
    # Do something here...
    return OrderedDict((k, v.get('/V', '')) for k, v in fields.items())


# fn is the name of the file to analyze...
# kw are marker keywords to look for...
# i1 and i2 are the names of the .ini files...
def gettextfields(kw, i1, i2, fn):
    # Do something here...
    pgtxt = page.extract_text()
    if kw.lower() in pgtxt.lower():
        # Do something here...
        for i, l in enumerate(txt):
        # Do something here...
        pdf.close()
    return dict(res)


def execute():
    try:
        i1 = readini('l1.ini') # Read the 1st .ini file
        i2 = readini('l2.ini') # Read the 2nd .ini file
        # Read fields for each file (instructions are missing here)
        # Both getfields and gettextfields should be invoked
    except BaseException as msg:
        print('Error occured: ' + str(msg))

if __name__ == '__main__':
    execute()

print(getfiles())
