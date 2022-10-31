import datetime as dt
from typing import List
import os
import pandas as pd

from src.config.fileMappings import getIsgsMappings


def fetchIsgsScadaSummaryForDate( scadaIsgsFolderPath: str, targetDt: dt.datetime, isgsName: str) -> List :
    """fetched scada isgs summary data rows for a date from excel file

    Args:
        targetDt (dt.datetime): date for which data is to be extracted

    Returns:
        list of scada isgs availability records fetched from the excel data
    """
    # get file config
    isgsConfig = getIsgsMappings()
    # sem column name from mapping file
    scadaCol = isgsConfig.loc[isgsConfig['ISGS'] == isgsName, 'SCADA'].iloc[0]
    # sample excel filename -GEN_SCADA_SEM_05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d_%m_%Y')
    targetFilename = 'GEN_SCADA_SEM_{0}.csv'.format(fileDateStr)
    targetFilePath = os.path.join( scadaIsgsFolderPath, targetFilename)
    # print(targetFilePath)

    # check if csv file is present
    if not os.path.isfile(targetFilePath):
        print("ISGS Scada csv file for date {0} is not present".format(targetDt))
        return []

    # read pmu excel 
    excelDf = pd.read_csv(targetFilePath, skiprows=2, nrows=96)
    
    #  acbil addition with mcpl test starts
    if isgsName == "AC-91":
        excelDf["ACBIL_EXPP"] = excelDf["ACBIL_EXPP"] + excelDf["MCPL_EXPP"] 

    excelDf = excelDf[["Timestamp", scadaCol]]
    excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],dayfirst=True)
    excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],format="%d-%m-%Y %H:%M:S")
    excelDf[scadaCol]= excelDf[[scadaCol]].div(4, axis=0)

    scadaData = excelDf[scadaCol].tolist()
    # timeStamp = list(excelDf.index)
    excelDf['Timestamp'] = pd.to_datetime(excelDf.Timestamp)
    # print(excelDf)
    timeStamp = excelDf["Timestamp"].tolist()
    return scadaData, timeStamp