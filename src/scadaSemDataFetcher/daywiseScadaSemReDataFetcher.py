import datetime as dt
import pandas as pd
from src.fetcher.semDataFetcher.testFetchReSemDataForDate import fetchReSemSummaryForDate
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
        dailySemReData = fetchReSemSummaryForDate(semReFolderPath, currDate,  reName)
        semData.extend(dailySemReData)
        dailyScadReData, timeStamp = fetchReScadaSummaryForDate(scadaReFolderPath, currDate,  reName)
        times.extend(timeStamp)
        scadaData.extend(dailyScadReData)

        currDate += dt.timedelta(days=1)
    # dataframe for pushing data to DB
    dataDF = pd.DataFrame()
    dataDF['time_stamp']= times
    dataDF['SCADA_DATA_RE']= scadaData
    dataDF['SEM_DATA_RE']= semData
    dataDF['RE_NAME']=  reName
    # convert nan to None
    dataDF = dataDF.where(pd.notnull(dataDF), None)
    # convert dataframe to list of dictionaries
    scadaSemRecords = dataDF.to_dict('records')

    return scadaSemRecords