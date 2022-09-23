import datetime as dt
#from src.typeDefs.pmuAvailabilitySummary import IPmuAvailabilitySummary
from typing import List
import os
import pandas as pd


def fetchSemSummaryForDate(scadaSemFolderPath: str, targetDt: dt.datetime, stateName: str) -> List :
    """fetched pmu availability summary data rows for a date from excel file

    Args:
        targetDt (dt.datetime): date for which data is to be extracted

    Returns:
        List[]: list of sem data records fetched from the excel data
    """
    # sample excel filename - PMU_availability_Report_05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d%m%y')
    targetFilename = '{0}.{1}'.format(fileDateStr, stateName)
    targetFilePath = os.path.join(scadaSemFolderPath, targetFilename)
    # print(targetFilePath)

    # check if excel file is present
    if not os.path.isfile(targetFilePath):
        print("Sem file for date {0} is not present for state {1}".format(targetDt, stateName))
        return [] 

    # read notepad type file format r"C:\Users\DEVANSH SHARMA\Desktop\example.txt",'r'
    with open(targetFilePath, mode='r') as f:
        # read all the file content   
        fLines = f.read()
        fLines = fLines.replace('\x00','').replace('\n\n', '\n').split('\n')
        # read header from first line
        # dfCols = fLines[7].split(',')[2:-1]
        schDfRows = []
        # read the values from line 10 to 105 NOTE: same text file format is for CS1, DD1, DN1, GO1, MP2, GU2, HZ1
        for rowInd in range(9,105):
            # read the data line
            dataRowVals = fLines[rowInd].split()
            dataRowVals = [k for k in dataRowVals[0:]]
            # print("row")
            # print(dataRowVals)
            schDfRows.append(dataRowVals)
        excelDf = pd.DataFrame(data=schDfRows)
    # print(excelDf)
    # append previous code
    # excelDf = pd.read_excel(targetFilePath, skiprows=9, skipfooter=3, header=None)
    if stateName == "TD1":
        excelDf = excelDf.iloc[:, [0,30]]
        excelDf.rename(columns = {0: 'Timestamp', 30:'semData'}, inplace = True)
        # print(excelDf)
    # elif stateName == "DD1":
    #     excelDf = excelDf.iloc[:, [0,11]]
    #     excelDf.rename(columns = {0: 'Timestamp', 11:'semData'}, inplace = True)
    elif stateName == "GO1":
        excelDf = excelDf.iloc[:, [0,8]]
        excelDf.rename(columns = {0: 'Timestamp', 8:'semData'}, inplace = True)
    elif stateName == "CS1":
        excelDf = excelDf.iloc[:, [0,32]]
        excelDf.rename(columns = {0: 'Timestamp', 32:'semData'}, inplace = True)
    elif stateName == "MP2":
        excelDf = excelDf.iloc[:, [0,32]]
        excelDf.rename(columns = {0: 'Timestamp', 32:'semData'}, inplace = True)
    elif stateName == "GU2":
        excelDf = excelDf.iloc[:, [0,32]]
        excelDf.rename(columns = {0: 'Timestamp', 32:'semData'}, inplace = True)
    elif stateName == "HZ1":
        excelDf = excelDf.iloc[:, [0,5]]
        excelDf.rename(columns = {0: 'Timestamp', 5:'semData'}, inplace = True)
    elif stateName == "BR1":
        excelDf = excelDf.iloc[:, [0,8]]
        excelDf.rename(columns = {0: 'Timestamp', 8:'semData'}, inplace = True)
    elif stateName == "MH2" or stateName == "NR1" or stateName == "ER1":
        # excelDf = pd.read_excel(targetFilePath, skiprows=8, skipfooter=3, header=None)
        schDfRows = []
        # read the values from line 9 to 104 NOTE: same text file format is for MH2, NR1, ER1
        for rowInd in range(8,104):
            # read the data line
            dataRowVals = fLines[rowInd].split()
            dataRowVals = [k for k in dataRowVals[0:]]
            # print("row")
            # print(dataRowVals)
            schDfRows.append(dataRowVals)
        excelDf = pd.DataFrame(data=schDfRows)
        if stateName == "MH2" or stateName == "NR1":
            excelDf = excelDf.iloc[:, [0,30]]
            excelDf.rename(columns = {0: 'Timestamp', 30:'semData'}, inplace = True)
        elif stateName == "ER1":
            excelDf = excelDf.iloc[:, [0,20]]
            excelDf.rename(columns = {0: 'Timestamp', 20:'semData'}, inplace = True)
    elif stateName == "SR1":
        schDfRows = []
        # read the values from line 8 to 103
        for rowInd in range(7,103):
            # read the data line
            dataRowVals = fLines[rowInd].split()
            dataRowVals = [k for k in dataRowVals[0:]]
            # print("row")
            # print(dataRowVals)
            schDfRows.append(dataRowVals)
        excelDf = pd.DataFrame(data=schDfRows)
        excelDf = excelDf.iloc[:, [0,15]]
        excelDf.rename(columns = {0: 'Timestamp', 15:'semData'}, inplace = True)
    # convert string typed column to float
    excelDf['semData'] = excelDf['semData'].astype(float)
    semData = excelDf["semData"].tolist()
    # print(excelDf)
    return semData