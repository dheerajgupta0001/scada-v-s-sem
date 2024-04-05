import datetime as dt
import pandas as pd
from src.fetcher.semDataFetcher.testFetchIsgsSemDataForDate import fetchIsgsSemSummaryForDate
from src.fetcher.scadaDataFetcher.fetchIsgsScadaDataForDate import fetchIsgsScadaSummaryForDate
import logging

def fetchScadaSemIsgsRawData(scadaIsgsFolderPath: str, semIsgsFolderPath: str, startDate: dt.datetime, endDate: dt.datetime, isgsName: str) -> bool:
    """fetches the scada sem re availability data from excel files 
    and pushes it to the raw data table
    Args:
        scadaIsgsFolderPath (str): folder path of scada re availability data excel files
        semIsgsFolderPath (str): folder path of sem re availability data excel files
        startDate (dt.datetime): start date
        endDate (dt.datetime): end date
    Returns:
        [bool]: returns True if succeded
    """
    #isRawDataFetchSuccess = False

    reqStartDt = startDate.date()
    reqEndDt = endDate.date()

    if reqEndDt < reqStartDt:
        return False

    currDate = reqStartDt
    semData = []
    scadaData = []
    times = []
    logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    while currDate <= reqEndDt:
        # logging.warning('ISGS sem data fetch start')
        try:
            dailySemIsgsData = fetchIsgsSemSummaryForDate(semIsgsFolderPath, currDate,  isgsName)
            semData.extend(dailySemIsgsData)
        except:
            logging.warning('ISGS sem data fetch failed')
        # logging.warning('ISGS sem data fetch successful')
        try:
            dailyScadaIsgsData, timeStamp = fetchIsgsScadaSummaryForDate(scadaIsgsFolderPath, currDate,  isgsName)
            times.extend(timeStamp)
            scadaData.extend(dailyScadaIsgsData)
        except:
            logging.warning('ISGS scada data fetch failed')

        currDate += dt.timedelta(days=1)
    # dataframe for pushing data to DB
    dataDF = pd.DataFrame()
    dataDF['time_stamp']= times
    # lenScada = len(scadaData)
    # lenSem = len(semData)
    # logging.warning(f'length of SCADA data {lenScada}')
    dataDF['SCADA_DATA_ISGS']= scadaData
    # logging.warning(f'length of SEM data {lenSem}')
    dataDF['SEM_DATA_ISGS']= semData
    dataDF['ISGS_NAME']=  isgsName
    # convert nan to None
    dataDF = dataDF.where(pd.notnull(dataDF), None)
    # convert dataframe to list of dictionaries
    scadaSemRecords = dataDF.to_dict('records')

    return scadaSemRecords