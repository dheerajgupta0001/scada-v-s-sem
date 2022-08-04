import datetime as dt
from typing import List
import os
import pandas as pd


def fetchIsgsSemSummaryForDate(semIsgsFolderPath: str, targetDt: dt.datetime, isgsName: str) -> List:
    """fetched scada sem re availability summary data rows for a date from excel file

    Args:
        targetDt (dt.datetime): date for which data is to be extracted

    Returns:
        List[]: list of sem data records fetched from the excel data
    """
    # sample excel filename - PMU_availability_Report_05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d%m%y')
    # if isgsName == "AC-91":
    #     targetFilename = '{0}.{1}'.format(fileDateStr, 'AC1')
    if isgsName in ["AC-91", "BL-91", "CG-91", "DB-91", "DC-91", "DG-91", "DW-91", "EM-91", "GA-91", "GM-91", "JD-96", "JD-97", "JH-91", "JY-91", "KA-91", "KB-91", "KO-97", "KO-98", "KS-91", "KW-91", "LK-91", "MB-91", "MD-96", "MD-97", "MN-91", "NS-91", "RG-91", "RK-91", "SA-91"]:
        targetFilename = '{0}.{1}'.format(fileDateStr, 'IN6')
    else:
        targetFilename = '{0}.{1}'.format(fileDateStr, 'IN7')
    targetFilePath = os.path.join(semIsgsFolderPath, targetFilename)
    print(targetFilePath)

    # check if excel file is present
    if not os.path.isfile(targetFilePath):
        print("ISGS Sem file for date {0} is not present for state {1}".format(
            targetDt, isgsName))
        return []

    # read notepad type file format r"C:\Users\dheer\Desktop\example.txt",'r'
    with open(targetFilePath, mode='r') as f:
        # read all the file content
        fLines = f.read()
        fLines = fLines.replace('\x00', '').replace('\n\n', '\n').split('\n')
        # read header from first line
        # dfCols = fLines[7].split(',')[2:-1]
        schDfRows = []
        # read the values from line 9 to 104 NOTE: same text file format is for CS1, DD1, DN1, GO1, MP2, GU2, HZ1
        for rowInd in range(8, 104):
            # read the data line
            dataRowVals = fLines[rowInd].split()
            dataRowVals = [k for k in dataRowVals[0:]]
            # print("row")
            # print(dataRowVals)
            schDfRows.append(dataRowVals)
        excelDf = pd.DataFrame(data=schDfRows)
    # print(excelDf)
    # print(excelDf.columns)
    if isgsName in ["SK-91", "AC-91"]:
        excelDf = excelDf.iloc[:, [0, 2]]
        excelDf.rename(columns={0: 'Timestamp', 2: 'semData'}, inplace=True)

    # elif isgsName in ["AC-91"]:
    #     schDfRows = []
    #     # read the values from line 10 to 105
    #     for rowInd in range(9, 105):
    #         # read the data line
    #         dataRowVals = fLines[rowInd].split()
    #         dataRowVals = [k for k in dataRowVals[0:]]
    #         # print("row")
    #         # print(dataRowVals)
    #         schDfRows.append(dataRowVals)
    #     excelDf = pd.DataFrame(data=schDfRows)
    #     excelDf = excelDf.iloc[:, [0, 6]]
    #     excelDf.rename(columns={0: 'Timestamp', 6: 'semData'}, inplace=True)
    elif isgsName in ["BL-91", "SP-91"]:
        excelDf = excelDf.iloc[:, [0, 3]]
        excelDf.rename(columns={0: 'Timestamp', 3: 'semData'}, inplace=True)
    elif isgsName in ["CG-91", "SS-91"]:
        excelDf = excelDf.iloc[:, [0, 4]]
        excelDf.rename(columns={0: 'Timestamp', 4: 'semData'}, inplace=True)
    elif isgsName in ["DB-91", "TA-91"]:
        excelDf = excelDf.iloc[:, [0, 5]]
        excelDf.rename(columns={0: 'Timestamp', 5: 'semData'}, inplace=True)
    elif isgsName in ["DC-91", "TA-94"]:
        excelDf = excelDf.iloc[:, [0, 6]]
        excelDf.rename(columns={0: 'Timestamp', 6: 'semData'}, inplace=True)
    elif isgsName in ["DG-91", "TR-91"]:
        excelDf = excelDf.iloc[:, [0, 7]]
        excelDf.rename(columns={0: 'Timestamp', 7: 'semData'}, inplace=True)
    elif isgsName in ["DW-91", "VI-96"]:
        excelDf = excelDf.iloc[:, [0, 8]]
        excelDf.rename(columns={0: 'Timestamp', 8: 'semData'}, inplace=True)
    elif isgsName in ["EM-91", "VI-97"]:
        excelDf = excelDf.iloc[:, [0, 9]]
        excelDf.rename(columns={0: 'Timestamp', 9: 'semData'}, inplace=True)
    elif isgsName in ["GA-91", "VI-99"]:
        excelDf = excelDf.iloc[:, [0, 10]]
        excelDf.rename(columns={0: 'Timestamp', 10: 'semData'}, inplace=True)
    elif isgsName in ["GM-91", "VI-V4"]:
        excelDf = excelDf.iloc[:, [0, 11]]
        excelDf.rename(columns={0: 'Timestamp', 11: 'semData'}, inplace=True)
    elif isgsName in ["JD-96", "VI-V5"]:
        excelDf = excelDf.iloc[:, [0, 12]]
        excelDf.rename(columns={0: 'Timestamp', 12: 'semData'}, inplace=True)
    elif isgsName in ["JD-97", "SO-91"]:
        excelDf = excelDf.iloc[:, [0, 13]]
        excelDf.rename(columns={0: 'Timestamp', 13: 'semData'}, inplace=True)
    elif isgsName in ["JH-91", "LA-91"]:
        excelDf = excelDf.iloc[:, [0, 14]]
        excelDf.rename(columns={0: 'Timestamp', 14: 'semData'}, inplace=True)
    elif isgsName in ["JY-91", "GD-91"]:
        excelDf = excelDf.iloc[:, [0, 15]]
        excelDf.rename(columns={0: 'Timestamp', 15: 'semData'}, inplace=True)
    elif isgsName in ["KA-91", "KH-91"]:
        excelDf = excelDf.iloc[:, [0, 16]]
        excelDf.rename(columns={0: 'Timestamp', 16: 'semData'}, inplace=True)
    elif isgsName == "KB-91":
        excelDf = excelDf.iloc[:, [0, 17]]
        excelDf.rename(columns={0: 'Timestamp', 17: 'semData'}, inplace=True)
    elif isgsName == "KO-97":
        excelDf = excelDf.iloc[:, [0, 18]]
        excelDf.rename(columns={0: 'Timestamp', 18: 'semData'}, inplace=True)
    elif isgsName == "KO-98":
        excelDf = excelDf.iloc[:, [0, 19]]
        excelDf.rename(columns={0: 'Timestamp', 19: 'semData'}, inplace=True)
    elif isgsName == "KS-91":
        excelDf = excelDf.iloc[:, [0, 20]]
        excelDf.rename(columns={0: 'Timestamp', 20: 'semData'}, inplace=True)
    elif isgsName == "KW-91":
        excelDf = excelDf.iloc[:, [0, 21]]
        excelDf.rename(columns={0: 'Timestamp', 21: 'semData'}, inplace=True)
    elif isgsName == "LK-91":
        excelDf = excelDf.iloc[:, [0, 22]]
        excelDf.rename(columns={0: 'Timestamp', 22: 'semData'}, inplace=True)
    elif isgsName == "MB-91":
        excelDf = excelDf.iloc[:, [0, 23]]
        excelDf.rename(columns={0: 'Timestamp', 23: 'semData'}, inplace=True)
    elif isgsName == "MD-96":
        excelDf = excelDf.iloc[:, [0, 24]]
        excelDf.rename(columns={0: 'Timestamp', 24: 'semData'}, inplace=True)
    elif isgsName == "MD-97":
        excelDf = excelDf.iloc[:, [0, 25]]
        excelDf.rename(columns={0: 'Timestamp', 25: 'semData'}, inplace=True)
    elif isgsName == "MN-91":
        excelDf = excelDf.iloc[:, [0, 26]]
        excelDf.rename(columns={0: 'Timestamp', 26: 'semData'}, inplace=True)
    elif isgsName == "NS-91":
        excelDf = excelDf.iloc[:, [0, 27]]
        excelDf.rename(columns={0: 'Timestamp', 27: 'semData'}, inplace=True)
    elif isgsName == "RG-91":
        excelDf = excelDf.iloc[:, [0, 28]]
        excelDf.rename(columns={0: 'Timestamp', 28: 'semData'}, inplace=True)
    elif isgsName == "RK-91":
        excelDf = excelDf.iloc[:, [0, 29]]
        excelDf.rename(columns={0: 'Timestamp', 29: 'semData'}, inplace=True)
    elif isgsName == "SA-91":
        excelDf = excelDf.iloc[:, [0, 30]]
        excelDf.rename(columns={0: 'Timestamp', 30: 'semData'}, inplace=True)
    # elif isgsName == "SK-91":
    #     excelDf = excelDf.iloc[:, [0, 2]]
    #     excelDf.rename(columns={0: 'Timestamp', 2: 'semData'}, inplace=True)
    
    # print(excelDf)
    # convert string typed value '--' column to ZERO
    excelDf.loc[excelDf["semData"] == "--", "semData"] = 0
    # convert string typed column to float
    excelDf['semData'] = excelDf['semData'].astype(float)
    # print(excelDf)
    semData = excelDf["semData"].tolist()
    return semData
