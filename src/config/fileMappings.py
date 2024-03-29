import json
from typing import List
import pandas as pd

# fileMappings = []
fileMappingsDf = pd.DataFrame()
isgsMappingsDf = pd.DataFrame()
reMappingsDf = pd.DataFrame()
linesMappingsDf = pd.DataFrame()

jsonConfig: dict = {}

def initConfigs():
    loadIsgsMappings()
    loadReMappings()
    loadLinesMappings()


def loadIsgsMappings(filePath='Mapping.xlsx'):
    global isgsMappingsDf
    isgsMappingsDf = pd.read_excel(filePath, sheet_name= 'ISGS')
    return isgsMappingsDf

def getIsgsMappings():
    global isgsMappingsDf
    return isgsMappingsDf

def loadReMappings(filePath='Mapping.xlsx'):
    global reMappingsDf
    reMappingsDf = pd.read_excel(filePath, sheet_name= 'RE')
    return reMappingsDf

def getReMappings():
    global reMappingsDf
    return reMappingsDf

def loadLinesMappings(filePath='Mapping.xlsx'):
    global linesMappingsDf
    linesMappingsDf = pd.read_excel(filePath, sheet_name= 'Lines')
    return linesMappingsDf

def getLinesMappings():
    global linesMappingsDf
    return linesMappingsDf


