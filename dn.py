import os
import sys
import pdfplumber

from collections import OrderedDict
from PyPDF2 import PdfFileReader

FORMAT_ONE_IDENTITIER = 'ALBARAN Nº'
FORMAT_TWO_IDENTITIER = 'TALLER'


def getfiles():
    return [file for root, dirs, files in os.walk(os.path.abspath(os.getcwd())) for file in files if
            file.endswith(".pdf".lower())]


def readini(filename):
    '''Reads the ini-files values and returns a Ordered dictionary.'''

    config = configparser.ConfigParser(delimiters=('=', '|'), dict_type=OrderedDict, default_section="[DEFAULT]")
    with open(filename) as file:
        lines = ("[DEFAULT]\n" + file.read())
        config.read_string(lines)
        return config


def getformfields(pdf, tree=None, retval=None, fileobj=None):
    ''' Returns PDF fields found with PyPDF2 getFields. '''

    return OrderedDict([(key, value) for key, item in pdf.getFields(tree=tree, retval=retval, fileobj=fileobj).items()
                        for innerKey, value in item.items() if innerKey == '/V'
                        ])


def getfields(filename):
    '''gets Fields from PDF and removes unneeded values.'''

    with open(filename, 'rb') as file:
        pdf = PdfFileReader(file)
        return getformfields(pdf)


def filterFunction(value):
    return lambda entry: (entry if entry else '').lower().find(value.lower()) != -1


def filter(entries, testfunction):
    '''Finds the index of a entry in a list, where the return function returns True.'''

    return next(idx for idx, entry in enumerate(entries) if testfunction(entry))


def gettextfields(iniFile1, iniFile2, filename):
    '''Read the Needed Text-fields out of PDF depending on format'''

    textFields = OrderedDict()
    with pdfplumber.open(filename) as pdf:
        firstPage = pdf.pages[0]

        firstPageContent = firstPage.extract_text()
        # TODO: refactor to only extract once the text
        firstPageTableContent = firstPage.extract_tables()

        if firstPageContent.find(FORMAT_ONE_IDENTITIER) != -1:
            firstPageTableContent = firstPageTableContent[0]

            for key, value in iniFile1["DEFAULT"].items():
                if len(value) > 1:
                    index = filter(firstPageTableContent[0], filterFunction(value))

                    if index > -1:
                        textFields[key] = firstPageTableContent[1][index]

        elif firstPageContent.find(FORMAT_TWO_IDENTITIER) != -1:
            firstPageTableContent = firstPageTableContent[1]

            # TODO: refactor duplication
            for key, value in iniFile2["DEFAULT"].items():
                if len(value) > 1:
                    index = filter(firstPageTableContent[0], filterFunction(value))
                    if index > -1:
                        textFields[key] = firstPageTableContent[0][index].split('\n')[1]

        else:
            raise TypeError("PDF DN Format not recognised.")

    return textFields


def createScriptForFile(filename, fields):
    scriptCommandLines = []

    for key, value in fields.items():
        scriptCommandLines.append(f'$("[id=\'{key}\' i]").val("{value}");')

    with open(filename, "w") as scriptFile:
        scriptFile.write("\n".join(scriptCommandLines))

    print("\n".join(scriptCommandLines))


def execute():
    '''starts the pdf parsing and field grabbing.'''

    try:
        filesFolder = os.path.join(os.getcwd(), 'formats')
        baseFolder = os.path.dirname(os.path.realpath(__file__))
        scriptsFolder = os.path.join(baseFolder, 'scripts')

        ini1FileName = os.path.join(baseFolder, 'l1.ini')
        ini2FileName = os.path.join(baseFolder, 'l2.ini')

        iniFile1 = readini(ini1FileName)
        iniFile2 = readini(ini2FileName)

        files = getfiles(filesFolder)
        for file in files:
            scriptFilename = os.path.join(scriptsFolder, file.split(os.sep)[-1].replace('.pdf', '.js'))
            # print(getfields(file))
            # print(gettextfields(iniFile1, iniFile2, file))

            fields = getfields(file)
            fields.update(gettextfields(iniFile1, iniFile2, file))

            createScriptForFile(scriptFilename, fields)

    except BaseException as msg:
        print('Error occured: ' + str(msg))


if __name__ == '__main__':
    execute()
