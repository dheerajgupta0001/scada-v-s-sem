import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from typing import List
from src.fetcher.semDataFetcher.testFetchSemDataForDate import fetchSemSummaryForDate
from src.fetcher.scadaDataFetcher.fetchScadaDataForDate import fetchScadaSummaryForDate
import logging

def fetchScadaSemRawData(appDbConStr: str, scadaSemFolderPath: str,scadaFolderPath: str, semFolderPath: str, startDate: dt.datetime, endDate: dt.datetime, stateName: str) -> bool:
    """fetches the pmu availability data from excel files 
    and pushes it to the raw data table
    Args:
        appDbConStr (str): application db connection string
        pmuFolderPath (str): folder path of scad vs sem availability data excel files
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
        try:
            dailySemData = fetchSemSummaryForDate(semFolderPath, currDate, stateName)
            semData.extend(dailySemData)
            # logging.warning(f'State sem data fetch success for {stateName} for {currDate}')

        except:
            logging.warning(f'State sem data fetch failed for {stateName} for {currDate}')
        try:
            dailyScadaData, timeStamp = fetchScadaSummaryForDate(scadaFolderPath, currDate, stateName)
            times.extend(timeStamp)
            scadaData.extend(dailyScadaData)
            # logging.warning(f'State scada data fetch success for {stateName} for {currDate}')
        except:
            logging.warning(f'State scada data fetch failed for {stateName} for {currDate}')
        currDate += dt.timedelta(days=1)
    dateList = []
    for col in times:
        dateList.append(dt.datetime.strftime(col, '%Y-%m-%d %H:%M:%S'))
    # print(dateList)

    # dataframe for pushing data to DB
    dataDF = pd.DataFrame()
    # lenScada = len(scadaData)
    # lenSem = len(semData)
    # logging.warning(f'length of SCADA data {lenScada}')
    dataDF['time_stamp']= dateList
    dataDF['SCADA_DATA']= scadaData
    # logging.warning(f'length of SCADA data {lenSem}')
    dataDF['SEM_DATA']= semData
    dataDF['CONSTITUENTS_NAME']= stateName
    # convert nan to None
    dataDF = dataDF.where(pd.notnull(dataDF), None)

    # convert dataframe to list of dictionaries
    scadaSemRecords = dataDF.to_dict('records')

    return scadaSemRecords