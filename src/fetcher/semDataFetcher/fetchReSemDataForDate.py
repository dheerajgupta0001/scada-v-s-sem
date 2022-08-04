import datetime as dt
#from src.typeDefs.pmuAvailabilitySummary import IPmuAvailabilitySummary
from typing import List
import os
import pandas as pd


def fetchReSemSummaryForDate(semReFolderPath: str, targetDt: dt.datetime, reName: str) -> List :
    """fetched scada sem re availability summary data rows for a date from excel file

    Args:
        targetDt (dt.datetime): date for which data is to be extracted

    Returns:
        List[]: list of sem data records fetched from the excel data
    """
    # sample excel filename - PMU_availability_Report_05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d%m%y')
    targetFilename = '{0}.{1}'.format(fileDateStr, 'IN7')
    if reName in ["EG-91", "GP-91", "TP-91"]:
        targetFilename = '{0}.{1}'.format(fileDateStr, 'RD1')
        
    if reName == "KR-91":
        targetFilename = '{0}.{1}'.format(fileDateStr, 'KR1')
    if reName == "GS-91":
        targetFilename = '{0}.{1}'.format(fileDateStr, 'RD1')
    if reName == "JM-91":
        targetFilename = '{0}.{1}'.format(fileDateStr, 'PW1')
    targetFilePath = os.path.join(semReFolderPath, targetFilename)
    # print(targetFilePath)

    # check if excel file is present
    if not os.path.isfile(targetFilePath):
        print("RE Sem file for date {0} is not present for state {1}".format(targetDt, reName))
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
        for rowInd in range(8,104):
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
    if reName == "OS-91":
        excelDf = excelDf.iloc[:, [0,17]]
        excelDf.rename(columns = {0: 'Timestamp', 17:'semData'}, inplace = True)
    elif reName == "AM-91":
        excelDf = excelDf.iloc[:, [0,18]]
        excelDf.rename(columns = {0: 'Timestamp', 18:'semData'}, inplace = True)
    elif reName == "MA-91":
        excelDf = excelDf.iloc[:, [0,19]]
        excelDf.rename(columns = {0: 'Timestamp', 19:'semData'}, inplace = True)
    elif reName == "AR-91":
        excelDf = excelDf.iloc[:, [0,20]]
        excelDf.rename(columns = {0: 'Timestamp', 20:'semData'}, inplace = True)
    elif reName == "RE-91":
        excelDf = excelDf.iloc[:, [0,21]]
        excelDf.rename(columns = {0: 'Timestamp', 21:'semData'}, inplace = True)
    elif reName == "GI-91":
        excelDf = excelDf.iloc[:, [0,22]]
        excelDf.rename(columns = {0: 'Timestamp', 22:'semData'}, inplace = True)
    elif reName == "GI-94":
        excelDf = excelDf.iloc[:, [0,23]]
        excelDf.rename(columns = {0: 'Timestamp', 23:'semData'}, inplace = True)
    elif reName == "IX-91":
        excelDf = excelDf.iloc[:, [0,24]]
        excelDf.rename(columns = {0: 'Timestamp', 24:'semData'}, inplace = True)
    elif reName == "AG-91":
        excelDf = excelDf.iloc[:, [0,25]]
        excelDf.rename(columns = {0: 'Timestamp', 25:'semData'}, inplace = True)
    elif reName == "AF-91":
        excelDf = excelDf.iloc[:, [0,26]]
        excelDf.rename(columns = {0: 'Timestamp', 26:'semData'}, inplace = True)
    elif reName == "GH-91":
        excelDf = excelDf.iloc[:, [0,27]]
        excelDf.rename(columns = {0: 'Timestamp', 27:'semData'}, inplace = True)
        
    elif reName == "AV-91":
        excelDf = excelDf.iloc[:, [0,32]]
        excelDf.rename(columns = {0: 'Timestamp', 32:'semData'}, inplace = True)

    elif reName == "EG-91":
        excelDf = excelDf.iloc[:, [0,5]]
        excelDf.rename(columns = {0: 'Timestamp', 5:'semData'}, inplace = True)
    elif reName == "GP-91":
        excelDf = excelDf.iloc[:, [0,6]]
        excelDf.rename(columns = {0: 'Timestamp', 6:'semData'}, inplace = True)
    elif reName == "TP-91":
        excelDf = excelDf.iloc[:, [0,7]]
        excelDf.rename(columns = {0: 'Timestamp', 7:'semData'}, inplace = True)
        
    # KAWAS-KR-91, GSECL-GS-91, POWERICA added
    elif reName in ["KR-91", "JM-91"]:
        excelDf = excelDf.iloc[:, [0,4]]
        excelDf.rename(columns = {0: 'Timestamp', 4:'semData'}, inplace = True)
    elif reName == "GS-91":
        excelDf = excelDf.iloc[:, [0,8]]
        excelDf.rename(columns = {0: 'Timestamp', 8:'semData'}, inplace = True)

    # convert string typed value '--' column to ZERO
    excelDf.loc[excelDf["semData"] == "--", "semData"] = 0
    # convert string typed column to float
    excelDf['semData'] = excelDf['semData'].astype(float)
    semData = excelDf["semData"].tolist()
    # print(semData)
    return semData