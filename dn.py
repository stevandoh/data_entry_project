import os
import sys


def getfiles():
    return [file for root, dirs, files in os.walk(os.path.abspath(os.getcwd())) for file in files if
            file.endswith(".pdf".lower())]


print(getfiles())
