import datetime as dt
import pandas as pd
from src.fetcher.semDataFetcher.fetchLineSemDataForDate import fetchLineSemSummaryForDate
from src.fetcher.scadaDataFetcher.fetchLineScadaDataForDate import fetchLineScadaSummaryForDate
import logging

def fetchScadaSemLineRawData(scadaLineFolderPath: str, semLineFolderPath: str, startDate: dt.datetime, endDate: dt.datetime, lineName: str) -> bool:
    """fetches the scada sem Line availability data from excel files 
    and pushes it to the raw data table
    Args:
        scadaLineFolderPath (str): folder path of scada line availability data excel files
        semLineFolderPath (str): folder path of sem Line availability data excel files
        startDate (dt.datetime): start date
        endDate (dt.datetime): end date
    Returns:
        [bool]: returns True if succeeded
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
        try:
            dailySemLineData = fetchLineSemSummaryForDate(semLineFolderPath, currDate,  lineName)
            semData.extend(dailySemLineData)
        except:
            logging.warning(f'Line sem data fetch failed for {lineName} for {currDate}')
        try:
            dailyScadaLineData, timeStamp = fetchLineScadaSummaryForDate(scadaLineFolderPath, currDate,  lineName)
            times.extend(timeStamp)
            scadaData.extend(dailyScadaLineData)
        except:
            logging.warning(f'Line scada data fetch failed for {lineName} for {currDate}')
        currDate += dt.timedelta(days=1)
    # dataframe for pushing data to DB
    dataDF = pd.DataFrame()
    dataDF['time_stamp']= times
    dataDF['SCADA_DATA_Line']= scadaData
    dataDF['SEM_DATA_Line']= semData
    dataDF['Line_NAME']=  lineName
    # convert nan to None
    dataDF = dataDF.where(pd.notnull(dataDF), None)
    # convert dataframe to list of dictionaries
    scadaSemRecords = dataDF.to_dict('records')

    return scadaSemRecords