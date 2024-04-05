import datetime as dt
from typing import List
import os
import pandas as pd
import logging
from urllib.parse import urljoin

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
    logging.basicConfig(filename='isgs.log', filemode='w', 
					format='%(asctime)s %(message)s',)

    # sem column name from mapping file
    scadaCol = isgsConfig.loc[isgsConfig['ISGS'] == isgsName, 'SCADA'].iloc[0]
    # sample excel filename -GEN_SCADA_SEM_05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d_%m_%Y')
    targetFilename = 'GEN_SCADA_SEM_{0}.csv'.format(fileDateStr)
    # http://10.2.100.55:8088/SCADA/Reports/GEN_SCADA_SEM/
    # targetFilePath = os.path.join( scadaIsgsFolderPath, targetFilename)
    targetFilePath = urljoin(scadaIsgsFolderPath, targetFilename)
    # print(targetFilePath)

    # check if csv file is present
    '''
    if not os.path.isfile(targetFilePath):
        logging.warning('ISGS scad file not present')
        logging.warning('file path is :{0}'.format(targetFilePath))
        print("ISGS Scada csv file for date {0} is not present".format(targetDt))
        return []
    '''
    # read pmu excel
    try:
        excelDf = pd.read_csv(targetFilePath, skiprows=2, nrows=96)
        # logging.warning(f'ISGS scada file with path {targetFilePath} success')
    except:
        logging.warning(f'Unable to read ISGS scada file with path {targetFilePath}')
        return []
    
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