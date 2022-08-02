import datetime as dt
#from src.typeDefs.pmuAvailabilitySummary import IPmuAvailabilitySummary
from typing import List
import os
import pandas as pd


def fetchScadaSummaryForDate(scadaSemFolderPath: str, targetDt: dt.datetime, stateName: str) -> List :
    """fetched pmu availability summary data rows for a date from excel file

    Args:
        targetDt (dt.datetime): date for which data is to be extracted

    Returns:
        List[IPmuAvailabilitySummary]: list of pmu availability records fetched from the excel data
    """
    # sample excel filename - PMU_availability_Report_05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d_%m_%Y')
    targetFilename = 'ONEMINREP_New_{0}.csv'.format(fileDateStr)
    targetFilePath = os.path.join(scadaSemFolderPath, targetFilename)
    # print(targetFilePath)

    # check if csv file is present
    if not os.path.isfile(targetFilePath):
        print("Scada Excel file for date {0} is not present".format(targetDt))
        return []

    # read pmu excel 
    excelDf = pd.read_csv(targetFilePath, skiprows=2, skipfooter=7, engine='python')
    # print("scada Data")
    if stateName == "TD1":
        column = "DDDNH_Actual"
    elif stateName == "GO1":
        column = "GOA_DRWL_TTL"
    elif stateName == "DD1":
        column = "DD_DRWL_TTL"
    elif stateName == "CS1":
        column = "CSEB_DRWL_TOT"
    elif stateName == "MP2":
        column = "MPEB_DRWL_TOT"
    elif stateName == "MH2":
        column = "MSEB_DRWL_TOT"
    elif stateName == "GU2":
        column = "GEB_DRWL_TOT"
    elif stateName == "NR1":
        column = "WR_NR_FLOW"
    elif stateName == "ER1":
        column = "WR_ER_FLOW"
    elif stateName == "SR1":
        column = "WR_SR_FLOW"
    elif stateName == "HZ1":
        column = "AMNSIL_TOT_DRWL"
    elif stateName == "BR1":
        column = "BARC"
    excelDf = excelDf.loc[:, ["Timestamp", column]]
    # print(excelDf)
    # print(type(excelDf["Timestamp"][0]))
    # print(excelDf["Timestamp"][0])
    # excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"], format="%d-%m-%Y %H:%M:S")
    excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],dayfirst=True)
    excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],format="%d-%m-%Y %H:%M:S")
    # print(excelDf)
    excelDf= excelDf.resample('15min', on='Timestamp').mean()  # resamples as well as make timestamp index
    excelDf[column]= excelDf[[column]].div(4, axis=0)
    scadaData = excelDf[column].tolist()
    timeStamp = list(excelDf.index)

    return scadaData, timeStamp