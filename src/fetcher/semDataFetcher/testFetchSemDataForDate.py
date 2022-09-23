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
    targetFilename = '{0}.DR3.csv'.format(fileDateStr, stateName)
    targetFilePath = os.path.join(scadaSemFolderPath, targetFilename)
    # print(targetFilePath)

    # check if excel file is present
    if not os.path.isfile(targetFilePath):
        print("Sem file for date {0} is not present for state {1}".format(targetDt, stateName))
        return [] 

    excelDf = pd.read_csv(targetFilePath, skipfooter= 1)
    if stateName == "GO1":
        excelDf = excelDf[['TIME', 'GO-901']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'GO-901':'semData'}, inplace = True)
        # print(excelDf)
    elif stateName == "BR1":
        excelDf = excelDf[['TIME', 'BR-901']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'BR-901':'semData'}, inplace = True)
    elif stateName == "TD1":
        excelDf['DDDNH'] = excelDf['DD-901'] + excelDf['DN-901']
        excelDf = excelDf[['TIME', 'DDDNH']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'DDDNH':'semData'}, inplace = True)
    elif stateName == "CS1":
        excelDf = excelDf[['TIME', 'CS-901']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'CS-901':'semData'}, inplace = True)
    elif stateName == "MP2":
        excelDf = excelDf[['TIME', 'MP-901']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'MP-901':'semData'}, inplace = True)
    elif stateName == "GU2":
        excelDf = excelDf[['TIME', 'GU-901']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'GU-901':'semData'}, inplace = True)
    elif stateName == "HZ1":
        excelDf = excelDf[['TIME', 'HZ-901']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'HZ-901':'semData'}, inplace = True)
    elif stateName == "MH2":
        excelDf = excelDf[['TIME', 'MH-901']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'MH-901':'semData'}, inplace = True)
    elif stateName == "NR1":
        excelDf = excelDf[['TIME', 'NR-901']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'NR-901':'semData'}, inplace = True)
        excelDf['semData'] = -1*excelDf['semData']
    elif stateName == "ER1":
        excelDf = excelDf[['TIME', 'ER-901']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'ER-901':'semData'}, inplace = True)
        excelDf['semData'] = -1*excelDf['semData']
    elif stateName == "SR1":
        excelDf = excelDf[['TIME', 'SR-901']]
        excelDf.rename(columns = {'TIME': 'Timestamp', 'SR-901':'semData'}, inplace = True)
        excelDf['semData'] = -1*excelDf['semData']
    # convert string typed column to float
    excelDf['semData'] = excelDf['semData'].astype(float)
    semData = excelDf["semData"].tolist()
    # print(excelDf)
    return semData