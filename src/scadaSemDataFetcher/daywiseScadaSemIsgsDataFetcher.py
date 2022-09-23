#from src.fetchers.dayPmuAvailabilitySummaryFetcher import fetchPmuAvailabilitySummaryForDate
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from typing import List
from src.fetcher.semDataFetcher.fetchIsgsSemDataForDate import fetchIsgsSemSummaryForDate
from src.fetcher.scadaDataFetcher.fetchIsgsScadaDataForDate import fetchIsgsScadaSummaryForDate

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
    while currDate <= reqEndDt:
        # print("sem data processing")
        dailySemReData = fetchIsgsSemSummaryForDate(semIsgsFolderPath, currDate,  isgsName)
        # print("sem file {}".format(semIsgsFolderPath))
        # print(len(semData))
        semData.extend(dailySemReData)
        print("sem data processing ended")
        # print(semData)
        dailyScadReData, timeStamp = fetchIsgsScadaSummaryForDate(scadaIsgsFolderPath, currDate,  isgsName)
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
    dataDF['SCADA_DATA_ISGS']= scadaData
    dataDF['SEM_DATA_ISGS']= semData
    dataDF['ISGS_NAME']=  isgsName
    # print(dataDF)
    # convert nan to None
    dataDF = dataDF.where(pd.notnull(dataDF), None)
    # print(dataDF)

    # convert dataframe to list of dictionaries
    scadaSemRecords = dataDF.to_dict('records')

    return scadaSemRecords