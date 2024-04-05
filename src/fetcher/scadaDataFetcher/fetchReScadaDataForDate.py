import datetime as dt
from typing import List
import os
import pandas as pd
from src.config.fileMappings import getReMappings
from urllib.parse import urljoin


def fetchReScadaSummaryForDate( scadaReFolderPath: str, targetDt: dt.datetime, reName: str) -> List :
    """fetched pmu availability summary data rows for a date from excel file

    Args:
        targetDt (dt.datetime): date for which data is to be extracted

    Returns:
        List[IPmuAvailabilitySummary]: list of pmu availability records fetched from the excel data
    """
    # get file config
    reConfig = getReMappings()
    # sem column name from mapping file
    scadaCol = reConfig.loc[reConfig['RE'] == reName, 'SCADA'].iloc[0]
    # sample excel filename - PMU_availability_Report_05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d_%m_%Y')
    targetFilename = 'RE_SCADASEM_{0}.csv'.format(fileDateStr)
    # targetFilePath = os.path.join( scadaReFolderPath, targetFilename)
    targetFilePath = urljoin(scadaReFolderPath, targetFilename)
    # print(targetFilePath)

    # check if csv file is present
    # if not os.path.isfile(targetFilePath):
    #     print("RE Scada csv file for date {0} is not present".format(targetDt))
    #     return []

    excelDf = pd.read_csv(targetFilePath, skiprows=2, nrows=96)
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