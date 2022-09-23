#from src.fetchers.dayPmuAvailabilitySummaryFetcher import fetchPmuAvailabilitySummaryForDate
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from typing import List
# from src.fetcher.fetchSemDataForDate import fetchSemSummaryForDate
from src.fetcher.semDataFetcher.fetchSemDataForDate import fetchSemSummaryForDate
from src.fetcher.scadaDataFetcher.fetchScadaDataForDate import fetchScadaSummaryForDate

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
    while currDate <= reqEndDt:
        # fetch sem data for the date
        # print("sem data processing")
        dailySemData = fetchSemSummaryForDate(semFolderPath, currDate, stateName)
        # print("sem file {}".format(semFolderPath))
        # print(len(semData))
        semData.extend(dailySemData)
        # print("sem data processing ended")
        # fetch scada data and convert min wise to block wise
        dailyScadaData, timeStamp = fetchScadaSummaryForDate(scadaFolderPath, currDate, stateName)
        times.extend(timeStamp)
        scadaData.extend(dailyScadaData)

        currDate += dt.timedelta(days=1)
    dateList = []
    for col in times:
        dateList.append(dt.datetime.strftime(col, '%Y-%m-%d %H:%M:%S'))
    # print(dateList)

    # dataframe for pushing data to DB
    dataDF = pd.DataFrame()
    dataDF['time_stamp']= dateList
    dataDF['SCADA_DATA']= scadaData
    dataDF['SEM_DATA']= semData
    dataDF['CONSTITUENTS_NAME']= stateName
    # convert nan to None
    dataDF = dataDF.where(pd.notnull(dataDF), None)

    # convert dataframe to list of dictionaries
    scadaSemRecords = dataDF.to_dict('records')

    return scadaSemRecords