import datetime as dt
from typing import List
import os
import pandas as pd

from src.config.fileMappings import getLinesMappings


def fetchLineScadaSummaryForDate( scadaLineFolderPath: str, targetDt: dt.datetime, lineName: str) -> List :
    """fetched scada line summary data rows for a date from excel file

    Args:
        targetDt (dt.datetime): date for which data is to be extracted

    Returns:
        list of scada line availability records fetched from the excel data
    """
    # get file config
    linesConfig = getLinesMappings()
    # sem column name from mapping file
    scadaCol = linesConfig.loc[linesConfig['Lines'] == lineName, 'SCADA'].iloc[0]
    # sample excel filename SCADA_SEM_01092023
    fileDateStr = dt.datetime.strftime(targetDt, '%d%m%Y')
    targetFilename = 'SCADA_SEM_{0}.xlsx'.format(fileDateStr)
    targetFilePath = os.path.join( scadaLineFolderPath, targetFilename)
    # print(targetFilePath)

    # check if csv file is present
    if not os.path.isfile(targetFilePath):
        print("Lines Scada csv file for date {0} is not present".format(targetDt))
        return []

    # read line data from excel 
    excelDf = pd.read_excel(targetFilePath, nrows=96)

    excelDf = excelDf[["time", scadaCol]]
    excelDf = excelDf.rename(columns={'time': 'Timestamp'})
    excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],dayfirst=True)
    excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],format="%d-%m-%Y %H:%M:S")
    excelDf[scadaCol]= excelDf[[scadaCol]].div(4, axis=0)

    scadaData = excelDf[scadaCol].tolist()
    # timeStamp = list(excelDf.index)
    excelDf['Timestamp'] = pd.to_datetime(excelDf.Timestamp)
    # print(excelDf)
    timeStamp = excelDf["Timestamp"].tolist()
    return scadaData, timeStamp