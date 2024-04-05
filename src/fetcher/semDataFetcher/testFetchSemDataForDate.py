import datetime as dt
#from src.typeDefs.pmuAvailabilitySummary import IPmuAvailabilitySummary
from typing import List
import os
import pandas as pd
from urllib.parse import urljoin

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
    targetFilePath = urljoin(scadaSemFolderPath, targetFilename)
    # targetFilePath = os.path.join(scadaSemFolderPath, targetFilename)
    # print(targetFilePath)

    # check if excel file is present
    # if not os.path.isfile(targetFilePath):
    #     print("Sem file for date {0} is not present for state {1}".format(targetDt, stateName))
    #     return [] 

    excelDf = pd.read_csv(targetFilePath, skipfooter= 1, skiprows= 1)
    if stateName == "GO1":
        excelDf = excelDf[['GO-91']]
        excelDf.rename(columns = {'GO-91':'semData'}, inplace = True)
        # print(excelDf)
    elif stateName == "BR1":
        excelDf = excelDf[['BR-91']]
        excelDf.rename(columns = {'BR-91':'semData'}, inplace = True)
    elif stateName == "TD1":
        excelDf['DDDNH'] = excelDf['DD-91'] + excelDf['DN-91']
        excelDf = excelDf[['DDDNH']]
        excelDf.rename(columns = {'DDDNH':'semData'}, inplace = True)
    elif stateName == "CS1":
        excelDf = excelDf[['CS-91']]
        excelDf.rename(columns = {'CS-91':'semData'}, inplace = True)
    elif stateName == "MP2":
        excelDf = excelDf[['MP-91']]
        excelDf.rename(columns = {'MP-91':'semData'}, inplace = True)
    elif stateName == "GU2":
        excelDf = excelDf[['GU-91']]
        excelDf.rename(columns = {'GU-91':'semData'}, inplace = True)
    elif stateName == "HZ1":
        excelDf = excelDf[['HZ-91']]
        excelDf.rename(columns = {'HZ-91':'semData'}, inplace = True)
    elif stateName == "MH2":
        excelDf = excelDf[['MH-91']]
        excelDf.rename(columns = {'MH-91':'semData'}, inplace = True)
    elif stateName == "NR1":
        excelDf = excelDf[['NR-93']]
        excelDf.rename(columns = {'NR-93':'semData'}, inplace = True)
        excelDf['semData'] = -1*excelDf['semData']
    elif stateName == "ER1":
        excelDf = excelDf[['ER-91']]
        excelDf.rename(columns = {'ER-91':'semData'}, inplace = True)
        excelDf['semData'] = -1*excelDf['semData']
    elif stateName == "SR1":
        excelDf = excelDf[['SR-91']]
        excelDf.rename(columns = {'SR-91':'semData'}, inplace = True)
        excelDf['semData'] = -1*excelDf['semData']
    # convert string typed column to float
    excelDf['semData'] = excelDf['semData'].astype(float)
    semData = excelDf["semData"].tolist()
    # print(excelDf)
    return semData