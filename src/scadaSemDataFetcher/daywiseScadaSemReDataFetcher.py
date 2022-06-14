#from src.fetchers.dayPmuAvailabilitySummaryFetcher import fetchPmuAvailabilitySummaryForDate
import datetime as dt
from os import rename
import pandas as pd
import matplotlib.pyplot as plt
from typing import List
from src.fetcher.semDataFetcher.fetchReSemDataForDate import fetchReSemSummaryForDate
from src.fetcher.scadaDataFetcher.fetchReScadaDataForDate import fetchReScadaSummaryForDate

def fetchScadaSemReRawData(scadaReFolderPath: str, semReFolderPath: str, startDate: dt.datetime, endDate: dt.datetime, reName: str) -> bool:
    """fetches the scada sem re availability data from excel files 
    and pushes it to the raw data table
    Args:
        scadaReFolderPath (str): folder path of scada re availability data excel files
        semReFolderPath (str): folder path of sem re availability data excel files
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
        # print("sem data processing")
        print(reName)
        dailySemReData = fetchReSemSummaryForDate(semReFolderPath, currDate,  reName)
        # print("sem file {}".format(semReFolderPath))
        # print(len(semData))
        semData.extend(dailySemReData)
        # print("sem data processing ended")
        dailyScadReData, timeStamp = fetchReScadaSummaryForDate(scadaReFolderPath, currDate,  reName)
        # print(type(timeStamp[0]))
        times.extend(timeStamp)
        scadaData.extend(dailyScadReData)

        currDate += dt.timedelta(days=1)
    # dateList = []
    # for col in times:
    #     dateList.append(dt.datetime.strptime(col, "%Y-%d-%m %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"))
    #     print(dateList)
        # dateList.append(dt.datetime.strftime(col, '%Y-%m-%d %H:%M:%S'))
    # print(dateList)

    # dataframe for pushing data to DB
    dataDF = pd.DataFrame()
    dataDF['time_stamp']= times
    dataDF['SCADA_DATA_RE']= scadaData
    dataDF['SEM_DATA_RE']= semData
    dataDF['RE_NAME']=  reName
    # print(dataDF)
    # convert nan to None
    dataDF = dataDF.where(pd.notnull(dataDF), None)
    # print(dataDF)

    # convert dataframe to list of dictionaries
    scadaSemRecords = dataDF.to_dict('records')

    return scadaSemRecords