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
    if reName in ["OS-91", "AM-91", "MA-91", "AR-91", "RE-91", "GI-91", "GI-94", "IX-91", "AG-91", "AF-91", "GH-91",
                  "EG-91", "GP-91", "TP-91", "AV-91"]:
        fileExtName = 'IN7'
    elif reName in ["KR-91", "GS-91"]:
        fileExtName = 'IN6'
    elif reName in ["JM-91", "CR-91", "MJ-91", "GR-91"]:
        fileExtName = 'IN4'
    fileDateStr = dt.datetime.strftime(targetDt, '%d%m%y')
    targetFilename = '{0}.{1}.csv'.format(fileDateStr, fileExtName)
    targetFilePath = os.path.join(semReFolderPath, targetFilename)
    # print(targetFilePath)

    # check if excel file is present
    if not os.path.isfile(targetFilePath):
        print("RE Sem file for date {0} is not present for state {1}".format(targetDt, reName))
        return [] 
    excelDf = pd.read_csv(targetFilePath, skipfooter= 1)
    
    # excelDf = pd.read_excel(targetFilePath, skiprows=9, skipfooter=3, header=None)
    if reName == "OS-91":
        excelDf = excelDf[['TIME', '(OS-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(OS-91)':'semData'}, inplace = True)
    elif reName == "AM-91":
        excelDf = excelDf[['TIME','(AM-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(AM-91)':'semData'}, inplace = True)
    elif reName == "MA-91":
        excelDf = excelDf[['TIME','(MA-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(MA-91)':'semData'}, inplace = True)
    elif reName == "AR-91":
        excelDf = excelDf[['TIME','(AR-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(AR-91)':'semData'}, inplace = True)
    elif reName == "RE-91":
        excelDf = excelDf[['TIME','(RE-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(RE-91)':'semData'}, inplace = True)
    elif reName == "GI-91":
        excelDf = excelDf[['TIME','(GI-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(GI-91)':'semData'}, inplace = True)
    elif reName == "GI-94":
        excelDf = excelDf[['TIME','(GI-94)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(GI-94)':'semData'}, inplace = True)
    elif reName == "IX-91":
        excelDf = excelDf[['TIME','(IX-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(IX-91)':'semData'}, inplace = True)
    elif reName == "AG-91":
        excelDf = excelDf[['TIME','(AG-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(AG-91)':'semData'}, inplace = True)
    elif reName == "AF-91":
        excelDf = excelDf[['TIME','(AF-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(AF-91)':'semData'}, inplace = True)
    elif reName == "GH-91":
        excelDf = excelDf[['TIME','(GH-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(GH-91)':'semData'}, inplace = True)
    elif reName == "AV-91":
        excelDf = excelDf[['TIME','(AV-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(AV-91)':'semData'}, inplace = True)
    elif reName == "EG-91":
        excelDf = excelDf[['TIME','(EG-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(EG-91)':'semData'}, inplace = True)
    elif reName == "GP-91":
        excelDf = excelDf[['TIME','(GP-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(GP-91)':'semData'}, inplace = True)
    elif reName == "TP-91":
        excelDf = excelDf[['TIME','(TP-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(TP-91)':'semData'}, inplace = True)
    elif reName == "KR-91":
        excelDf = excelDf[['TIME','(KR-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(KR-91)':'semData'}, inplace = True)
    elif reName == "GS-91":
        excelDf = excelDf[['TIME','(GS-91)']]
        excelDf.rename(columns = {'TIME': 'Timestamp', '(GS-91)':'semData'}, inplace = True)
    elif reName == "JM-91":
        excelDf = excelDf[['TIME','POWERICA WIND']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'POWERICA WIND':'semData'}, inplace = True)
    elif reName == "CR-91":
        excelDf = excelDf[['TIME','SKRPL WIND INJECTION']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'SKRPL WIND INJECTION':'semData'}, inplace = True)
    elif reName == "MJ-91":
        excelDf = excelDf[['TIME','SESPL WIND']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'SESPL WIND':'semData'}, inplace = True)
    elif reName == "GR-91":
        excelDf = excelDf[['TIME','Gandhar SOLAR INJECTION']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'Gandhar SOLAR INJECTION':'semData'}, inplace = True)

    # convert string typed value '--' column to ZERO
    excelDf.loc[excelDf["semData"] == "--", "semData"] = 0
    # convert string typed column to float
    excelDf['semData'] = excelDf['semData'].astype(float)
    semData = excelDf["semData"].tolist()
    # print(semData)
    return semData